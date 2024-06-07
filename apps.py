import streamlit as st
from openai import OpenAI
from config import *
import replicate as rp
import os
import requests
import re
from app import *

st.set_page_config("Humane AI.", "./favicon.ico")

st.sidebar.header(Project_name)
st.sidebar.header(Author)

choice = st.sidebar.radio("Navigate", Menu)

if choice == "Humane AI":
    st.write("""Humane AI""")

if choice == "HumaneGPT":

    openai_api_key = st.sidebar.text_input("OpenAi API key", key = "openai api key", type= "password")
        
    st.title("Humane AI")

    st.caption("""with love\t - AI""")

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

if choice == "HumaneImagin-E":

    #image = "pic.jpg"
    #st.image(image)

    obj = HumaneAi()
    image = obj.humaneImagine(choice)

    if image:
        st.success("If you like the generated image download it from the link before changing the parameters.")
        st.image(image)
        st.success(f"You can download the image by going here: {image[0]}")
    else:
        pass

    with st.expander("This App Generated Images", expanded=True):
            spacer1, col1, spacer2, col2 = st.columns([0.5,4,0.5,4])
            with open('./prompts/prompts.md', 'r') as file:
                for idx, prompt_line in enumerate(file):
                    model_part, prompt_part = prompt_line.split("Prompt:", 1)
                    col_logic = col1 if idx%2 == 0 else col2
                    with col_logic:
                        st.image(f"./generated_images/out-0 ({idx}).png", width=250, caption=prompt_part.strip() + "\n" + model_part.strip())

if choice == 'About':
    st.write("About")