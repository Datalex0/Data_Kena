import streamlit as st
import pandas as pd
#import time
#import base64
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import bz2
import pickle
import _pickle as cPickle
from PIL import Image

#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Tableau de Bord",
                   page_icon="",  # A CHANGER
                   layout='wide')

# Afficher image
image = Image.open('SRC/Carte Interactive.png')
st.image(image, width=1250)

# Load compressed pickle file
@st.cache_data
def map():
    data = bz2.BZ2File('SRC/df_map.pbz2', 'rb')
    data = cPickle.load(data)
    #data=data[
    #data['Region']=='Pays de la Loire'
    #          ]
    data.reset_index(drop=True, inplace=True)
    return data
df_map =map()
#df_map.drop(index=([361891, 28505, 135648, 291799, 26102, 28505, 48517, 96645, 113905, 135648, 235967, 242666, 294238]), inplace=True)

# Titre
# titre = '''<p style="font-family:sans-serif  ; font-size: 20px;">Carte des établissements</p>'''
# st.markdown(titre, unsafe_allow_html=True)

st.write('')
st.write('***')
st.write('')

# Menu déroulant des REGIONS
liste_regions = df_map['Region'].unique().tolist()
liste_regions.sort()
region = st.sidebar.selectbox(
'Région', liste_regions, index=liste_regions.index('Pays de la Loire')
)
df_map = df_map[
    df_map.Region.str.contains(region)
    ]
df_map.reset_index(drop=True, inplace=True)


# Menu déroulant des DEPARTEMENTS
liste_dpts = df_map['Département'].unique().tolist()
liste_dpts.sort()
departement = st.sidebar.selectbox(
'Département', liste_dpts #, index=liste_dpts.index('Loire-Atlantique'), 
)
df_map = df_map[
    df_map['Département'].str.contains(departement)
    ]
df_map.reset_index(drop=True, inplace=True)



# Menu déroulant des CATEGORIES
liste_categories = df_map['Categorie'].unique().tolist()
liste_categories.sort()
categorie = st.sidebar.selectbox(
'Catégorie', liste_categories, index=liste_categories.index('Site Culturel')
)
df_map = df_map[
    df_map.Categorie.str.contains(categorie)
    ]
df_map.reset_index(drop=True, inplace=True)



# Menu déroulant des ETABLISSEMENTS
liste_etablissements = df_map['label'].unique().tolist()
liste_etablissements.append(' Tous')
liste_etablissements.sort()
etablissement = st.sidebar.selectbox(
'Etablissement', liste_etablissements, index=0)


# Initialisation Map
fig = folium.Figure(width=800, height=600)
if etablissement!=' Tous' :
    lat = df_map[
        df_map['label']==etablissement
        ]['latitude'].values[0]
    lon = df_map[
    df_map['label']==etablissement
        ]['longitude'].values[0]
    zoom=15
else:
    lat = df_map['latitude'][0]
    lon = df_map['longitude'][0]
    zoom=9

m = folium.Map(location=[lat, lon], zoom_start=zoom) #, tiles="CartoDB positron")

# Initialisation Clusters
cluster_poi = MarkerCluster(name='POI')

# Initialisation des Markers
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
    icon = folium.CustomIcon(f"SRC/icones/{categorie}.png", icon_size=(60, 60))
    ).add_to(cluster_poi)


cluster_poi.add_to(m)
fig.add_child(m)
#folium_static(fig)
st_folium(fig)
