from dash.dependencies import Input, Output
from summary import summary_total, summary_undetermined
import pandas as pd
from table_integration import update_tables
from datetime import datetime

def filter_tables(start_date, end_date, select_sequencers):
    # Load your dataframes (bcl_stats, multiqc_lanes, etc.)
    bcl_stats = pd.read_csv("data/bcl_stats.csv")
    multiqc_summary = pd.read_csv("data/multiqc_summary.csv")
    merged_df = pd.merge(bcl_stats, multiqc_summary, on='run_name', how='outer')
    merged_df["date"] = pd.to_datetime(merged_df['run_name'].str[:6], format='%y%m%d')
    merged_df["% >= Q30"] = merged_df["% >= Q30"] / 100
    filtered_df = merged_df[
        (merged_df['date'] >= pd.to_datetime(start_date)) & 
        (merged_df['date'] <= pd.to_datetime(end_date)) &
        (merged_df['sequencer_x'].isin(select_sequencers))
    ]
    return filtered_df

def register_callbacks(app):
    @app.callback(
        Output('runs-table', 'data'),
        Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('sequencer-checklist', 'value')
    )
    def update_table(start_date, end_date, select_sequencers):
        df = filter_tables(start_date, end_date, select_sequencers)
        table_data = df.to_dict('records')
        return table_data
    
    @app.callback(
        Output('summary-total', 'figure'),
        Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('sequencer-checklist', 'value')
    )
    def update_summarytotal(start_date, end_date, select_sequencers):
        df = filter_tables(start_date, end_date, select_sequencers)
        fig = summary_total(df)
        return fig
    
    @app.callback(
        Output('summary-undetermined', 'figure'),
        Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('sequencer-checklist', 'value')
    )
    def update_undetermined(start_date, end_date, select_sequencers):
        df = filter_tables(start_date, end_date, select_sequencers)
        fig = summary_undetermined(df)
        return fig
    
    @app.callback(
        Output('last-reload', 'children'),
        Input('reload-button', 'n_clicks'),
    )
    def run_update_tables(n_clicks):
        if n_clicks is not None:  # Only run if the button has been clicked
            update_tables()
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

