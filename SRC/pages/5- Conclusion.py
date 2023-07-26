import streamlit as st
import pandas as pd
from PIL import Image

#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Conclusion",
                   page_icon="",  # A CHANGER
                   layout='wide')


# Carrousel
st.markdown("""
<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vT9Vze2Ije6t_-AXciUUqsAgMkfuNuBRRdh-eaZ1Db98zx2lAcrSZBTPy7plrU7JYZyeR7sWUF9JmZN/embed?start=false&loop=false&delayms=3000" frameborder="0" width="1250" height="900" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
""", unsafe_allow_html=True)