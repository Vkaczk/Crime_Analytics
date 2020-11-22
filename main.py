import pandas as pd
import plotly_express as px

import os.path

from data_read import *

from urllib.request import urlopen

import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

if __name__ == '__main__':
    app.run_server(debug=False)
