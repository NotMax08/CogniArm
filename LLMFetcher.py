import google.generativeai as genai

# Put your API key here
API_KEY = "YOUR_API_KEY_HERE"

# Configure
genai.configure(api_key=API_KEY)

# Create model
model = genai.GenerativeModel('gemini-1.5-flash')

# Simple test
response = model.generate_content("Hello Gemini! Say hi back.")
print(response.text)