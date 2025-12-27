import json
import re
import time

class ProcedureParser:
    def __init__(self):
        self.procedures = []
        self.last_response = ""
    
    def parse_llm_response(self, llm_response):
        """
        Parse LLM response that contains multiple JSON objects
        Returns a list of procedure dictionaries
        """
        self.procedures = []
        self.last_response = llm_response.strip()
        
        if not self.last_response:
            print("⚠️ Empty LLM response received")
            return []
        
        print(f"📥 Raw LLM response length: {len(self.last_response)} chars")
        
        # Clean the response first
        cleaned_response = self._clean_response(self.last_response)
        
        # Method 1: Try to parse as a single JSON first
        try:
            data = json.loads(cleaned_response)
            self._process_parsed_data(data)
            if self.procedures:
                print(f"✅ Parsed {len(self.procedures)} procedure(s) as single JSON")
                return self.procedures
        except json.JSONDecodeError as e:
            print(f"⚠️ Not a single JSON: {e}")
        
        # Method 2: Extract all JSON objects using regex
        self._extract_multiple_json_objects(cleaned_response)
        
        # Method 3: Try to find procedures in any format
        if not self.procedures:
            self._find_procedures_any_format(cleaned_response)
        
        print(f"📋 Total procedures parsed: {len(self.procedures)}")
        return self.procedures
    
    def _clean_response(self, response):
        """Clean the LLM response before parsing"""
        # Remove the ```json markers if present
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'\s*```', '', response)
        
        # Fix the array values - extract first element from [value] arrays
        response = re.sub(r'\[\s*(\d+(?:\.\d+)?)\s*\]', r'\1', response)  # Numbers
        response = re.sub(r'\[\s*"([^"]+)"\s*\]', r'"\1"', response)  # Strings in quotes
        response = re.sub(r'\[\s*([^\[\]]+?)\s*\]', r'"\1"', response)  # Strings without quotes
        
        return response.strip()
    
    def _extract_multiple_json_objects(self, response):
        """Extract multiple JSON objects that are not in an array"""
        # Split response by lines to find individual JSON objects
        lines = response.split('\n')
        current_object = []
        brace_count = 0
        in_object = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            for char in line:
                if char == '{':
                    brace_count += 1
                    if brace_count == 1:
                        in_object = True
                        current_object = ['{']
                    else:
                        current_object.append(char)
                elif char == '}':
                    brace_count -= 1
                    current_object.append(char)
                    
                    if brace_count == 0 and in_object:
                        in_object = False
                        # Try to parse the collected object
                        json_str = ''.join(current_object)
                        try:
                            data = json.loads(json_str)
                            self._add_procedure(data)
                        except json.JSONDecodeError:
                            # Try to fix it
                            fixed_json = self._fix_json(json_str)
                            if fixed_json:
                                try:
                                    data = json.loads(fixed_json)
                                    self._add_procedure(data)
                                except json.JSONDecodeError:
                                    pass
                        current_object = []
                elif in_object:
                    current_object.append(char)
    
    def _process_parsed_data(self, data):
        """Process parsed JSON data"""
        if isinstance(data, list):
            # It's a list of procedures
            for item in data:
                if isinstance(item, dict):
                    self._add_procedure(item)
        elif isinstance(data, dict):
            # Check if it's a single procedure or multiple
            if 'procedure' in data:
                # Single procedure with 'procedure' key
                self._add_procedure(data['procedure'])
            elif any(key.startswith('procedure') for key in data.keys()):
                # Multiple procedures like procedure_1, procedure_2, etc.
                for key in sorted(data.keys()):
                    if isinstance(data[key], dict):
                        self._add_procedure(data[key])
            else:
                # Might be a procedure directly
                if 'function' in data and 'parameters' in data:
                    self._add_procedure(data)
                else:
                    # Search recursively
                    self._find_procedures_in_dict(data)
    
    def _add_procedure(self, proc_dict):
        """Add a procedure to the list, ensuring it has all required parameters"""
        if not isinstance(proc_dict, dict):
            return
        
        # Clean the function name - remove brackets if present
        if 'function' in proc_dict:
            func = proc_dict['function']
            if isinstance(func, str):
                # Remove [ and ] if present
                func = func.replace('[', '').replace(']', '')
                proc_dict['function'] = func
        
        # Ensure parameters dictionary exists
        if 'parameters' not in proc_dict:
            proc_dict['parameters'] = {}
        
        # Ensure orientation parameter exists with default value
        if 'orientation' not in proc_dict['parameters']:
            proc_dict['parameters']['orientation'] = 0  # Default orientation
        
        # Clean parameter values - extract from arrays if needed
        if 'parameters' in proc_dict and isinstance(proc_dict['parameters'], dict):
            for key, value in proc_dict['parameters'].items():
                if isinstance(value, list) and len(value) == 1:
                    # Extract single value from array
                    proc_dict['parameters'][key] = value[0]
        
        # Convert string numbers to actual numbers
        if 'parameters' in proc_dict:
            params = proc_dict['parameters']
            for key in ['x', 'y', 'z', 'orientation', 'duration']:
                if key in params and isinstance(params[key], str):
                    try:
                        # Try to convert to float or int
                        if '.' in params[key]:
                            params[key] = float(params[key])
                        else:
                            params[key] = int(params[key])
                    except ValueError:
                        pass
        
        # Add to procedures
        self.procedures.append({'procedure': proc_dict})
    
    def _extract_json_objects(self, response):
        """Extract JSON objects from markdown code blocks"""
        # Try different patterns
        patterns = [
            r'```json\s*(.*?)\s*```',  # ```json ... ```
            r'```\s*(.*?)\s*```',      # ``` ... ```
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            for match in matches:
                json_str = match.strip()
                if not json_str:
                    continue
                
                # Try to parse as JSON
                try:
                    data = json.loads(json_str)
                    self._process_parsed_data(data)
                except json.JSONDecodeError as e:
                    # Try to fix common issues
                    fixed_json = self._fix_json(json_str)
                    if fixed_json:
                        try:
                            data = json.loads(fixed_json)
                            self._process_parsed_data(data)
                        except json.JSONDecodeError:
                            continue
                    continue
    
    def _clean_json_string(self, json_str):
        """Clean JSON string before parsing"""
        # Remove any non-JSON content at beginning/end
        json_str = re.sub(r'^[^{[]*', '', json_str)
        json_str = re.sub(r'[^}\]]*$', '', json_str)
        
        # Remove trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        return json_str.strip()
    
    def _fix_json(self, json_str):
        """Try to fix common JSON formatting issues"""
        try:
            # Convert single quotes to double quotes
            json_str = json_str.replace("'", '"')
            
            # Add missing quotes around unquoted keys
            # Match word characters followed by colon
            json_str = re.sub(r'(\w+)(?=\s*:)', r'"\1"', json_str)
            
            # Fix missing commas between objects in array
            json_str = re.sub(r'}\s*{', '},{', json_str)
            
            return json_str
        except:
            return None
    
    def _find_procedures_any_format(self, response):
        """Find procedures in various formats"""
        # Look for procedure patterns
        procedure_patterns = [
            r'"procedure[^"]*"\s*:\s*(\{.*?\})(?=\s*,|\s*\})',
            r'"function"\s*:\s*"[^"]*".*?"parameters"\s*:\s*\{.*?\}',
        ]
        
        for pattern in procedure_patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            for match in matches:
                try:
                    # Add wrapper if needed
                    if not match.strip().startswith('{'):
                        match = '{' + match
                    if not match.strip().endswith('}'):
                        match = match + '}'
                    
                    data = json.loads(match)
                    if isinstance(data, dict):
                        self._add_procedure(data)
                except:
                    continue
    
    def _is_float(self, value):
        """Check if string can be converted to float"""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def _find_procedures_in_dict(self, data):
        """Find procedures in nested dictionary structure"""
        if isinstance(data, dict):
            # Check if this dict looks like a procedure
            if 'function' in data and ('parameters' in data or any(k in data for k in ['x', 'y', 'z', 'orientation'])):
                # It might be a procedure already
                if 'parameters' not in data:
                    # Extract parameters from root level
                    params = {}
                    for key in ['x', 'y', 'z', 'orientation', 'duration', 'object_id']:
                        if key in data:
                            params[key] = data[key]
                    data['parameters'] = params
                self._add_procedure(data)
                return
            
            # Search recursively
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    self._find_procedures_in_dict(value)
        elif isinstance(data, list):
            for item in data:
                self._find_procedures_in_dict(item)
    
    def get_procedure_steps(self):
        """Get a clean list of procedure steps"""
        steps = []
        for proc in self.procedures:
            if 'procedure' in proc:
                steps.append(proc['procedure'])
        return steps
    
    def get_state_sequence(self):
        """Get procedures sorted by state"""
        steps = self.get_procedure_steps()
        # Sort by state if available
        try:
            steps.sort(key=lambda x: x.get('state', 0))
        except:
            # Keep original order if sorting fails
            pass
        return steps
    
    def execute_procedures(self, robotic_arm, confirm_before_execute=True):
        """
        Execute all parsed procedures on a robotic arm
        
        Args:
            robotic_arm: An object with methods corresponding to procedure functions
            confirm_before_execute: Ask for confirmation before executing
        """
        steps = self.get_state_sequence()
        
        if not steps:
            print("❌ No procedures to execute")
            return False
        
        print(f"\n📋 Found {len(steps)} procedure(s):")
        for i, step in enumerate(steps):
            state = step.get('state', i+1)
            function_name = step.get('function', 'unknown')
            params = step.get('parameters', {})
            
            # Add orientation to display if not present
            if 'orientation' not in params and function_name in ['move_to_position', 'place_object']:
                params['orientation'] = 0  # Default
            
            print(f"  {i+1}. State {state}: {function_name}")
            print(f"     Parameters: {params}")
        
        if confirm_before_execute:
            print("\n" + "-"*60)
            confirm = input("Execute these procedures? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Execution cancelled")
                return False
        
        print("\n▶️ Starting execution...")
        
        for i, step in enumerate(steps):
            state = step.get('state', i+1)
            function_name = step.get('function', '')
            parameters = step.get('parameters', {})
            
            print(f"\n[{i+1}/{len(steps)}] Executing State {state}: {function_name}")
            print(f"    Parameters: {parameters}")
            
            # Map function name to robotic arm method
            if hasattr(robotic_arm, function_name):
                method = getattr(robotic_arm, function_name)
                try:
                    # Execute the method with parameters
                    print(f"    ⚙️ Calling {function_name} with {parameters}")
                    result = method(**parameters)
                    print(f"    ✅ Success: {result}")
                except TypeError as e:
                    # Try with fewer parameters
                    print(f"    ⚠️ Type error: {e}")
                    print(f"    🔄 Trying with filtered parameters...")
                    filtered_params = self._filter_parameters(parameters, method)
                    try:
                        result = method(**filtered_params)
                        print(f"    ✅ Success: {result}")
                    except Exception as e2:
                        print(f"    ❌ Error: {e2}")
                except Exception as e:
                    print(f"    ❌ Error executing {function_name}: {e}")
            else:
                print(f"    ⚠️ Function '{function_name}' not found in robotic arm")
        
        print("\n✅ All procedures executed!")
        return True
    
    def _filter_parameters(self, parameters, method):
        """Filter parameters to match method signature"""
        import inspect
        try:
            # Get method signature
            sig = inspect.signature(method)
            valid_params = list(sig.parameters.keys())
            
            # Filter parameters to only include valid ones
            filtered = {k: v for k, v in parameters.items() if k in valid_params}
            print(f"    Filtered parameters: {filtered} (from {parameters})")
            return filtered
        except:
            # If we can't inspect, use all parameters
            return parameters