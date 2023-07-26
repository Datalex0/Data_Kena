import streamlit as st
import pandas as pd
from PIL import Image

#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Notre Mission",
                   page_icon="",  # A CHANGER
                   layout='wide')

#Importation image accueil
# image = Image.open('logo.png')
# st.image(image)

# Initialisation du fond d'écran
import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
#add_bg_from_local('logo.png')

# Carrousel
st.markdown("""
<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vRq5B5Fchy4RYjf-5pSMPPBqbINVkUAWXw_yX068b5l_0z5kVxfnD2acjQdZNrsLgq4Ar-2qRPzapBR/embed?start=false&loop=false&delayms=3000" width="1250" height="900"></iframe>
""", unsafe_allow_html=True)