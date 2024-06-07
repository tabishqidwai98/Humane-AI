import streamlit as st
import google.generativeai as genai
from config import *

st.title("Humane AI")

#st.markdown("\twith Love💞")
st.caption("-with love💞")

menu = ['Gemini Ai','Mistral-7b', 'MusicGenMeta','stableai']

option = st.sidebar.selectbox("the feature you want",menu)

if option == 'Gemini Ai':
    st.header("Gemini Ai")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "parts":"How can i help you today?"}]
    
    for msg in st.session_state.mesasges:
        st.chat_message(msg["role"]).write(msg["parts"])
    
    

if option == 'Mistral-7b':
    st.text('hello')

if option == 'MusicGen':
    st.text('hello')

if option == 'stableai':
    st.text('hello')