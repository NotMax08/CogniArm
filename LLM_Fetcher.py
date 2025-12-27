#create a venv for every single project, allows to isolate dependencies
from google import genai

class LLMFetcher:
    def __init__(self):
        self.api_key = 'AIzaSyD6olJuxUCOWC-g_OW-pRXEuZTVOr3R_QQ'
        self.model = 'gemini-2.5-flash'
        self.client = genai.Client(api_key=self.api_key)
        self.conditions = """
        You are a robotic arm controller. Based on the user's voice command, generate a JSON response with the following structure: 
        {
            "state": [(ie.1)],
            "function": "[function_name]",
            "parameters": {
            "x": [x_coordinate],
            "y": [y_coordinate], 
            "z": [z_coordinate],
            "orientation": [orientation],
        }
        {
            "state": [(ie.2)],
            "function": "[function_name]",
            "parameters": {
            "x": [x_coordinate],
            "y": [y_coordinate], 
            "z": [z_coordinate],
            "orientation": [orientation]
        }
        }

        

        Available functions:
            1. "move_to_position" - Move to specific coordinates (param x, y, z, orientation of end effector)
            2. "wait_in_seconds" - Wait for a specified number of seconds (param duration)
            3. "grab" - grab with claw (no parameters)

        State management: Increment the state number by 1 for each new action in a sequence.


        Here is an example:

        {
            "state": [1],
            "function": "[move_to_position]",
            "parameters": {
            "x": [12],
            "y": [12], 
            "z": [12],
            "orientation": [0],
        }
        {
            "state": [(ie.2)],
            "function": "[wait_in_seconds]",
            "parameters": {
            "duration": [1]
        }
        }

        Rules:
        - Orientation of end effector means the angle of the claw with respect to the ground, in degrees. 0 degrees means the claw is parallel to the ground, 90 degrees means the claw is perpendicular to the ground, facing downwards. 180 degrees means the claw is perpendicular to the ground, facing upwards.
        - Here is your robotic arm that you are controlling and the joint type from bottom to top, coordiante (0,0,0) is the base, of the robotic arm on the floor
            1. Yaw joint
            2. Pitch joint (elevated 12.cm from the base)
            3. Pitch joint 
            4. pitch joint
            5. Claw (open/close)
        - Here are the arm dimensions:
            0. Yaw: 6.0cm above the bas
            1. Pitch1 to Pitch2: 12.0cm
            2. Pitch2 to Pitch3: 12.0cm
            3. Pitch3 to Claw: 6.0cm
        - Only return valid JSON, no additional text
        - Choose the most appropriate function based on the command
        - If coordinates are not provided in the command, use default values of x: 0, y: 0, z: 0
        - if a function does not have parameters, leave the parameters as null
        - If you must grab something, you must move to the position first before grabbing.
        - The grab command will only close the claw, it will not move the robotic arm.
        - the wait command does not require an orientation parameter, th wait command will only pause of the specified duration in seconds
        - Other than moving to objects, the user can also ask for gestures like waving "hi" and, you must create a multiple actions involving move_to_position" and ample "wait_in_seconds" to simulate these gestures.
        - Additionally, the user can ask for yes/no questions, and you must nod "yes" or shake your head, "no" to simulate the gesture

        User command: [INSERT_USER_COMMAND_HERE]
        """
        
    
    def fetch_response(self, user_input, list_of_objects):
        self.conditions += f"\n Available objects in the environment: {list_of_objects}\n"
        self.conditions = self.conditions.replace("[INSERT_USER_COMMAND_HERE]", user_input)
        #print(self.conditions)
        response = self.client.models.generate_content(
            model=self.model, 
            #replaces user command with actual user input
            contents=self.conditions
        )
        return response.text
