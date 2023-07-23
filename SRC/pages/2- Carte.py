import streamlit as st
import pandas as pd
#from geopy.geocoders import Nominatim
#from geopy.extra.rate_limiter import RateLimiter
import time
#import plotly.express as px
import base64
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
# imports pickle
import bz2
import pickle
import _pickle as cPickle

#df = pd.read_csv

#df_map = cPickle.load(bz2.BZ2File('df_map.pbz2', 'rb'))  # CHANGER LE NOM DU FICHIER
# df = cPickle.load(df)
# df = pd.read_pickle('C:/Users/murai/OneDrive/Bureau/DATA/PROJET 3/code/df_ML.pkl')

# # Load any compressed pickle file
@st.cache_data
def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data
df_map = decompress_pickle('df_map.pbz2')


# Titre
titre = '''<p style="font-family:sans-serif  ; font-size: 20px;">Carte des établissements</p>'''
st.markdown(titre, unsafe_allow_html=True)

# # Menu déroulant des REGIONS
# liste_regions =[
# 'Auvergne-Rhône-Alpes',
#  'Bourgogne-Franche-Comté',
#  'Bretagne',
#  'Centre-Val de Loire',
#  'Corse',
#  'Grand Est',
#  'Hauts-de-FranceNormandie',
#  'Ile-de-France',
#  'Nouvelle-Aquitaine',
#  'Occitanie',
#  'Pays de la Loire',
#  "Provence-Alpes-Côte d'Azur"
# ]
# region = st.sidebar.selectbox(
# 'Région', liste_regions
# )

# Menu déroulant des REGIONS
liste_regions = df_map['Region'].unique().tolist()
liste_regions.sort()
region = st.sidebar.selectbox(
'Région', liste_regions
)

df_map = df_map[
    df_map.Region.str.contains(region)
    ]
df_map.reset_index(drop=True, inplace=True)


# Menu déroulant des DEPARTEMENTS
# liste_depts =['Ain',
#  'Aisne',
#  'Allier',
#  'Alpes-Maritimes',
#  'Alpes-de-Haute-Provence',
#  'Ardennes',
#  'Ardèche',
#  'Ariège',
#  'Aube',
#  'Aude',
#  'Aveyron',
#  'Bas-Rhin',
#  'Bouches-du-Rhône',
#  'Calvados',
#  'Cantal',
#  'Charente',
#  'Charente-Maritime',
#  'Cher',
#  'Corrèze',
#  'Corse-du-Sud',
#  'Creuse',
#  "Côte-d'Or",
#  "Côtes-d'Armor",
#  'Deux-Sèvres',
#  'Dordogne',
#  'Doubs',
#  'Drôme',
#  'Essonne',
#  'Eure',
#  'Eure-et-Loir',
#  'Finistère',
#  'Gard',
#  'Gers',
#  'Gironde',
#  'Haut-Rhin',
#  'Haute-Corse',
#  'Haute-Garonne',
#  'Haute-Loire',
#  'Haute-Marne',
#  'Haute-Savoie',
#  'Haute-Saône',
#  'Haute-Vienne',
#  'Hautes-Alpes',
#  'Hautes-Pyrénées',
#  'Hauts-de-Seine',
#  'Hérault',
#  'Ille-et-Vilaine',
#  'Indre',
#  'Indre-et-Loire',
#  'Isère',
#  'Jura',
#  'Landes',
#  'Loir-et-Cher',
#  'Loire',
#  'Loire-Atlantique',
#  'Loiret',
#  'Lot',
#  'Lot-et-Garonne',
#  'Lozère',
#  'Maine-et-Loire',
#  'Manche',
#  'Marne',
#  'Mayenne',
#  'Meurthe-et-Moselle',
#  'Meuse',
#  'Morbihan',
#  'Moselle',
#  'Nièvre',
#  'Nord',
#  'Oise',
#  'Orne',
#  'Paris',
#  'Pas-de-Calais',
#  'Puy-de-Dôme',
#  'Pyrénées-Atlantiques',
#  'Pyrénées-Orientales',
#  'Rhône',
#  'Sarthe',
#  'Savoie',
#  'Saône-et-Loire',
#  'Seine-Maritime',
#  'Seine-Saint-Denis',
#  'Seine-et-Marne',
#  'Somme',
#  'Tarn',
#  'Tarn-et-Garonne',
#  'Territoire de Belfort',
#  "Val-d'Oise",
#  'Val-de-Marne',
#  'Var',
#  'Vaucluse',
#  'Vendée',
#  'Vienne',
#  'Vosges',
#  'Yonne',
#  'Yvelines'
# ]
liste_dpts = df_map['Département'].unique().tolist()
liste_dpts.sort()
departement = st.sidebar.selectbox(
'Département', liste_dpts
)

