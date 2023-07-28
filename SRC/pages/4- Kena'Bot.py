import streamlit as st
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.linear_model import LogisticRegression
import sklearn.externals as extjoblib
import joblib
import time
from PIL import Image

#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Kena'Bot",
                   page_icon="",  # A CHANGER
                   layout='wide')

# Loader la vectorisation
@st.cache_data(show_spinner=False)
def vectorization ():
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open("SRC/feature.pkl", "rb")))

    return loaded_vec

# Loader le model entrainé
@st.cache_data(show_spinner=False)
def lr_fitted():
    loaded_model = joblib.load("SRC/lr_trained.joblib")
    return loaded_model

# Afficher image
image = Image.open('SRC/Kenabot.png')
st.image(image, width=1200)

st.markdown('')
st.markdown('***')
st.markdown('')

st.title("Besoin d'un coup de pouce ? :thumbsup:", anchor=None,help=None)
st.markdown("""""")
st.markdown("""""")
st.markdown("Un doute sur la classification, sur les coordonnées géographiques ?")
st.markdown("Votre assistant virtuel est là pour vous aider.")
st.markdown("""""")
st.markdown("""""")


message = st.chat_message("assistant")
message.write("Hello ! Enchanté, je suis Kena'Bot ! :wave:")
message.write("Comment puis-je t'aider aujourd'hui?")

# Liste des options disponibles
options = ["J\'ai besoin de tes conseils pour une classification", "J'ai un doute sur des coordonnées géographiques", "J\'ai une autre question", "Rien, juste te dire bonjour",]

# Liste pour stocker les options sélectionnées
selected_options = []

st.write("Choisi parmi les options suivantes :")
choice = st.radio(label = "", options = options, label_visibility='collapsed', index = 3)

response = ""
response0 = ""
response2 = ""
prompt=""
response3 = ""
if 'Rien, juste te dire bonjour' == choice:
    response = "Chouette, bonjour à toi :wave:! "
if 'J\'ai besoin de tes conseils pour une classification' == choice:
    response0 = "Ca marche, allons-y ! :smiley:"
    response2 = "Quelle est la description de l'établissement ?"
if "J'ai un doute sur des coordonnées géographiques" == choice : 
    response = "Allons vérifier ça !"
if "J\'ai une autre question" == choice :
    response = "Bientôt tu pourras retrouver de nouvelles fonctionalités ! "

# Afficher le message final
if response:
    message = st.chat_message("assistant")
    message.write(response)
if response0:
    message = st.chat_message("assistant")
    message.write(response0)
if response2 :
    time.sleep(0.5)
    message.write(response2)
    prompt = st.chat_input("Ecris la description ici")
    st.caption("Exemple de description : Le 'Logis Hôtel la Bonne Auberge' dans la Creuse :")
    st.caption("Situé en pleine campagne, cet hôtel simple se trouve à 14 km du château de Boussac et à 23 km de la route nationale N145. Dotées de murs aux touches colorées, les chambres à l'atmosphère détendue disposent du Wi-Fi gratuit et d'une télévision à écran plat. Celles de catégorie supérieure comprennent en outre un lit à baldaquin. Les suites sont pourvues de chambres communicantes. L'établissement possède un restaurant convivial doté de poutres apparentes au plafond et d'une terrasse. Il comporte également un jardin et un espace de réunion. Le petit-déjeuner est payant.")
if prompt :
    moi = st.chat_message("user")
    moi.write("Voilà la description")
    moi.write(prompt)
    loaded_vec = vectorization()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(loaded_vec.fit_transform(np.array([prompt])))
    lr = lr_fitted()
    categorie_df = lr.predict(tfidf)[0]
    # Transformer le nom de la categorie 
    trad = {
    'Hebergement':'Hébergement',
    'Site_sportif_récréatif_de_loisirs':'Site Sportif ou de Loisirs',
    'Site_culturel':'Site Culturel',
    'Commerce_detail':'Commerce de détail',
    'Fournisseur_degustation':'Fournisseur de Dégustation',
    'Prestataire_activite':"Prestataire d'activité",
    'Site_naturel':'Site Naturel',
    'Service_pratique':'Service pratique',
    'Prestataire_service':'Prestataire de Services',
    'Service_information_touristique':"Service d'Information Touristique",
    'Sante':'Service de Santé',
    'Site_affaire':"Site d'Affaires",
    'Transport':'Transport',
    'Restauration':'Restauration'}
    
    categorie = trad[categorie_df]
    proba_categorie_principale=lr.predict_proba(tfidf)
    #Trouver le % de probabilité de prédiction de la catégorie principale
    liste_proba_cat_principal = []
    for array in range (len(proba_categorie_principale)) :
        liste_proba_cat_principal.append(f"{round(proba_categorie_principale[array].max()*100,2)} %")
    pourcent = liste_proba_cat_principal[0]
    # Trouver catégorie secondaire
    liste_classification = ['Commerce de detail', 'Fournisseur de degustation', 'Hébergement', 'Prestataire d\'activite', 'Prestataire de service', 'Restauration', 'Santé', 'Service d\'information touristique', 'Service pratique', 'Site d\'affaire', 'Site culturel', 'Site naturel', 'Site sportif récréatif de loisirs', 'Transport']
    seconde_categorie = []
    probabilite_seconde_categorie = []
    probabilite = lr.predict_proba(tfidf)

    for array in range (len(probabilite)) : 
        array_reference = probabilite[array]
        id_max = array_reference.argmax()
        array_reference[id_max]= 0
        id_max2 = array_reference.argmax()
        probabilite2 = array_reference[id_max2]
        probabilite_seconde_categorie.append(f"{round(probabilite2*100, 2)} %")
        seconde_categorie.append(liste_classification[id_max2])
    
    
    message = st.chat_message("assistant")
    time.sleep(1)
    message.write(f"Selon cette description, nous estimons à {pourcent} que cet établissement se trouve principalement dans la catégorie {categorie}. La catégorie secondaire serait {seconde_categorie[0]} à {probabilite_seconde_categorie[0]}")
    
