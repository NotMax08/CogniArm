import time
from servo import Servo # type: ignore
import sys

while True:
    command = input()
    print(f"Received: {command}")
    
    parts = command.split()
    
    function = parts[0]
    
    if function == "move_to_position":
        if len(parts) >= 4:
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])
            
            print(f"Moving to x={x}, y={y}, z={z}")
        else:
            print("Error: move_to_position needs 3 coordinates (x, y, z)")
    
    elif function == "grab":
        print("Executing grab")

    elif function == "wait":
        duration = float(parts[1])
        print(f"wait {duration}")
    
    else:
        print(f"finished")
    