df_map = df_map[
    df_map.Département.str.contains(departement)
    ]
df_map.reset_index(drop=True, inplace=True)

# Menu déroulant des CATEGORIES
# liste_categories =[
#                 'Hébergement',
#                 'Restauration',
#                 'Site Sportif ou de Loisirs',
#                 "Site Culturel",
#                 'Commerce de détail',
#                 'Fournisseur de Dégustation',
#                 "Prestataire d'activité",
#                 'Site Naturel'
#                 'Service Pratique',
#                 'Prestataire de Services',
#                 "Service d'Information Touristique",
#                 'Service de Santé',
#                 'Transport',
#                 "Site d'Affaires"
#                 ]
liste_categories = df_map['Categorie'].unique().tolist()
liste_categories.sort()
categorie = st.sidebar.selectbox(
'Catégorie', liste_categories
)

# Lire le contenu du fichier m.html
# with open("m.html", "r", encoding="utf-8") as file:
#     df_map = file.read()


# @st.cache_data
# def new_df_map(df) :
df_map = df_map[
    df_map.Categorie.str.contains(categorie)
    ]
df_map.reset_index(drop=True, inplace=True)
#df_map = new_df_map(df_map)

# Afficher la carte dans votre application Streamlit
#st.components.v1.html(df_map, width=1000, height=1000)

# ***** MAP *****
#@st.cache_data
#def centrer(df):
# total_lat = 0
# total_lon = 0
# for lat, lon in df_map['location']:
#     total_lat += float(lat)
#     total_lon += float(lon)
# centre_lat = total_lat / len(df_map)
# centre_lon = total_lon / len(df_map)
# centre = [centre_lat, centre_lon]
#    return centre
#centre=centrer(df_map)

m = folium.Map(location=[df_map['latitude'].mean(), df_map['longitude'].mean()],zoom_start=9, tiles="CartoDB positron")

for i in range(len(df_map)):
    html=f"""
       <h3 align=center> {df_map.iloc[i]['label']}</h3>
       <p></p>
       <ul>
           <li>{df_map.iloc[i]['Categorie']}</li>
           <br>
           <li><u>Contacts</u></li>
           Tél : {df_map.iloc[i]['Téléphone']}
           <br>
           Mail : {df_map.iloc[i]['E-mail']}
           <br><br>
           <li><u>Adresse</u></li>
           {df_map.iloc[i]['Adresse']}
           <br>
           {df_map.iloc[i]['Code_Postale']} {df_map.iloc[i]['Ville']}
           <br>
           {df_map.iloc[i]['Département']}
           <br><br>
           <li><a href={df_map.iloc[i]['Site_web'][0]}>Site web</a></li>
           <br><br>
           {df_map.iloc[i]['Description']}
       </ul>
       </p>
       """
    iframe = folium.IFrame(html=html, width=300, height=500)
    popup = folium.Popup(iframe, max_width=2650)

    folium.Marker(location=df_map['location'][i],
    popup=popup,
    tooltip = df_map['label'][i]+" - "+df_map['Adresse'][i]+" "+df_map['Code_Postale'][i]+" "+df_map['Ville'][i],
    #icon=folium.Icon(color="red", icon="exclamation-sign")  # = Point d'exclamation rouge
    #icon=folium.Icon(color="darkred", icon="home", prefix="fa")      = maison rouge

    # icon=folium.Icon(color="white",icon_color="red", icon="table-picnic", prefix="fa")
    # icon=folium.Icon(color="white",icon_color="red", icon="volleyball", prefix="fa")
    icon = folium.CustomIcon(f"icones/{categorie}.png", icon_size=(60, 60))
    ).add_to(m)



# Taille de la map + zoom
st_data = st_folium(m, width=1000)
# st_data



# @st.cache_data()
# def get_map():
#   HtmlFile = open("m.html", 'r', encoding='utf-8')
#   bcn_map_html = HtmlFile.read()
#   return bcn_map_html

# bcn_map_html = get_map()
# import streamlit.components.v1 as components

# with st.container():
#   components.html(bcn_map_html,width=1000, height=1000)


