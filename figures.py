import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
from data_read import *

def create_map(df, couleur, label, titre, couleur_continue, mini=0, maxi=None):
    """fonction de création de map"""
    if maxi == None:
        maxi = max(df[couleur])
    map = px.choropleth_mapbox(df, geojson=depart, locations='dep', color=couleur,
                            color_continuous_scale=couleur_continue,
                            range_color=(mini, maxi),
                            labels=label,
                            mapbox_style="carto-positron",
                            zoom=4, center = {"lat": 46.71109, "lon": 1.7191036},
                            opacity=0.8,
                            )

    map.update_layout(title = dict(text=titre,
                                    font = {"size":30},
                                    y=0.97,
                                    x=0.5,
                                    xanchor = 'center',
                                    yanchor  = 'top'),
                    #margin={"r":0,"t":100,"l":1200,"b":0},
                    paper_bgcolor=colors['background'],
                    font_color=colors['text']
                    )
    return map


colors = {
  'background': '#5D6D7E',
  'text' : 'white',
  'PN': '#2874A6',
  'GN': '#A93226'
}




map = create_map(df_empty,'vide',{'vide':"Nombre de crimes commis"},"Répartition des crimes et délits en France","reds",mini=0,maxi=100)

map_p = create_map(df_pop_carte[[2019,'dep']],2019,{"2019":"Nombre d'habitants"},"Répartition de la population française","blues")

map_den = create_map(df_empty,'vide',{'vide':'Nb crimes pour 1000 hbs'},"Densité des crimes et délits en France","purples",mini=0,maxi=10)



hist = px.histogram(df[['année','service',list_crimes[10]]],
                    x='année',
                    y=list_crimes[10],
                    labels = {'année':'Années','y' : 'Somme des '+list_crimes[10]},
                    color='service',
                    barmode='overlay',
                    opacity=0.5,
                    color_discrete_sequence=[colors['GN'],colors['PN']])

hist.update_layout(title = dict(text="Nombre de crimes et délits commis par année",
                                font = {"size":30},
                                y=0.9,
                                x=0.5,
                                xanchor = 'center',
                                yanchor  = 'top'),
                    paper_bgcolor=colors['background'],
                    font_color=colors['text'])

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_pop_0['année'],y=df_pop_0['01']))

fig.update_layout(title = dict(text="Evolution de la population par département",
                                font = {"size":30},
                                y=0.97,
                                x=0.5,
                                xanchor = 'center',
                                yanchor  = 'top'),
                    xaxis_title = 'Année',
                    yaxis_title = 'Population',
                    paper_bgcolor=colors['background'],
                    font_color=colors['text'])
