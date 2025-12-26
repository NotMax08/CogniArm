import cv2
import Detection_Models as dm
import time

# Initialize the detection model
can_model = dm.Detection_Models(camera_height= 3, pitch_angle=1)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Create window
cv2.namedWindow("Object Detection", cv2.WINDOW_NORMAL)


while True:
    success, frame = cap.read()
    if not success:
        print("Error: Failed to capture frame")
        break

    result = can_model.process_frame(frame)
    
    # Get the processed frame with bounding boxes
    processed_frame = result['frame_with_boxes']
    measurements = result['measurements']

    # Show the frame
    cv2.imshow("Object Detection", processed_frame)

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
    

cap.release()
cv2.destroyAllWindows()