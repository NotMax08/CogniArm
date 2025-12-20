#need to import the project on python 3.13, was on the wrong version

from google import genai

# Only run this block for Gemini Developer API
client = genai.Client(api_key='AIzaSyBAkaqZL0W3J08I449kJw8vsKfBzoqiKMI')
response = client.models.generate_content(
    model='gemini-2.5-flash', contents='Why is the sky blue?'
)
print(response.text)