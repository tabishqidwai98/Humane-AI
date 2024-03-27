import streamlit as st
from openai import OpenAI
from config import *
import replicate as rp
import os
import requests
import re

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
    st.title("HumaneImagin-E")

    curr_dir = os.path.dirname(__file__)

    st.markdown("<h1 style='color: #A2CFFE; font-family: sans-serif; text-align: center'>Imagin-E</h1>", unsafe_allow_html=True)

    if "user_API_key" in st.session_state:
        st.session_state.user_API_key = None      
    
    st.session_state.user_API_key = st.sidebar.text_input(label="Enter your replicate API key:", type="password")
    os.environ["REPLICATE_API_TOKEN"] = st.session_state.user_API_key
    if st.session_state.user_API_key is not None: 
        if not re.match("^r8_", st.session_state.user_API_key) or not len(st.session_state.user_API_key) > 30:
            st.sidebar.error("Please enter a correct API key. Please check the below link to learn how to get a replicate API key.")   
    st.sidebar.markdown("<h4><a href='https://gist.github.com/MonishSoundarRaj/76d1d6ef9a806d879ef4357ae5111f00'>How to get replicate API key?</a></h4>", unsafe_allow_html=True)

    with st.form("stable_diffusion_parameter_form"):
        st.write("Control Stable Diffusion Model Parameters Here")
        sd_num_inference_steps = st.slider("Adjust the slider for no of denoising steps.", min_value=5, max_value=50, value=50, step=10)
        sd_scheduler_options = st.selectbox("Choose a scheduler.", ["DPMSolverMultistep", "DDIM", "K_EULER", "K_EULER_ANCESTRAL"], index=0)
        sd_seed = st.text_input("Enter a seed (optional) (Leave this 0 for random seed)", 0)
        sd_submit_form = st.form_submit_button("Apply") 
        if sd_submit_form:
            st.success("Applied!")
            if not re.match("^[0-9]+$", sd_seed):
                st.error("Please enter a seed number not a String in a 'Enter a seed' field above.")
                         
        with st.form("Enter_Prompt_form"):
            prompt = st.text_area("Enter Image Generation Prompt")
            prompt_submit = st.form_submit_button("Submit Prompt")
        
        placeholder = st.empty()
        
        placeholder.markdown("<div style='margin: 20px;'><h3 style='text-align: center; padding: 50px'>Image will be displayed here once generated.</h3></div>", unsafe_allow_html=True)
        
        if prompt_submit:
            placeholder.empty()
            model_selected = None
            model_selected = "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4"
            input={"prompt": prompt,"num_inference_steps":sd_num_inference_steps, "scheduler":sd_scheduler_options, **({"seed": int(sd_seed)} if int(sd_seed) > 0 else {})}
            
            if model_selected and input:    
                output = rp.run(
                    model_selected,
                    input = input,
                )

            else:
                st.error("Please enter NSFW prompt, if you think you have entered a NSFW prompt and please reclick on 'Submit Prompt'")
                
            st.success("If you like the generated image download it from the link before changing the parameters.")
            st.image(output)
            st.success(f"You can download the image by going here: {output[0]}")
            '''else:
                st.success("If you like the generated image download it from the link before changing the parameters.")
                if len(output) > 1:
                    for idx, item in enumerate(output):
                        col1, col2 = st.columns(2)
                        col_logic = col1 if idx%2 == 0 else col2
                        with col_logic:
                            st.image(item)
                    print(output)
                else:
                    st.image(output)
                st.success(f"You can download the image by going here: {output}") '''


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