# Analyse des crimes et délits en France de 2012 à 2019

## Table des matières

 - [Introduction](#Introduction)
 - [User's Guide](#users-guide)
 - [Developper's Guide](#developpers-guide)
 - [Rapport d'analyse](#rapport-danalyse)
 - [Liens des données](#lien-des-données)


# Introduction

Chaque année, de nombreux articles apparaissent témoignant d'une augmentation de la criminalité en France ainsi que de l'aggravation du sentiment d'insécurité au sein de la population. Récemment, au cours de l'année 2020, le terme "ensauvagement" a été grandement utilisé par le gouvernement français pour qualifier la gravité de la situation. <br>

Le but de ce dashboard est de vérifier la véracité de ces propos pour savoir si ce sentiment croissant s'insécurité est justifié ou est le résultat d'un jeu politique et médiatique. <br>

Le jeu de données utilisé est un recueil des crimes recensés par les services de gendarmerie et les services de police de 2012 à 2019.
Nous avons complété ce dernier avec un jeu de données recensant la population nationale par département.

# User's Guide

Le dashboard nécessite d'avoir installé python3 sur son ordinateur. Il est conseillé d'utiliser Anaconda pour pouvoir installer plus facilement les librairies nécessaires.

Les packages et librairies nécessaires à la bonne exécution du code sont :

  - pandas
  - plotly_express
  - plotly.graph_objects
  - os
  - re
  - urllib
  - numpy
  - json
  - dash
  - dash_html_components
  - dash_core_components
  - dash_html_components
  - sklearn.linear_model

Pour installer une librairie :<br>
      - sur Windows via Anaconda, il faut utiliser la commande : conda install [package] <br>
      - sur Linux : pip install [package] <br>

Le dashboard se lance via le terminal depuis la racine du projet avec la commande : python3 main.py

Lors de la première exécution, le programme télécharge les fichiers Excel automatiquement puis réalise le traitement de ceux-ci. Cette action prend plusieurs minutes. C'est pourquoi les fichiers transformés sont ensuite enregistrés dans le dossier data pour ne plus attendre lors des futures exécutions. <br>
Le dashboard est hébergé sur le port : http://127.0.0.1:8050/

# Developper's Guide

## Architecture du Projet
Le projet se décompose en 5 fichiers:
 - main.py : fichier principal permettant le lancement de l'app.
 - app.py : Contient le lancement de l'app, le Layout et les callbacks.
 - data_read.py : Contient les fonctions permettant l'importation et le travail sur les datasets. Il crée également les dataframes.
 - figures.py : Initialise les figures et contient les fonctions de création de map.
 - navbar.py : Contient la fonction permettant la création de la navbar dans le layout.

## Pistes d'amélioration
Voici quelques pistes d'amélioration pour perfectionner le dashboard
 - La régression linéaire pourrait être améliorée. Certains départements ne suivent pas une croissance linéaire, comme Paris, et une régression polynomiale serait plus adaptée.
 - L'update du slider input pourrait être améliorer afin d'obtenir un rafraichissement plus rapide.
 - La prise en compte des critiques dans la partie rapport d'analyse pourrait conduire à la mise en place de la prédiction statistique des crimes non signalés ou non enregistrés
 - L'utilisation d'autre jeu de données pour la population prenant en compte les déplacements des citoyens (ex: repérage anonyme via réseau téléphonique) et la localisation précise des emplacements des gendarmeries ou centre de police voir des lieux des infractions.

# Rapport d'analyse
L'objectif de ce dashboard était d'observer s'il y a eu une augmentation des crimes et délits de 2012 à 2019. Le jeu de données étant composé de 103 infractions différentes allant des vols à main armée jusqu'aux fraudes alimentaires et infraction à l'hygiène en passant par les fraudes fiscales et la consommation de stupéfiant, mais exclu les infractions routières. Afin de pouvoir examiner spécifiquement les infractions en lien à l'insécurité, nous avons regroupé les crimes et délits par thématique. Les infractions liées à l'insécurité regroupent de façon non exhaustive les différents types de vols, les agressions, les viols ou les homicides. Un autre regroupement comprenant uniquement les vols à aussi été réalisé.<br>

Une carte du nombre de crimes et délits par millier d'habitants à aussi été réalisée permettant de géolocaliser les zones les plus touchées par la criminalité en France en tenant compte du nombre d'habitants par département.

## Résultats obtenus
Nous avons pu observer que la somme des infractions liées à l'insécurité reste stable au cours du temps. Les crimes et délits recensés par la police restent aux alentours de 1.4M et ceux par la gendarmerie autour de 1.1M. <br>
L'ensemble des vols perpétrés en France reste aussi globalement stable (environ 1M) et on peut même remarque une diminution de ceux rescenséspar la gendarmerie, c'est-à-dire en campagne.<br>
Quant à la somme de toutes les infractions, celle-ci est aussi relativement stable (environ 2.3M) bien qu'on puisse observer une légère augmentation à la fois par ceux recensés par la police (+100k) et par la gendarmerie (300k) <br>
Cepandant, il est intéressant de remarquer que pour les infractions telles que les viols ou les harcèlements sexuels, une nette augmentation est visible. En effet, la somme de ces crimes et délit double sur les sept années étudiées. Ce résultat est à mettre en perspective à cause de l'évolution de la législation entre 2015 et 2016, mais nous aborderons ce point dans la partie suivante.

On remarque grâce à la carte que la majorité des infractions à lieu dans le sud est de la France ainsi qu'à Paris, et ce indépendamment du nombre d'habitants. Néanmoins, certains crimes ou délits sont particulièrement représentés dans des régions précises comme les règlements de compte en malfaiteur en Corse.

## Critiques
À la suite de ces résultats, il est important de relever plusieurs points quant à la fiabilité de ces données afin de ne pas tirer de conclusions hâtives. <br>

### Déclaration des infractions

  - Les infractions déclarées ne se sont pas forcément produites sur le territoire où elles ont été enregistrées.
  - Les infractions déclarées sur une année peuvent s'être produites l'année précédente.
  - Les infractions déclarées ne sont pas forcément représentatives de l'insécurité des citoyens (fonction de la catégorie). La plainte n'est pas forcément déposée :<br>
        - 90% pour les vols de voiture <br>
        - 70-80% pour les cambriolages <br>
        - 20-30% pour les violences physiques (hors ménage) <br>
        - 10% pour les violences physiques (au sein du ménage) et les violences sexuelles <br>
 - Les infractions sans victimes physiques ou morales (ex: stupéfiants) témoignent de l'investissement des forces de l'ordre dans la lutte contre celles-ci <br>

### Modalités d'enregistrement

 - Une évolution des systèmes d'enregistrement est à noter entre 2012 et 2015 pour la gendarmerie et à partir de 2013 pour la police
 - Le territoire de certains services évolue au cours des années
 - Ne sont comptées que les infractions suffisamment constituées juridiquement pour pouvoir être poursuivies par un tribunal

## Conclusion

Au vu des critiques, il semble complexe d'apporter une réponse tranchée au problème soulevé. Bien que les données semblent nier la présence d'une augmentation de la criminalité, la difficulté de recenser les infractions doit être prise en compte et notre analyse ne permet pas d'invalider l'augmentation de l'insécurité en France.

# Lien des données

Les données proviennent de data.gouv et de l'INSEE et sont disponibles aux URL suivantes: <br>

 - Crimes et délits enregistrés par la police et la gendarmerie :<br>
https://static.data.gouv.fr/resources/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012/20200129-181725/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012.xlsx
 - Population française répartie par département :<br>
https://www.insee.fr/fr/statistiques/fichier/2012713/TCRD_004.xls
