
import numpy as np
from enum import Enum

class Object_Heights(Enum):
    CAN = 12.3 / 2  # height in cm, but when it scans, it gets the middle point not the top point


class Distance_Calculator:
    def __init__(self, camera_height, pitch_angle, object_to_grab):
        self.camera_params = {
            'fx': 950,       # focal length x (pixels)
            'fy': 950,       # focal length y (pixels)
            'cx': 960,        # optical center x (pixels)
            'cy': 540,        # optical center y (pixels)
            'camera_height': camera_height,  # in cm
            'pitch_angle': pitch_angle  # in degrees
        }

    def calculate_real_world_coordinates(self, pixel_cord_x, pixel_coord_y):
        fx = self.camera_params['fx']
        fy = self.camera_params['fy']
        cx = self.camera_params['cx']
        cy = self.camera_params['cy']
        h = self.camera_params['camera_height']
        pitch = self.camera_params['pitch_angle']

        u = pixel_cord_x 
        v = pixel_coord_y

        # Normalized image coordinates
        pixel_coord_x = u - cx
        pixel_coord_y = v - cy

        # Calculate angles in radians
        tx = np.arctan2(pixel_coord_x, fx)
        ty = np.arctan2(pixel_coord_y, fy)

        # object height
        object_top_height = Object_Heights.CAN.value

        # Calculate difference in height
        delta_h = h - object_top_height

        # we subtract ty from pitch because if object is above the centerline, ty would be negative, we want the opposite
        angle_to_ground = np.radians(pitch) - ty
        # Distance calculation
        z = delta_h * np.tan(angle_to_ground)
        x = z * np.tan(tx)

        return float(x), float(delta_h), float(z), float(np.degrees(tx)), float(np.degrees(ty))

    def convert_local_to_arm_frame(self, x_distance, y_distance, z_distance):
        # Placeholder for conversion logic
        # This would depend on the specific robotic arm's coordinate system
        x_distance_to_arm = 39
        y_distance_to_arm = 0
        z_distance_to_arm = 0

        arm_x = x_distance_to_arm - x_distance
        arm_y = y_distance_to_arm - y_distance
        arm_z = z_distance_to_arm - z_distance
        return arm_x, arm_y, arm_z