import Serial
serial_connection = Serial.SerialServoConnection()
serial_connection.send_command(f"move_to_position {12} {12} {12} {90}")