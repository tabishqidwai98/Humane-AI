import google.generativeai as genai
from config import *

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY = keys['GOOGLE_API_KEY']

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

response = chat.send_message('Explain to a child, the Electromagnetic specturm')

print(response.text.strip())

response = chat.send_message("In one sentence, explain how a computer works to a young child.")
print(response.text.lstrip())

chat.history

for message in chat.history:
  print(f'**{message.role}**: {message.parts[0].text}')