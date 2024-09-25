from dash import dcc, html, Input, Output, State
import os
import pandas as pd

def register_callbacks(app, config):
    @app.callback(
        Output('summary-figures', 'figure'),
        Output('runs-table', 'data'),
        Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('sequencer-dropdown', 'value'),
        Input('reload-button', 'n_clicks'),
    )
    def update_summary_and_table(start_date, end_date, selected_sequencers, n_clicks):
        # Initialize an empty list to store data
        data = []

        # Iterate through each sequencer path
        for sequencer_path in selected_sequencers:
            # Iterate through each run under the sequencer path
            for root, dirs, files in os.walk(sequencer_path):
                for file in files:
                    if file.endswith('.bcl'):  # Example condition, adjust based on your files
                        run_name = os.path.basename(root)
                        total_reads = calculate_total_reads(root)
                        undetermined_ratio = calculate_undetermined_ratio(root)
                        data.append({
                            'run_name': run_name,
                            'total_reads': total_reads,
                            'undetermined_ratio': undetermined_ratio,
                            'sequencer': sequencer_path.split('/')[-1],
                        })

        df = pd.DataFrame(data)
        
        # Create summary figures
        figure = {
            'data': [
                {
                    'x': df['run_name'],
                    'y': df['total_reads'],
                    'type': 'bar',
                    'name': 'Total Reads',
                    'marker': {'color': df['sequencer']}
                },
                {
                    'x': df['run_name'],
                    'y': df['undetermined_ratio'],
                    'type': 'bar',
                    'name': 'Undetermined Ratio',
                    'marker': {'color': df['sequencer']}
                },
            ],
            'layout': {
                'title': 'Summary of Runs',
                'barmode': 'group'
            }
        }
        
        return figure, df.to_dict('records')

    @app.callback(
        Output('detailed-figures', 'figure'),
        Input('runs-table', 'selected_rows'),
        State('runs-table', 'data')
    )
    def update_detailed_figures(selected_rows, table_data):
        if not selected_rows:
            return {}
        
        selected_run = table_data[selected_rows[0]]
        # Extract details of the selected run
        # Implement logic to retrieve and visualize detailed figures
        
        detailed_figure = {
            'data': [
                # Example data
                {
                    'x': [1, 2, 3],  # Replace with actual data
                    'y': [10, 20, 30],  # Replace with actual data
                    'type': 'line',
                    'name': selected_run['run_name']
                }
            ],
            'layout': {
                'title': f'Detailed Figures for {selected_run["run_name"]}',
            }
        }
        
        return detailed_figure

    @app.callback(
        Output('start-date-picker', 'date'),
        Output('end-date-picker', 'date'),
        Output('sequencer-dropdown', 'value'),
        Output('runs-table', 'selected_rows'),
        Input('reset-button', 'n_clicks')
    )
    def reset_app(n_clicks):
        return (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d'), [], []

def calculate_total_reads(run_path):
    # Implement logic to calculate total reads from BCL files
    return 0  # Replace with actual calculation

def calculate_undetermined_ratio(run_path):
    # Implement logic to calculate undetermined ratio from BCL files
    return 0.0  # Replace with actual calculation
