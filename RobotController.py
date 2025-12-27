import newIK
import ServoController
import time

class RobotController:
    def __init__(self):
        self.turret = ServoController.ServoController(0,270,"positive")
        self.pitch1 = ServoController.ServoController(1, 270,"positive")
        self.pitch2 = ServoController.ServoController(2, 270,"negative")
        self.pitch3 = ServoController.ServoController(3, 180,"positive")
        self.claw = ServoController.ServoController(4, 180,"positive")
    
    def move_to_position(self,coordinate,effectorAngle):
        buffer = 0.3
        IK = newIK.IK()
        theta1,theta2,theta3,theta4 = IK.solver(coordinate,effectorAngle)
        self.turret.rotate_angle(theta1)
        time.sleep(buffer)
        self.pitch1.rotate_angle(theta2)
        time.sleep(buffer)
        self.pitch2.rotate_angle(theta3)
        time.sleep(buffer)
        self.pitch3.rotate_angle(theta4)
    
    @staticmethod
    def wait_in_seconds(duration):
        time.sleep(duration)
