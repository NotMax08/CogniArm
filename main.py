import cv2
import Detection_Models as dm
import time
import LLM_Fetcher as llm
import SpeechListener 
import JSON_Interpreter
import serial
import time
import serial.tools.list_ports
import Serial

def run_detections():
    for frame_count in range(num_frames_to_process):
        success, frame = cap.read()
        if not success: 
            print("Error: Failed to capture frame")
            break

        detections = can_model.process_frame(frame)
        
        # Get the processed frame with bounding boxes
        processed_frame = detections['frame_with_boxes']
        measurements = detections['measurements']

        # Show the frame
        #cv2.imshow("Object Detection", processed_frame)

        # Print measurements if any detections
        if measurements:
            for detection_id, measurement in measurements.items():
                #print(f"  Detection {detection_id}: {measurement}cm")
                print()
        key = cv2.waitKey(1) & 0xFF
            
            # Check for 'q' key press to quit   
        if key == ord('q'):
            print("\nQuitting...")
            break
        frame_count += 1
    cap.release()
    cv2.destroyAllWindows()

# initializes stuff
can_model = dm.Detection_Models(camera_height= 25.867, pitch_angle=45)
llm_fetcher = llm.LLMFetcher()
listener = SpeechListener.SpeechListener()
serial_connection = Serial.SerialServoConnection()

print("Listening...")
result = listener.listen_for(10)

if result:
    print("You said:", result)
else:
    print("Could not understand audio")


# get webcam ready
cap = cv2.VideoCapture(0)
# Allow the camera to warm up
time.sleep(0.1)

num_frames_to_process = 20
frame_count = 0

run_detections()
    
print(can_model.latest_measurements)
response = llm_fetcher.fetch_response(user_input= result, list_of_objects= can_model.latest_measurements)

print("\nLLM Response:",response)
interpreter = JSON_Interpreter.ProcedureParser()    
interpreter.parse_llm_response(response)

print("\nParsed Procedures:")
for proc in interpreter.procedures:
    state = proc['procedure']['state']
    function = proc['procedure']['function']
    parameters = proc['procedure']['parameters']
    print("state: ", state)
    print("function: ", function)

    if "move_to_position" in function:
        x = int(parameters['x']) 
        y = int(parameters['y']) 
        z = int(parameters['z']) 
        orientation = int(parameters['orientation'])
        print(f"move to {x}, {y}, {z}, at orientation {orientation}.")

        serial_connection.send_command(f"move_to_position {12} {12} {12} {90}")

    elif "wait_in_seconds" in function:
        duration = int(parameters['duration'])
        print(f"wait {duration}")
        serial_connection.send_command(f"wait_in_seconds {duration}")
    
    elif "grab" in function:
        serial_connection.send_command(f"grab")
        
    print("----")

    
serial_connection.send_command("finished")
