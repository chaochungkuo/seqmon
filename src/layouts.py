from dash import html, dcc, dash_table
from datetime import datetime, timedelta

def create_layout(config):
    logo_path = config['logo'][0]
    print(logo_path)

    return html.Div([
        # Side panel
        html.Div([
            # html.Img(src=logo_path, style={'width': '100%', 'margin-bottom': '20px'}),  # Logo
            html.H1("Seqmon", style={'font-family': 'Roboto, sans-serif'}),
            html.H3("A Light Sequencing Monitor", style={'font-family': 'Roboto, sans-serif'}),
            html.Div("This web app is used to monitor the sequencing runs from multiple sequencers for their efficiency and quality.", style={'font-family': 'Roboto, sans-serif'}),
            html.Br(),
            html.H3("Define the range of dates", style={'font-family': 'Roboto, sans-serif'}),
            dcc.DatePickerSingle(
                id='start-date-picker',
                date=(datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
                display_format='YYYY-MM-DD',
                style={'margin-bottom': '10px'}
            ),
            dcc.DatePickerSingle(
                id='end-date-picker',
                date=datetime.now().strftime('%Y-%m-%d'),
                display_format='YYYY-MM-DD',
                style={'margin-bottom': '10px'}
            ),
            dcc.Dropdown(
                id='sequencer-dropdown',
                options=[{'label': path.split('/')[-1], 'value': path} for path in config['bcl_paths']],
                multi=True,
                placeholder="Select sequencers",
                style={'margin-bottom': '10px', 'font-family': 'Roboto, sans-serif'}
            ),
            html.Button('Reload Data', id='reload-button', style={'margin-bottom': '10px'}),
            html.Button('Reset App', id='reset-button')
        ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px', 'background-color': '#f4f4f4'}),
        
        # Main body
        html.Div([
            # Summary figures
            dcc.Graph(id='summary-figures', style={'margin-bottom': '20px'}),
            
            # Table of runs
            dash_table.DataTable(
                id='runs-table',
                columns=[
                    {'name': 'Run Name', 'id': 'run_name'},
                    {'name': 'Total Reads', 'id': 'total_reads'},
                    {'name': 'Undetermined Ratio', 'id': 'undetermined_ratio'},
                    {'name': 'Sequencer', 'id': 'sequencer'},
                ],
                row_selectable='single',
                selected_rows=[],
                style_table={'height': '300px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': '#e1e1e1', 'fontWeight': 'bold'},
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f9f9f9'
                    }
                ],
            ),
            
            # Detailed figures for the selected run
            dcc.Graph(id='detailed-figures')
        ], style={'width': '75%', 'display': 'inline-block', 'padding': '20px'})
    ])
