import streamlit as st 
import replicate as rp
import re
import requests
import os

class HumaneAi:

    def humaneImagine(self, choice):

        self.choice = choice
        #st.title("HumaneImagin-E")

        #curr_dir = os.path.dirname(__file__)

        st.markdown("<h1 style='color: #A2CFFE; font-family: sans-serif;'>HumaneImagin-E</h1>", unsafe_allow_html=True)

        if "user_API_key" in st.session_state:
            st.session_state.user_API_key = None      

        st.session_state.user_API_key = st.sidebar.text_input(label="Enter your replicate API key:", type="password")
        if st.session_state.user_API_key is not None: 
            if not re.match("^r8_", st.session_state.user_API_key) or not len(st.session_state.user_API_key) > 30:
                st.sidebar.error("Please enter a correct API key. Please check the below link to learn how to get a replicate API key.")   
        st.sidebar.markdown("<h4><a href='https://gist.github.com/MonishSoundarRaj/76d1d6ef9a806d879ef4357ae5111f00'>How to get replicate API key?</a></h4>", unsafe_allow_html=True)

        with st.sidebar.form("model_selection_form"):
            st.markdown("<h4 style='text-align: center'>Choose a model from the dropdown to begin</h4>", unsafe_allow_html=True)
            option = st.selectbox("**Select the model you want to use**", (None, "Stable Diffusion", "Anything-v4.0", "Waifu Diffusion", "Vintedios Diffusion"), index=1)
            model_select_button = st.form_submit_button("Select Model")
    
        if model_select_button:
            with st.spinner("Setting Model."):
                st.write(f"Model '{option}' selected.")
            st.toast(f"Model '{option}' has been selected.")

        if option == "Stable Diffusion":
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
                        
        elif option == "Anything-v4.0":
            with st.form("anything_v4_parameter_form"):
                st.write("Control Anything-v4.0 Model Parameters Here")
                at_num_outputs = st.radio("Choose no of images you like to generate", ["1", "4"], index=0)
                at_num_inference_steps = st.slider("Adjust the slider for no of denoising steps.", min_value=5, max_value=20, value=20, step=5)
                at_scheduler_options = st.selectbox("Choose a scheduler.", ["DPMSolverMultistep", "DDIM", "K_EULER", "K_EULER_ANCESTRAL", "PNDM", "KLMS"], index=0)
                at_seed = st.text_input("Enter a seed (optional) (Leave this 0 for random seed)", 0)
                at_submit_form = st.form_submit_button("Apply")
                if at_submit_form:
                    st.success("Applied!")
                    if not re.match("^[0-9]+$", at_seed):
                        st.error("Please enter a seed number not a String in a 'Enter a seed' field above.")
                        
        elif option == "Waifu Diffusion":
            with st.form("waifu_diffusion_parameter_form"):
                st.write("Control Waifu Diffusion Model Parameters Here")
                wd_num_outputs = st.radio("Choose no of images you like to generate", ["1", "4"], index=0)
                wd_num_inference_steps = st.slider("Adjust the slider for no of denoising steps.", min_value=5, max_value=50, value=50, step=10)
                wd_seed = st.text_input("Enter a seed (optional) (Leave this 0 for random seed)", 0)
                wd_submit_form = st.form_submit_button("Apply")
                if wd_submit_form:
                    st.success("Applied!")
                    if not re.match("^[0-9]+$", wd_seed):
                        st.error("Please enter a seed number not a String in a 'Enter a seed' field above.")
                        
        else:
            with st.form("vintedios_diffusion_parameter_form"):
                st.write("Control Vintedios Diffusion Model Parameters Here")
                vd_num_inference_steps = st.slider("Adjust the slider for no of denoising steps.", min_value=5, max_value=50, value=50, step=10)
                vd_scheduler_options = st.selectbox("Choose a scheduler.", ["DPMSolverMultistep", "DDIM", "K_EULER", "K_EULER_ANCESTRAL", "PNDM", "KLMS"], index=0)
                vd_seed = st.text_input("Enter a seed (optional) (Leave this 0 for random seed)", 0)
                vd_submit_form = st.form_submit_button("Apply")
                if vd_submit_form:
                    st.success("Applied!")
                    if not re.match("^[0-9]+$", vd_seed):
                        st.error("Please enter a seed number not a String in a 'Enter a seed' field above.")
                                
        with st.form("Enter_Prompt_form"):
            prompt = st.text_area("Enter Image Generation Prompt")
            prompt_submit = st.form_submit_button("Submit Prompt")

        os.environ["REPLICATE_API_TOKEN"] = "Your_key"
        placeholder = st.empty()

        placeholder.markdown("<div style='margin: 20px;'><h3 style='text-align: center; padding: 50px'>Image will be displayed here once generated.</h3></div>", unsafe_allow_html=True)

        if prompt_submit:
            placeholder.empty()
            model_selected = None
            if option == "Stable Diffusion":
                model_selected = "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4"
                input={"prompt": prompt,"num_inference_steps":sd_num_inference_steps, "scheduler":sd_scheduler_options, **({"seed": int(sd_seed)} if int(sd_seed) > 0 else {})}
            
            elif option == "Anything-v4.0":
                model_selected = "cjwbw/anything-v4.0:42a996d39a96aedc57b2e0aa8105dea39c9c89d9d266caf6bb4327a1c191b061"
                input={"prompt": prompt, "num_outputs":int(at_num_outputs), "num_inference_steps":at_num_inference_steps, "scheduler":at_scheduler_options, **({"seed": int(at_seed)} if int(at_seed) > 0 else {})}
            elif option == "Waifu Diffusion":
                model_selected = "cjwbw/waifu-diffusion:25d2f75ecda0c0bed34c806b7b70319a53a1bccad3ade1a7496524f013f48983"
                input={"prompt": prompt, "num_outputs":int(wd_num_outputs), "num_inference_steps":wd_num_inference_steps, **({"seed": int(wd_seed)} if int(wd_seed) > 0 else {})}
            else:
                model_selected = "22-hours/vintedois-diffusion:28cea91bdfced0e2dc7fda466cc0a46501c0edc84905b2120ea02e0707b967fd"
                input={"prompt": prompt, "num_inference_steps":vd_num_inference_steps, "scheduler":vd_scheduler_options, **({"seed": int(vd_seed)} if int(vd_seed) > 0 else {})}

            if model_selected and input:    
                output = rp.run(
                    model_selected,
                    input = input,
                )

            else:
                st.error("Please enter NSFW prompt, if you think you have entered a NSFW prompt and please reclick on 'Submit Prompt'")
                
            #if output:
            #    st.success("If you like the generated image download it from the link before changing the parameters.")
            #    if len(output) > 1:
            #        for idx, item in enumerate(output):
            #            col1, col2 = st.columns(2)
            #            col_logic = col1 if idx%2 == 0 else col2
            #            with col_logic:
            #                st.image(item)
            #        print(output)
            #    else:
            #        st.image(output)
            #    st.success(f"You can download the image by going here: {output}")"""
            
            return output
