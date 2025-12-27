import time
import RobotController
from servo import Servo # type: ignore
import sys

robot = RobotController.RobotController()
instructions = []
while True:
    command = input()
    print(f"Received: {command}")

    if command == "finished":
        break

    instructions.append(command)

for action in instructions:

    parts = action.split()

    function = parts[0]

    if function == "move_to_position":
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])
            orientation = float(parts[4])
            #print(f"Moving to x={x}, y={y}, z={z} at at an angle of {orientation}")
            robot.move_to_position((x,y,z),orientation)


    elif function == "wait_in_seconds":
        duration = float(parts[1])
        robot.wait_in_seconds(duration)

    elif function == "grab":
        #print("Executing grab")
        robot.grab()

    elif function == "release":
        #print("Executing release")
        robot.release()
