
import numpy as np
from enum import Enum

class Object_Heights(Enum):
    CAN = 12.3  # height in cm


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

        # Object height offset from camera
        object_top_height = Object_Heights.CAN.value
        delta_h = h - object_top_height

        # Calculate ground plane distance
        angle_to_ground = np.radians(pitch) - ty
        
        # DEBUG OUTPUT
        print("="*60)
        print(f"DEBUG INFO:")
        print(f"Pixel coords: u={u:.0f}, v={v:.0f}")
        print(f"Normalized: x={pixel_coord_x:.0f}, y={pixel_coord_y:.0f}")
        print(f"Camera height: {h} cm, Object height: {object_top_height} cm")
        print(f"Delta h: {delta_h} cm")
        print(f"Pitch angle: {pitch}° = {np.radians(pitch):.4f} rad")
        print(f"ty angle: {np.degrees(ty):.2f}° = {ty:.4f} rad")
        print(f"angle_to_ground: {np.degrees(angle_to_ground):.2f}° = {angle_to_ground:.4f} rad")
        print(f"tan(angle_to_ground): {np.tan(angle_to_ground):.4f}")
        print("="*60)
        
        # Distance calculation
        z = delta_h / np.tan(angle_to_ground)
        x = z * np.tan(tx)

        return float(x), float(delta_h), float(z), float(np.degrees(tx)), float(np.degrees(ty))