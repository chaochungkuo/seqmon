from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import pandas as pd
import base64
from summary import summary_total
import dash.dash_table.FormatTemplate as FormatTemplate

def create_layout(config, app_title):
    logo_path = config['logo'][0]

    return dbc.Container([
        create_banner(app_title=app_title),
        # Side panel
        html.Div([
            html.H1("Seqmon"),
            html.Div("A Lightweight Sequencing Monitor"),
            html.Br(),
            html.Div("This web app is used to monitor the sequencing runs from multiple sequencers for their efficiency and quality."),
            html.Hr(),
            html.Div("Define the starting date"),
            dcc.DatePickerSingle(
                id='start-date-picker',
                date=(datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
                display_format='YYYY-MM-DD',
                style={'margin-bottom': '10px'}
            ),
            html.Div("Define the ending date"),
            dcc.DatePickerSingle(
                id='end-date-picker',
                date=datetime.now().strftime('%Y-%m-%d'),
                display_format='YYYY-MM-DD',
                style={'margin-bottom': '10px'}
            ),
            html.Hr(),
            html.Div("Select the target sequencers"),
            dcc.Checklist(
                id='sequencer-checklist',
                options=[{'label': path, 'value': path} for path in config['sequencers']],
                value=config['sequencers'],
                style={'margin-bottom': '10px', 'font-family': 'Roboto, sans-serif'}
            ),
            html.Hr(),
            html.Button('Reload Data', id='reload-button'),
            html.Div("Last reload:"),
            html.Div(id='last-reload', children="-"),
        ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px', 'background-color': '#f4f4f4'}),
        
        
        # Main body
        html.Div([
            # Summary figures
            html.Div([
                dbc.Row([
                    dbc.Col(dcc.Graph(figure={}, id='summary-total')),
                    dbc.Col(dcc.Graph(figure={}, id='summary-undetermined'))
                ])
            ]),
            # Table of runs
            table_summary(),
            # Detailed figures for the selected run
            dbc.Row([
                dbc.Col(dcc.Graph(id='sample-reads')),
                dbc.Col(dcc.Graph(id='lane-reads')),
            ]),
            dcc.Graph(id='unknown_barcodes'),
        ], style={'width': '75%', 'display': 'inline-block', 'padding': '20px'})
    ])

def create_banner(app_title):
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Img(src='data:assets/png;base64,{}'.format(base64.b64encode(
                                    open(
                                        './assets/plotly_logo.png', 'rb'
                                    ).read()
                                ).decode()
                            ), height=30
                        ), width=10),
                    dbc.Col(html.A(
                        id='gh-link',
                        children=[
                            'View on GitHub'
                        ],
                        href="https://github.com/chaochungkuo/seqmon",
                        style={'color': 'black'}
                    ))
                ], justify="start")
        ],
        style ={'padding':'0.5em'},
        )


def table_summary():
    return dash_table.DataTable(
                id='runs-table',
                columns=[
                    {'name': 'Sequencer', 'id': 'sequencer_x'},
                    {'name': 'Run Name', 'id': 'run_name'},
                    {'name': 'Total Reads', 'id': 'total', 'type': 'numeric'},
                    {'name': 'Undetermined Ratio', 'id': 'undetermined_pct', 'type': 'numeric', 'format': FormatTemplate.percentage(2)},
                    {'name': 'Cluster Count', 'id': 'Cluster Count', 'type': 'numeric'},
                    {'name': 'Cluster Count Pf', 'id': 'Cluster Count Pf', 'type': 'numeric'},
                    {'name': '%Q30', 'id': '% >= Q30', 'type': 'numeric', 'format': FormatTemplate.percentage(2)},
                ],
                row_selectable='single',
                selected_rows=[],
                style_table={'height': '500px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'right',
                            'padding': '10px',
                            'whiteSpace': 'normal', 
                            'overflow': 'hidden',
                            'textOverflow': 'clip',},
                style_header={'backgroundColor': '#e1e1e1', 'fontWeight': 'bold'},
                fixed_rows={'headers': True},
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f9f9f9'
                    },
                    {
                        'if': {'column_id': 'run_name'},
                        'textAlign': 'left',  # Align 'run_name' column to the left
                    },
                    {
                        'if': {'column_id': 'sequencer_x'},
                        'textAlign': 'left',  # Align 'sequencer' column to the left
                    },
                    {
                        'if': {'column_id': 'selected_row'},
                        'width': '150px',  # Adjust the width of the selection column
                        'textAlign': 'center',  # Center-align the tick boxes
                        'overflow': 'hidden',  # Prevent overflow
                        'textOverflow': 'clip',  # Prevent the overflow dots
                        'padding': '0px 0px',  # Adjust padding to make the tick box fit better
                    }
                ],
                sort_action='native',  # Enables sortable headers
            )