import cv2
import numpy as np
from inference import get_model
from Distance_Calculator import Distance_Calculator

class Detection_Models:
    def __init__(self, camera_height, pitch_angle):
        # Initialize the model for single frame inference
        self.model = get_model(
            model_id="detect-can-cwnex/1",
            api_key="08XDdvmafTKglDwQgEyJ"
        )
        
        # Initialize distance calculator
        self.distance_calculator = Distance_Calculator(camera_height, pitch_angle, 'can')
        
        # For storing the latest predictions
        self.latest_measurements = {}


    def process_frame(self, frame):
        
        # Run inference on the frame
        results = self.model.infer(frame, confidence=0.6)
        
        
        # Convert to list of dictionaries in your expected format
        predictions = self._convert_predictions_to_dict(results, frame.shape)
        
        # Create a copy of the frame for drawing
        frame_with_boxes = frame.copy()
        
        # Calculate distances and draw detections
        distances = {}
        if predictions and 'predictions' in predictions and predictions['predictions']:
            for pred in predictions['predictions']: 
                class_name = pred['class_id']
                coord_x = int(pred['x'])
                coord_y = int(pred['y'])

                x, y, z, tx, ty = self.distance_calculator.calculate_real_world_coordinates(coord_x, coord_y)
                arm_x, arm_y, arm_z = self.distance_calculator.convert_local_to_arm_frame(x,y,z)
                

                if (class_name == 2):  # Assuming class_id 2 corresponds to 'can'
                    class_name = 'can'

                measurements = {
                    "class_id": class_name,
                    "x_cm": arm_x,
                    "y_cm": arm_y,
                    "z_cm": arm_z,
                    "tx": tx,
                    "ty": ty
                }
                # Stores a hashmap of class name to measurements
                if (class_name == 2):  # Assuming class_id 2 corresponds to 'can'
                    class_name = 'can'
                self.latest_measurements[class_name] = measurements

            # Draw detections on the frame
            self._draw_detections(frame_with_boxes, predictions, measurements)
        else:
            print("No valid detections found.")

        return {
            'frame_with_boxes': frame_with_boxes,
            'measurements': self.latest_measurements
        }

    def _convert_predictions_to_dict(self, inference_results, frame_shape):
        
        # Get the first result from the list
        result = inference_results[0]
        
        
        predictions_list = []
        
        
        for i, pred in enumerate(result.predictions):
            # Extract prediction data
            pred_dict = {
                'x': pred.x,  # Center X
                'y': pred.y,  # Center Y
                'width': pred.width,
                'height': pred.height,
                'confidence': pred.confidence,
                'class': pred.class_name,
                'class_id': pred.class_id,
                'detection_id': f"det_{i}_{int(pred.confidence * 100)}"
            }
            predictions_list.append(pred_dict)
        
        return {
            'predictions': predictions_list,
            'image': {
                'width': frame_shape[1],
                'height': frame_shape[0]
            }
        }

    def _draw_detections(self, frame, predictions, measurements):
        """Draw bounding boxes and labels on the frame"""
        if predictions and 'predictions' in predictions:
            for i, pred in enumerate(predictions['predictions']):
                # Extract prediction data
                x = int(pred['x'])
                y = int(pred['y'])
                width = int(pred['width'])
                height = int(pred['height'])
                confidence = pred.get('confidence', 0)
                class_name = pred.get('class', 'unknown')
                distance = pred.get('distance', 0)
                detection_id = pred.get('detection_id', str(i))
                
                # Calculate bounding box corners
                x1 = max(0, x - width // 2)
                y1 = max(0, y - height // 2)
                x2 = min(frame.shape[1], x + width // 2)
                y2 = min(frame.shape[0], y + height // 2)
                
                # Draw rectangle (green)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label background
                label = f"{class_name}: {confidence:.2f}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                label_y = max(y1 - 10, 20)  # Ensure label doesn't go off top of screen
                
                cv2.rectangle(
                    frame,
                    (x1, label_y - label_size[1]),
                    (x1 + label_size[0], label_y),
                    (0, 255, 0),
                    -1  # Filled rectangle
                )
                
                # Draw label text (black)
                cv2.putText(
                    frame,
                    label,
                    (x1, label_y - 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    2
                )

                label_2 = "x_cm: {:.1f}, y_cm: {:.1f}, z_cm: {:.1f}, tx: {:.1f}, ty: {:.1f}".format(
                        measurements['x_cm'],
                        measurements['y_cm'],
                        measurements['z_cm'],
                        measurements['tx'],
                        measurements['ty']
                    )
                label_size2  = cv2.getTextSize(label_2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                label_2_y = label_y + label_size[1] + 5
                cv2.rectangle(
                    frame,
                    (x1, label_2_y - label_size2[1] - 3),
                    (x1 + label_size2[0], label_2_y + 10),
                    (0, 255, 0),
                    -1  # Filled rectangle
                )

                cv2.putText(
                    frame,
                    label_2,
                    (x1, label_2_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0,0,0),
                    2
                )

                cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)  # Draw center point