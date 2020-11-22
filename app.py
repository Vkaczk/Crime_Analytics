import pandas as pd
import plotly_express as px
import plotly.graph_objects as go

import os.path
import re

from navbar import Navbar
from data_read import *
from figures import *


from urllib.request import urlopen
import numpy as np
import json
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


######################  APP  #######################


app = dash.Dash(__name__,title='Crimes Analytics',external_stylesheets=[dbc.themes.BOOTSTRAP]) # (3)


###################### LAYOUT ######################


app.layout = html.Div(style={'backgroundColor': colors['background']},
                    children=[
                        html.Div(Navbar()),
                        html.Div(
                            className='app-header--title',
                            children=[
                                html.H1(className="app-header--title",
                                    id = 'title',
                                    children=f'Crimes et Délits en France en {year}',
                                    style={'textAlign': 'center'}
                                    ),
                                ],
                            style={'marginTop':'50px'}
                        ),
                        html.Div(
                            children=[
                                dbc.Row(
                                        dbc.Col(
                                                html.Div(
                                                        dcc.Slider(
                                                            id="year_slider",
                                                            min = 2012,
                                                            max = 2019,
                                                            step = 1,
                                                            marks = { str(year) : {'label':str(year),'style':{'color':colors['text']}} for year in range(2012,2020)},
                                                            value=2019,
                                                            ), style={'marginTop':'25px'}
                                                        ),width=11
                                                ),justify='center'
                                        ),
                                dbc.Row([
                                        dbc.Col([dbc.Row([
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card([
                                                        dbc.CardHeader("Choix des infractions"),
                                                        dbc.CardBody([
                                                            dbc.RadioItems(
                                                                id='id_radioItems',
                                                                options=[
                                                                    {'label':'Selection libre','value':'libre'},
                                                                    {'label':'Toutes les infractions','value':'total'},
                                                                    {'label':'Ensemble des vols','value':'vols'},
                                                                    {'label':"Infractions liées à l'insécurité",'value':'securite'},
                                                                ],
                                                                value='libre'
                                                            )
                                                        ])
                                                    ],color="dark")
                                                ])
                                            ],align='top'),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card([
                                                        dbc.CardHeader("Organisme"),
                                                        dbc.CardBody(
                                                            [
                                                                #dbc.Label("Organisme :"),
                                                                dbc.Checklist(
                                                                    id = "id_chekclist",
                                                                        options=[
                                                                            {'label': 'Police Nationale', 'value': 'PN'},
                                                                            {'label': 'Gendarmerie Nationale', 'value': 'GN'},
                                                                        ],
                                                                        value=['PN', 'GN'],
                                                                )
                                                            ]
                                                        )
                                                    ],color="dark")
                                                ]),
                                                dbc.Row([
                                                    html.Div(dbc.Button("Play", color="dark", className="mr-1", id='play_button'),style={'marginTop':'10px','marginRight' : '3%','marginLeft' : '1%'}),
                                                    html.Div(dbc.Button("Pause", color="dark", className="mr-1", id='pause_button'),style={'marginTop':'10px'}),
                                                ]
                                                ,justify='center',align='center'),
                                            ]),

                                                ],justify='center',),

                                                #dbc.Row([
                                                #    html.Div(dbc.Button("Play", color="dark", className="mr-1", id='play_button'),style={'marginTop':'10px','marginRight' : '3%','marginLeft' : '1%'}),
                                                #    html.Div(dbc.Button("Pause", color="dark", className="mr-1", id='pause_button'),style={'marginTop':'10px'}),
                                                #]
                                                #,justify='end',align='center'),
                                        ],width=4,align='center'),

                                        dbc.Col(
                                                html.Div([
                                                        dbc.Tabs([
                                                            dbc.Tab(
                                                                dcc.Graph(
                                                                    id='map_den',
                                                                    figure=map_den,
                                                                    #style={'marginLeft': '55%',"display": "block", "width": "40%"}
                                                                ),label = "Densité de crimes",
                                                            ),
                                                            dbc.Tab(
                                                                dcc.Graph(
                                                                    id='map',
                                                                    figure=map,
                                                                    #style={'marginLeft': '55%',"display": "block", "width": "40%"}
                                                                ), label="Nombre de crimes",
                                                            ),
                                                            dbc.Tab(
                                                                dcc.Graph(
                                                                    id='map_pop',
                                                                    figure=map_p,
                                                                    #style={'marginLeft': '55%',"display": "block", "width": "40%"}
                                                                ),label = "Population par département",
                                                            ),
                                                        ])
                                                ]), width=6
                                        )
                                    ],justify="end",style={'marginTop':'2%','marginRight':'5%','align':'center', 'color':colors['text']},),

                            ]
                        ),

                        html.Div(
                            [
                                dbc.Row(
                                        dbc.Col(
                                                html.Div(
                                                        dcc.Dropdown(
                                                            id='crime_dropdown',
                                                            options=[
                                                                {'label': x, 'value' : x } for x in list_crimes
                                                            ],
                                                            value=[],
                                                            multi = True,
                                                            disabled=True,
                                                            placeholder="Choisissez une infraction",
                                                            #style={"display": "block", "width": "80%"}
                                                    )
                                                ),width=11
                                        ),justify='center'
                                ),
                                dbc.Row(
                                        dbc.Col(
                                                html.Div(
                                                        dcc.Graph(
                                                                id='histo',
                                                                figure=hist,
                                                                #style={'marginRight': '30%',"display": "block", "width": "60%"}
                                                            ),style={'marginTop':'35px','marginLeft':'5%'}
                                                        ), width=8
                                                ),
                                        )


                            ]
                        ),
                        html.Div(
                            [
                                dbc.Row([
                                    dbc.Col(
                                        html.Div(
                                            dcc.Dropdown(
                                                id='dep_dropdown',
                                                options=get_dep_dropdown(df_dep),
                                                value=['F'],
                                                multi = True,
                                                placeholder="Choisissez une zone",
                                                ),
                                            style={'marginTop':'25%'}
                                            ),width=3, align='start'
                                    ),
                                    dbc.Col(
                                        dcc.Graph(
                                            id='fig_pop',
                                            figure=fig
                                        ),width=8, align='center'
                                    ),
                                ],justify='center')
                            ]
                        ),
                        dcc.Interval(   id='interval',
                                        interval=5*1000, # in milliseconds
                                        n_intervals=6,
                                        disabled=False),
                    ]
                )


