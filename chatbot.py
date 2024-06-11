import streamlit as st
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from config import *

if 'chat_history' not in st.session_state:
    st.session_state.messages = []

genai.configure(api_key=keys['GOOGLE_API_KEY'])

# Display chat messages
if prompt:= st.chat_input('Say Something'):
    st.session_state.messages.append({'role':'user', 'parts': prompt})
    st.chat_message("user").write(prompt)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.start_chat(prompt)
    content = response.text
    
    st.session_state.messages.append({"role": "assistant", "parts": content})

    st.chat_message('assistant').write(content)