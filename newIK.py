class IK:
    @staticmethod
    def solver(x,y,z,effectorAngle):
        import math

        x = x*10 # Converting all cm inputs into mm
        y = y*10 
        z = z*10 

        base = 127
        L1 = 120
        L2 = 120
        L3 = 60

        if z != 0:
            theta1 = math.degrees(math.atan(x/z))
        else:
            theta1 = 0

        x = math.sqrt(x**2+z**2) # Remap x into 2 dimensions

        x = x - L3 # Apply offset for claw length

        y = y-base # Apply offset for base height

        theta2 = math.degrees(math.atan((240*y)/(240*x)) + math.acos((x**2+y**2)/(240*math.sqrt(x**2+y**2))))

        d = math.sqrt(x**2+y**2)

        theta3 = math.degrees(math.acos((d**2-L1**2-L2**2)/(-2*L1*L2))) + 180

        theta4 = effectorAngle -(theta2+theta3)

        theta4 = theta4 % 360 # Normalize angle into the 1st Quadrant
        if theta1 > 180:
            theta1 = -(360-theta1)
        if theta2 > 180: # turn reflex (>180) angles into negative angles
            theta2 = -(360-theta2)
        if theta3 > 180:
            theta3 = -(360-theta3)
        if theta4 > 180:
            theta4 = -(360-theta4)

        if theta4 > 90:
            theta4 = 90
        if theta4 < -90:
            theta4 = -90

        
        if abs(theta1) > 135 or abs(theta2) > 135 or abs(theta3) > 135 or abs(theta4) > 90: # Check if angle is out of servo range
            return 0, 0, 0, 0
        
        return theta1,theta2,theta3,theta4