###################### CALLBACKS ######################


@app.callback(
        Output('histo','figure'),
        [Input('crime_dropdown', 'value')]
)

def update_histo(crime_dropdown):
    """renvoie un histogramme vide si rien n'est sélectionné,
    l'histogramme pour un crime si un seul crime selectionné,
    l'histogramme de la somme des crimes sinon"""
    if len(crime_dropdown) == 0:
        df_histo = get_dataframe('empty')
        crime = 'vide'
        y_label = {'année':'Année','vide' : 'nothing'}

    elif len(crime_dropdown) == 1:
        df_histo = get_dataframe()[['année','service',crime_dropdown[0]]]
        crime = crime_dropdown[0]
        y_label = {'année':'Année'}

    else:
        df_histo = get_dataframe()[['année','service']]
        df_histo['crimes'] = get_dataframe()[crime_dropdown].sum(axis = 1)
        crime = 'crimes'
        y_label = {'année':'Année'}

    histo = px.histogram(df_histo,
                        x='année',
                        y=crime,
                        labels = y_label,
                        barmode='overlay',
                        color='service',
                        opacity=0.5,
                        color_discrete_sequence=[colors['GN'],colors['PN']])

    histo.update_layout(title = dict(text="Nombre de crimes et délits commis par année",
                                    font = {"size":30},
                                    y=0.97,
                                    x=0.5,
                                    xanchor = 'center',
                                    yanchor  = 'top'),
                        paper_bgcolor=colors['background'],
                        font_color=colors['text'])

    return histo


@app.callback(
        [Output('map','figure'),
        Output('map_den','figure'),
        Output('title','children')],
        [Input('crime_dropdown', 'value'),
        Input('year_slider','value'),
        Input('id_chekclist','value')]
)



def update_map(crime_dropdown,year_slider,id_chekclist):

    """Mise à jour des map de densité de crimes et nombre de crimes,
    renvoie une map vide si aucun crime selectionné ou aucun service selectionné,
    renvoir la somme des crimes selectionnés sinon"""

    def test_crime_dropdown():
        if len(crime_dropdown) == 1:
            crime = crime_dropdown[0]
        else:
            df_map['Somme des crimes'] = df_map[crime_dropdown].sum(axis=1)
            df_den['Somme des crimes'] = df_den[crime_dropdown].sum(axis=1)
            crime = 'Somme des crimes'
        return crime

    if len(crime_dropdown) == 0 or len(id_chekclist) == 0:
        df_map = get_dataframe('empty')
        df_den = get_dataframe('empty')
        crime = 'vide'
        maxi=100
        maxi_den=10

    elif len(id_chekclist) == 1:
        df_map = get_dataframe(id_chekclist[0]).groupby(['dep','année']).sum().filter(like=str(year_slider), axis=0)
        df_map['dep'] = list(df_map.index.get_level_values('dep'))
        df_den = get_dataframe_den(id_chekclist[0]).groupby(['dep','annee']).sum().filter(like=str(year_slider), axis=0)
        df_den['dep'] = list(df_den.index.get_level_values('dep'))
        crime = test_crime_dropdown()
        maxi = df_map[crime].max()
        maxi_den = df_den[crime].max()
        if maxi == 0:
            maxi = 100
            maxi_den = 100

    elif len(id_chekclist) == 2:
        df_map = get_dataframe().groupby(['dep','année']).sum().filter(like=str(year_slider), axis=0)
        df_map['dep'] = list(df_map.index.get_level_values('dep'))
        df_den = get_dataframe_den().groupby(['dep','annee']).sum().filter(like=str(year_slider), axis=0)
        df_den['dep'] = list(df_den.index.get_level_values('dep'))
        crime = test_crime_dropdown()
        maxi = df_map[crime].max()
        maxi_den = df_den[crime].max()
        if maxi == 0:
            maxi = 100
            maxi_den = 100

    map = create_map(df_map,crime,{crime:'Nombre de crimes commis','dep':'Département '},"Répartition des crimes et délits en France","reds",maxi=maxi)

    map_den = create_map(df_den,crime,{crime:'Nb crimes pour 1000 hbs'},"Densité des crimes et délits en France","purples",maxi=maxi_den)


    return [map,
            map_den,
            f'Crimes et Délits en France en {year_slider}']


