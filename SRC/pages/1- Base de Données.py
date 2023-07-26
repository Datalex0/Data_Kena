import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import bz2
import pickle
import _pickle as cPickle
from PIL import Image
import plotly_express as px


#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Base de Données",
                   page_icon="",  # A CHANGER
                   layout='wide')



#df_pie = pd.read_pickle('df_categorise.pkl')
# Load compressed pickle file
@st.cache_data
def df():
    data = bz2.BZ2File('SRC/df_map_2.pbz2', 'rb')
    data = cPickle.load(data)
    data.reset_index(drop=True, inplace=True)
    return data
df = df()


# RESUME DATABASE
col1, col2, col3 = st.columns([1, 1, 1])
# Afficher l'image dans la deuxième colonne
with col2:
    image = Image.open('SRC/image_database.png')
    st.image(image, width=500)



# CARTE DES REGIONS
carte = df['Region'].value_counts()
df_carte = pd.DataFrame(list(carte.items()), columns=['Region', 'Value'])
# Calculate the total sum of 'Value' column
total_value = df_carte['Value'].sum()
# Calculate the percentage for each region
df_carte['Percentage'] = (df_carte['Value'] / total_value) * 100
# Create a choropleth map using Plotly Express
fig = px.choropleth(df_carte,
                    geojson='https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson',
                    locations='Region',
                    locationmode="geojson-id",
                    featureidkey='properties.nom',
                    color='Percentage',
                    width=2000, height=1000,
                    color_continuous_scale='algae',
                    range_color=(0, 30),
                    projection='mercator',
                    title='Représentation des régions dans le pourcentage total des établissements',
                    hover_name='Region',  # To display region name on hover
                    hover_data={'Percentage': ':.1f%'}, # To display percentage value on hover
                    labels={'Percentage': 'Percentage'},
                    )
# Add label with percent of
fig.add_scattergeo(
    geojson='https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson',
    locations=df_carte['Region'],
    featureidkey='properties.nom',
    text=df_carte["Percentage"].apply(lambda x: f'{x:.1f}%'),
    textposition="top center",
    mode='text',
    locationmode="geojson-id"
)
fig.add_scattergeo(
    geojson='https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson',
    locations=df_carte['Region'],
    featureidkey='properties.nom',
    text=df_carte['Region'],
    textposition="bottom center",
    mode='text',
    locationmode="geojson-id"
)
# Update the layout of the map
fig.update_geos(fitbounds='locations', visible=False)
fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
fig.update_coloraxes(showscale=True)
fig.update_layout(plot_bgcolor = "#232624")
# Update the layout of the map to set the background color to dark
fig.update_geos(bgcolor='rgba(0, 0, 0, 0.5)')  # Set the background color of the map to dark
# Update the layout to set the background color of the entire plot to dark
fig.update_layout(
    paper_bgcolor='rgb(17, 17, 17)',  # Set the background color of the entire plot to dark
    plot_bgcolor='rgb(17, 17, 17)',   # Set the background color of the plot area to dark
    font_color='white',  # Set the font color to white for better visibility on a dark background
)
fig.update_layout(legend=dict(font=dict(size=16)))
# Update the colorbar tick color to make them visible on a dark background
fig.update_coloraxes(colorbar_tickfont_color='white')
fig.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)  # Réglez les valeurs en pixels pour ajuster les marges
)
# Positionner la légende plus près de la carte
fig.update_layout(
    coloraxis=dict(
        colorbar=dict(
            yanchor="top",
            y=0.99,   # Ajustez cette valeur pour rapprocher ou éloigner la légende
            xanchor="left",
            x=0.01   # Ajustez cette valeur pour déplacer la légende horizontalement
        )
    )
)
# Augmenter la taille du titre
fig.update_layout(
    title_font=dict(size=24)  # Définir la taille de la police du titre (ici, 24 points)
)
st.plotly_chart(fig)





# PIECHART CATEGORIES
counts = df['Categorie'].value_counts()
fig2 = px.pie(df, values=counts.values*100/counts.values.sum(), names=counts.index, title='Pourcentage que représente chaque catégorie dans la répartition', hover_name=counts.index, width=1200, height=800, hole=0.5)
fig2.update_traces(textposition='auto', textinfo='percent+label')
fig2.update_traces(pull=[0.2, 0, 0, 0, 0, 0])
fig2.update_layout(title_font=dict(size=16))
fig2.update_layout(legend=dict(font=dict(size=16)))
# Mise à jour du titre de la légende
fig2.update_layout(legend_title='Catégories')
# Augmenter la taille du titre
fig.update_layout(
    title_font=dict(size=24)  # Définir la taille de la police du titre (ici, 24 points)
)
st.plotly_chart(fig2, use_container_width=True)