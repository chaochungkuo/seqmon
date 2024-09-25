import yaml
from dash import Dash, html
from layouts import create_layout
from callbacks import register_callbacks
# import os

# Load configuration
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Initialize Dash app
app = Dash(__name__)

# Set layout
app.layout = create_layout(config)

# Register callbacks
# register_callbacks(app, config)
# image_path = os.path.join(os.getcwd(), 'assets/test.png')
# print(image_path)
# app.layout = html.Div([
#     html.Img(src=app.get_asset_url('test.png'))
# ])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