@app.callback(Output('year_slider', 'value'),
            [Input('interval', 'n_intervals')])

def on_tick(n_intervals):
    """permet l'annimation"""
    years=[k for k in range(2012,2020)]
    if n_intervals is None: return 0
    return years[(n_intervals+1)%len(years)]

@app.callback(Output('interval', 'disabled'),
              [Input('play_button', 'n_clicks'),
               Input('pause_button', 'n_clicks')])

def play_pause(btn1, btn2):
    """calbalck des boutons play et pause"""
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'play_button' in changed_id:
        return False
    elif 'pause_button' in changed_id:
        return True
    else:
        return True

@app.callback(Output('fig_pop','figure'),
            [Input('dep_dropdown','value')])


def update_figure(dep_dropdown):
    """retourne les courbes de l'évolution de la population française"""
    fig = go.Figure()
    if len(dep_dropdown) == 0:
        df_pop = df_pop_0[['année']]
        df_pop['vide'] = [np.NaN for k in range(df_pop_0.shape[0])]
        deps = 'vide'
        fig.add_trace(go.Scatter(x=df_pop['année'],y=df_pop[deps]))
    else:
        fig.add_trace(go.Scatter(x=df_pop_0['année'],y=df_pop_0[dep_dropdown[0]],name=get_dep_dict(df_dep)[dep_dropdown[0]]))
        if len(dep_dropdown)>1:
            for departement in dep_dropdown[1:]:
                fig.add_trace(go.Scatter(x=df_pop_0['année'],y=df_pop_0[departement],name=get_dep_dict(df_dep)[departement]))

    fig.update_layout(title = dict(text="Evolution de la population par département",
                                    font = {"size":30},
                                    y=0.9,
                                    x=0.5,
                                    xanchor = 'center',
                                    yanchor  = 'top'),
                        xaxis_title="Année",
                        yaxis_title='Population',
                        paper_bgcolor=colors['background'],
                        font_color=colors['text'])

    return fig


@app.callback(Output('map_pop','figure'),
            [Input('year_slider','value')])

def map_pop_update(year_slider):
    """renvoie la carte de la population par département en fonction de l'année """
    map_p = create_map(df_pop_carte[[year_slider,'dep']],year_slider,{str(year_slider):"Nombre d'habitants"},"Répartition de la population française",'blues',maxi=3000000)
    return map_p

@app.callback([Output('crime_dropdown','value'),
            Output('crime_dropdown','disabled')],
            [Input('id_radioItems','value')])

def radio_items_update(id_radioItems):
    """choix des ensembles de crimes ou selection libre """
    if id_radioItems == 'libre':
        bool = False
        crime_selection = []
    elif id_radioItems == 'vols':
        bool = True
        crime_selection = [crime for crime in list_crimes if re.search(r'vols', crime.lower()) and not re.search(r'homicides', crime.lower())]
    elif id_radioItems == 'total':
        bool = True
        crime_selection = list_crimes
    elif id_radioItems == 'securite':
        bool = True
        crime_selection = [crime for crime in list_crimes
                        if (re.search(r'vols', crime.lower()) and not (re.search(r'homicides', crime.lower()) or re.search(r'agricoles', crime.lower()) or re.search(r'frêt', crime.lower()) or re.search(r'chantier', crime.lower())))
                        or re.search(r'dégradations', crime.lower())
                        or re.search(r'coups', crime.lower())
                        or (re.search(r'homicides', crime.lower())  and not (re.search(r'15', crime.lower()) or re.search(r'mineur(e)s',crime.lower())))
                        or (re.search(r'viols', crime.lower()) and not re.search(r'mineur(e)s', crime.lower()))]
    return crime_selection, bool
