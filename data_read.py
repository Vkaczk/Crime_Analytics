import pandas as pd
import numpy as np
import plotly_express as px
import json
import plotly
import plotly.graph_objs as go
import os
from urllib.request import urlopen
from sklearn.linear_model import LinearRegression
import re



def open_dataframe(year, service):
    '''Permet l'ouverture d'une feuille excel depuis data.gouv.fr si data/ est vide
     puis crée un dataframe à partir de cette feuille'''
    #Ouverture de la page demandée
    if service == 'PN':
        data = pd.read_excel('https://static.data.gouv.fr/resources/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012/20200129-181725/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012.xlsx',sheet_name = 'Services '+ service+ ' ' + str(year),index_col=None).drop(columns=['Année '+str(year)+' - services de police'])
    else:
        data = pd.read_excel('https://static.data.gouv.fr/resources/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012/20200129-181725/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012.xlsx',sheet_name = 'Services '+ service+ ' ' + str(year),index_col=None).drop(columns=['Année '+str(year)+' - compagnies de gendarmerie'])

    #On transpose le tableau et on renomme les colonnes
    data = data.transpose()
    new_header = data.iloc[0]   #On retire la première ligne pour les colonnes
    df = data[1:]
    df.columns = new_header

    # Rajout des colonnes département, année et service
    df['dep'] = df.index
    df['dep'] = df['dep'].apply(lambda n: n.split('.')[0])
    df['année'] = [year for k in range(df.shape[0])]
    df['service'] = [service for k in range(df.shape[0])]
    if service == 'PN':
        df = df.drop('Périmètres',axis='columns')
        df = df.rename(columns={'Libellé index \ CSP':'Libellé'})
    else:
        df = df.rename(columns={'Libellé index \ CGD':'Libellé'})
    df.index = range(0,df.shape[0])

    return df


def build_dataframes():
    """Ouvre toutes les feuilles excels du fichier source via open_dataframe()
    puis les concatène en deux dataframes (GN et PN) puis les sauvegarde en csv"""
    if len(os.listdir('data')) == 0:
        print("Ouverture des données, ne faites pas attention aux warnings")
        list_df_gn = []
        list_df_pn = []
        for year in range(2012,2020):
            print("Ouverture de l'année: ",year)
            list_df_gn.append(open_dataframe(year, 'GN'))
            df1 = open_dataframe(year, 'GN')
            df2 = open_dataframe(year, 'PN')
            list_df_gn.append(df1)
            list_df_pn.append(df2)
        df_gn = pd.concat(list_df_gn)
        df_pn = pd.concat(list_df_pn)
        df_gn = df_gn.reset_index()
        df_pn = df_pn.reset_index()
        df_gn.to_csv('data/crimes_GN.csv',index=False,encoding='utf-8')
        df_pn.to_csv('data/crimes_PN.csv',index=False,encoding='utf-8')


def open_csv(csv):
    """Ouvre les csv en utf-8 et suprimme les colonnes vides"""
    df = pd.read_csv(csv,encoding='utf-8')
    df = df.drop(['Index non utilisé'],axis='columns')
    df = df.drop(['Index non utilisé.1'],axis='columns')
    df = df.drop(['Index non utilisé.2'],axis='columns')
    df = df.drop(['Index non utilisé.3'],axis='columns')
    return df


def read_geojson(url):
    """Récupère le géojson des départements puis crée la feature id pour identifier les département dans la map"""
    with urlopen(url) as url:
        jdata = json.loads(url.read().decode())
    for feat in jdata['features']:   #Les ids sont stockées dans 'features/properties avec le nom code'
        feat['id'] = feat['properties']['code']
    return jdata


def get_pop_dataframe():
    """Permet de récuperer le dataset de la population française et de retourner deux build_dataframes
    df_t : dataframe de la population
    df_dep : dataframe qui servira à la création d'un dict code_dep/nom_dep"""
    #Recupération des données
    data = pd.read_excel('https://www.insee.fr/fr/statistiques/fichier/2012713/TCRD_004.xls')

    #Nouveaux noms de colonnes
    new_header = list(data.iloc[2])
    new_header[:3]=['code_dep','nom_dep','2020']
    new_header = [str(nom).split('.')[0] for nom in new_header]
    df = data[3:]
    df.columns = new_header

    #Réorganisation du df
    df = df[['code_dep','nom_dep','Part dans la France (p) (en %)','2020','2017','2012','2007','1999']]
    df.index = [k for k in range(df.shape[0])]

    #Suppression des colonnes vides
    df = df.replace('-',np.NaN)
    df = df.dropna()

    #Restructuration des données
    df[['2020','2017','2012','2007','1999']] = df[['2020','2017','2012','2007','1999']].astype('int64')
    df_t = df.T
    df_t = df_t.drop(['code_dep','nom_dep','Part dans la France (p) (en %)'])
    headers = list(df['code_dep'])
    df_t.columns = headers
    df_t['année'] = df_t.index
    df_t.index = [k for k in range(df_t.shape[0])]
    df_dep = df[['code_dep','nom_dep']]
    return df_t, df_dep

