import yaml
from dash import Dash, html
from layouts import create_layout
from callbacks import register_callbacks
import dash_bootstrap_components as dbc
# import os

# Load configuration
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

external_stylesheets = [dbc.themes.CERULEAN]
# Initialize Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Set layout
app.layout = create_layout(config, app_title="Seqmon")

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
