import time
import math
from newIK import IK
from servo import Servo, servo2040 # type: ignore

class ServoController:
    def __init__(self, pin, range, direction):
        self.pin = pin
        self.range = 90/(range/2)
        self.servo = Servo(pin)
        self.direction = direction

   
    def rotateAngle(self, angle):
        if self.direction == "negative":
            angle = -angle
        self.servo.value(angle*self.range)
    @staticmethod
    def MoveOnCoordinate (angles):
        theta1,theta2,theta3,theta4 = angles
        print(angles)
        turret.rotateAngle(theta1)
        time.sleep(0.3)
        pitch1.rotateAngle(theta2)
        time.sleep(0.3)
        pitch2.rotateAngle(theta3)
        time.sleep(0.3)
        pitch3.rotateAngle(theta4)

turret = ServoController(0, 270,"positive")
pitch1 = ServoController(1, 270,"positive")
pitch2 = ServoController(2, 270,"negative")
pitch3 = ServoController(3, 180,"positive")
claw = ServoController(4, 180,"positive")
zero = 0,0,0,0
straight = 0,90,0,0

ServoController.MoveOnCoordinate(IK.solver(20,30,0,90))
print(IK.solver(20,30,0,90))
time.sleep(1)
