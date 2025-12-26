#create a venv for every single project, allows to isolate dependencies
from google import genai

class LLMFetcher:
    def __init__(self):
        self.api_key = 'AIzaSyBAkaqZL0W3J08I449kJw8vsKfBzoqiKMI'
        self.model = 'gemini-2.5-flash'
        self.client = genai.Client(api_key=self.api_key)
        
    
    def fetch_response(self, prompt):
        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )
        return response.text
