import time
from newIK import IK
from servo import Servo  # type: ignore


class ServoController:
    def __init__(self, pin, range, direction):
        self.pin = pin
        self.range = 90/(range/2)
        self.servo = Servo(pin)
        self.direction = direction
    def rotate_angle(self, angle):
        if self.direction == "negative":
            angle = -angle
        self.servo.value(angle*self.range)