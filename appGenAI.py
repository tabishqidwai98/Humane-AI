import streamlit as st
import google.generativeai as genai
from config import *
import time
import random
from audiocraft.models import MusicGen
from audiocraft.data.audio_utils import i16_pcm, normalize_audio
import torch
import torchaudio

st.set_page_config(
    page_title="Humane AI",
    page_icon="💞"
)

#st.markdown("\twith Love💞")
st.title("Humane AI")
st.caption("-with love💞")

menu = ['Gemini Ai','Mistral-7b', 'MusicGenMeta','stableai']

option = st.sidebar.selectbox("the feature you want",menu)

if option == 'Gemini Ai':
    st.markdown('''A Chatbot Powered by **:red[Google Gemini Pro]**''')

    # Initialize Gemini-Pro 
    genai.configure(api_key=keys['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('gemini-pro')

    # Gemini uses 'model' for assistant; Streamlit uses 'assistant'
    def role_to_streamlit(role):
        if role == "model":
            return "assistant"
        else:
            return role

    # Add a Gemini Chat history object to Streamlit session state
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history = [])

    # Display Form Title
    st.title("Chat with Google Gemini-Pro!")

    # Display chat messages from history above current input box
    for message in st.session_state.chat.history:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Accept user's next message, add to context, resubmit context to Gemini
    if prompt := st.chat_input("I possess a well of knowledge. What would you like to know?"):
        # Display user's last message
        st.chat_message("user").markdown(prompt)
        
        # Send user entry to Gemini and read the response
        response = st.session_state.chat.send_message(prompt) 
        
        # Display last 
        with st.chat_message("assistant"):
            st.markdown(response.text)

if option == 'Mistral-7b':
    st.text('hello')



if option == 'MusicGen':

    @st.cache_resource
    def loadmodel(name):
        model = MusicGen.get_pretrained(name)
        return model


    def setparams(model, use_sampling, top_k, top_p, temperature, cfg_coef, duration):
        model.set_generation_params(
            use_sampling=use_sampling,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            cfg_coef=cfg_coef,
            duration=duration)
        return model


    def generate(model, prompt):
        output = model.generate(descriptions=prompt, progress=True)
        return output


    def purge():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
        gc.collect()


    st.title("MG Music Gen")
    st.divider()
    option = st.selectbox('Select a model:', ('small', 'medium', 'melody', 'large'))
    prompt = st.text_input(label='Prompt:', value='90s rock song with loud guitars and heavy drums')
    if st.button("Generate"):
        purge()
        model = loadmodel(option)
        model_ready = setparams(model, use_sampling=True, top_k=250, top_p=0.0, temperature=1.0, cfg_coef=3.0, duration=10)
        purge()
        with st.spinner("Generating..."):
            output = generate(model_ready, prompt)
        with st.spinner("Detaching..."):
            output = output.detach().cpu().float()[0]
        with st.spinner("Normalizing..."):
            wav = normalize_audio(wav=output, sample_rate=32000, strategy="rms")
        with st.spinner("PCM Encoding..."):
            pcm_audio = i16_pcm(wav)
        with st.spinner("Saving..."):
            now = str(time.strftime("%Y%m%d-%H%M%S"))
            filename = now + ".wav"
            torchaudio.save(filename, pcm_audio, sample_rate=32000, encoding="PCM_S", bits_per_sample=16)
        st.write("File " + filename + " created.")
        with st.spinner("Loading..."):
            with open(filename, "rb") as f:
                generation = f.read()
            st.audio(generation)
    purge()

    st.text('hello')

if option == 'stableai':
    st.text('hello')