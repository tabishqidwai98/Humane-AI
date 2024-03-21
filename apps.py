import streamlit as st
from openai import OpenAI

with st.sidebar:
    openai_api_key = st.text_input("OpenAi API key", key = "openai api key", type= "password")

st.title("humane Ai")

st.caption("""hey, with love 
           - AI""")

if "messages" not in st.session_state:
     st.session_state['messages'] = [{"role": "assistant", "content" : "How can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


prompt = st.chat_input('Say something')
if prompt:
    if not openai_api_key:
        st.info('Please add your Open API key to continue.')
        st.stop()

    clients = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", 'content': prompt})
    st.chat_message("user").write(prompt)
    response = clients.chat.completions.create(model="gpt-3.5-turbo", messages = st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role" : "assistant", "content" : msg})
    st.chat_message("assistant").write(msg)