def get_dep_dropdown(df_dep):
    """Permet de créer la liste des dict pour dep_dropdown"""
    list_code = list(df_dep['code_dep'])
    list_nom = list(df_dep['nom_dep'])
    #return {'label': x, 'value' : list_code[k] } for x in list_crimes
    return [{'label':list_nom[k], 'value':list_code[k]} for k in range(len(list_code))]

def get_dep_dict(df_dep):
    """Permet de créer un dictionnaire code_dep/nom_dep"""
    list_code = list(df_dep['code_dep'])
    list_nom = list(df_dep['nom_dep'])
    return {list_code[k]:list_nom[k] for k in range(len(list_code))}


def add_pop_years(df):
    """Permet de réaliser une régression linéaire pour déterminer la population des années manquantes"""

    def get_reg_coef(X,Y): #Fonction de régression linéaire
        model = LinearRegression().fit(X,Y)
        return model.intercept_,model.coef_

    list_annee = [1999,2007,2012,2017,2020]
    x = np.array(list_annee).reshape((-1, 1))
    x_pred = [2013,2014,2015,2016,2019,2019]
    df_bis = pd.DataFrame({'année':[k for k in range(1999,2021)]})
    deps = list(df.columns)[:-1]

    #Calcul de la régression linéaire pour chaque département
    for dep in deps:
        y = np.array(df[dep])[::-1]
        b0, b1 = get_reg_coef(x,y)
        y_pred = []
        i = 0

        #Calcul des points manquants
        for k in range(1999,2021):
            if k in list_annee:
                y_pred.append(y[i])
                i+=1
            else:
                y_pred.append(int(k*b1+b0))
        df_bis[dep]=y_pred
    return df_bis


def get_dataframe(service=None):
    """accesseur des dataframes"""
    if service == 'PN':
        return df_pn
    elif service == 'GN':
        return df_gn
    elif service =='empty':
        return df_empty
    elif service =='pop':
        return df_pop_0
    else:
        return df

def get_dataframe_den(service=None):
    """accesseur des dataframes de la densité de crimes"""
    if service == 'PN':
        return df_dens_pn
    elif service == 'GN':
        return df_dens_gn
    else:
        return df_dens

def build_dens_df():
    """constructeur des dataframes de densité de crimes"""
    list_gn=[]
    list_pn=[]
    #Pour chaque année, on merge les dfs de crimes avec la pop (pour supprimer les départements non renseignés) puis on divise l'ensemble des crimes par cette colonne
    for year in range(2012,2020):
        df_grouped_gn = df_gn.groupby(['dep','année']).sum().filter(like=str(year), axis=0)
        df_grouped_pn = df_pn.groupby(['dep','année']).sum().filter(like=str(year), axis=0)
        df_merged_gn = pd.merge(df_grouped_gn,df_pop_carte[[year,'dep']],on='dep')
        df_merged_pn = pd.merge(df_grouped_pn,df_pop_carte[[year,'dep']],on='dep')
        df_merged_gn[list_crimes]=df_merged_gn[list_crimes].div(df_merged_gn[[year]].to_numpy()*10**(-3))
        df_merged_pn[list_crimes]=df_merged_pn[list_crimes].div(df_merged_pn[[year]].to_numpy()*10**(-3))
        df_merged_gn['annee'] = [year for k in range(df_merged_gn.shape[0])]
        df_merged_pn['annee'] = [year for k in range(df_merged_pn.shape[0])]
        list_gn.append(df_merged_gn.drop(year,axis=1))
        list_pn.append(df_merged_pn.drop(year,axis=1))
    df_dens_gn = pd.concat(list_gn)
    df_dens_pn = pd.concat(list_pn)
    return df_dens_gn,df_dens_pn

#Ouverture des data pour l'application

build_dataframes()

depart = read_geojson('https://france-geojson.gregoiredavid.fr/repo/departements.geojson')

year = 2019

df_gn = open_csv('data/crimes_GN.csv')
df_pn = open_csv('data/crimes_PN.csv')

df = pd.concat([df_gn,df_pn])
list_crimes = list(df.columns)[2:-3]

df_2019 = get_dataframe().groupby(['dep','année']).sum().filter(like='2019', axis=0)
df_2019['dep'] = list(df_2019.index.get_level_values('dep'))

df_empty = df[['dep','année','service']]
df_empty['vide'] = [0 for k in range(df.shape[0])]

df_pop_less, df_dep = get_pop_dataframe()
df_pop_0 = add_pop_years(df_pop_less)


df_pop_carte = df_pop_0
df_pop_carte.index = df_pop_0['année']
df_pop_carte = df_pop_carte.drop(['année'],axis=1)
df_pop_carte = df_pop_carte.T
df_pop_carte['dep'] = df_pop_carte.index

df_dens_gn,df_dens_pn = build_dens_df()
df_dens = pd.concat([df_dens_gn,df_dens_pn])
df_dens_0 = df_dens.groupby(['dep','annee']).sum().filter(like='2019', axis=0)
df_dens_0['dep'] = list(df_dens_0.index.get_level_values('dep'))
