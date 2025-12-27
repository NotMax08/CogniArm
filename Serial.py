import serial
import time

class SerialServoConnection:
    def __init__(self, port='/dev/tty.usbmodem1101', baudrate=115200):
        """
        Initialize serial connection to Servo2040
        
        Find your port by running in terminal:
        ls /dev/tty.usb*
        """
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Wait for connection to establish
            print(f"✓ Connected to Servo2040 on {port}")
        except Exception as e:
            print(f"✗ Error connecting: {e}")
            print("Make sure Servo2040 is connected and the port is correct")
            self.ser = None
    
    def send_command(self, command):
        """
        Send command to Servo2040
        
        Args:
            command: string command (e.g., "move_to_position 10 20 30 90")
        """
        if not self.ser:
            print("Not connected to Servo2040")
            return False
        
        try:
            # Ensure command ends with newline and encode to bytes
            if not command.endswith('\n'):
                command += '\n'
            
            self.ser.write(command.encode('utf-8'))
            print(f"Sent: {command.strip()}")
            
            # Optional: Wait for acknowledgment
            time.sleep(0.1)  # Give device time to respond
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').strip()
                print(f"Response: {response}")
            
            return True
        except Exception as e:
            print(f"Error sending command: {e}")
            return False
    
    def close(self):
        """Close serial connection"""
        if self.ser:
            self.ser.close()
            print("Connection closed")