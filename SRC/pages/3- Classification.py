import streamlit as st
import pandas as pd
import bz2
import pickle
import _pickle as cPickle
import plotly_express as px
from wordcloud import WordCloud
from PIL import Image
import numpy as np

#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Classification",
                   page_icon="",
                   layout='wide')

# Afficher image
image = Image.open('SRC/Algorithme.png')
st.image(image, width=1200)


st.write('')
st.write('***')
st.write('')

# Fonction titre centré
def centered_text(text):
    st.markdown(f"<h3 style='text-align: center;'>{text}</h3>", unsafe_allow_html=True)
centered_text("Nuages de mots représentant les mots qui reviennent le plus")


# Load any compressed pickle file
def decompress_pickle(file):
 data = bz2.BZ2File(file, 'rb')
 data = cPickle.load(data)
 return data


# Diviser l'espace d'affichage en 2 colonnes
col1, col2, col3, col4, col5, col6 = st.columns(6)


# Afficher le premier wordcloud dans la première colonne
with col2:
    text = decompress_pickle('SRC/wordcloud.pbz2')
    # Chargement de l'image bouteille pour créer un masque
    bottle_mask = np.array(Image.open("SRC/france.png"))
    # Création du Wordcloud
    wordcloud = WordCloud(width=300, height=300, max_font_size=300, min_font_size=20, mask=bottle_mask)
    # Génération du wordcloud depuis la liste
    wordcloud.generate_from_frequencies(text)

    # Charger l'image
    image = wordcloud.to_array()

    # Afficher l'image à l'intérieur du conteneur
    st.image(image, use_column_width=False, width=800)
    

st.write('\n')
st.write('***')
st.write('\n')
    
    
    
# Titre centré
st.markdown(f"<h1 style='text-align: center;'>Exploration</h1>", unsafe_allow_html=True)

# Import du Dataframe
def decompress_pickle(file):
 data = bz2.BZ2File(file, 'rb')
 data = cPickle.load(data)
 return data
df_explo = decompress_pickle('SRC/df_explo.pbz2')



# Menu déroulant des REGIONS
liste_regions = df_explo['Région'].unique().tolist()
liste_regions.append(' Toutes')
liste_regions.sort()
region = st.sidebar.selectbox(
'Région', liste_regions, index=liste_regions.index('Occitanie')
)
df_explo = df_explo[
    df_explo.Région.str.contains(region)
    ]
df_explo.reset_index(drop=True, inplace=True)



# Menu déroulant des CATEGORIES
liste_categories = df_explo['Catégorie initiale'].unique().tolist()
liste_categories.append('Toutes')
liste_categories.sort()
categorie = st.sidebar.selectbox(
'Catégorie', liste_categories, index=liste_categories.index('Service pratique')
)
if categorie != 'Toutes':
    df_explo = df_explo[
        df_explo['Catégorie initiale'].str.contains(categorie)
        ]
    df_explo.reset_index(drop=True, inplace=True)


# COMPTEUR %age COMPARAISON DIFFERENTE
col_1, col_2 = st.columns(2)
with col_2 :
    counts = df_explo['Comparaison'].value_counts()
    values=counts.values*100/counts.values.sum()
    col_2.metric(label="Pourcentage de prédictions différentes de l'origine", value=f"{round(values[1],2)} %")

# Menu déroulant des Options de Comparaison
liste_comparaison = ['Tous', 'Identique', 'Différent']
comparaison = st.sidebar.selectbox(
    'Comparaison', liste_comparaison,
)
if comparaison != 'Tous' :
    df_explo = df_explo[
        df_explo['Comparaison'].str.contains(comparaison)
        ]
    df_explo.reset_index(drop=True, inplace=True)    



# Menu déroulant des ETABLISSEMENTS
liste_etablissements = df_explo['Etablissement'].unique().tolist()
liste_etablissements.append(' Tous')
liste_etablissements.sort()
etablissement = st.sidebar.selectbox(
'Etablissement', liste_etablissements, index=0)
if etablissement != ' Tous' :
    df_explo = df_explo[
        df_explo['Etablissement'].str.contains(etablissement)
        ]
    df_explo.reset_index(drop=True, inplace=True) 

# Fonction pour appliquer le style rouge aux cases
def mettre_en_rouge(valeur):
    return 'color: red' if valeur == 'Différent' else 'color: green'

# Appliquer le style rouge aux cases de la colonne 'Score'
df_explo = df_explo.style.applymap(mettre_en_rouge, subset=['Comparaison'])



st.dataframe(df_explo)