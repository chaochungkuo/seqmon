from dash.dependencies import Input, Output
from summary import summary_total, summary_undetermined
from viz_each_run import sample_reads, lane_reads, unkonwn_barcodes
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

    @app.callback(
        Output('sample-reads', 'figure'),
        Input('runs-table', 'selected_rows'),
        Input('runs-table', 'data')
    )
    def update_sample_reads(selected_rows, table_data):
        if selected_rows:
            # Get the index of the selected row
            selected_row_idx = selected_rows[0]
            # Get the data of the selected row
            selected_row = table_data[selected_row_idx]
            sel_run_name = selected_row["run_name"]
            
            df_samples = pd.read_csv('data/multiqc_samples.csv')
            df_samples = df_samples.loc[df_samples["run_name"]==sel_run_name]
            
            if df_samples.shape[0] > 0:
                fig = sample_reads(df_samples)
            else:
                fig = {}
        else:
            # Return an empty figure if no row is selected
            fig = {}

        return fig

    @app.callback(
        Output('lane-reads', 'figure'),
        Input('runs-table', 'selected_rows'),
        Input('runs-table', 'data')
    )
    def update_lane_reads(selected_rows, table_data):
        if selected_rows:
            # Get the index of the selected row
            selected_row_idx = selected_rows[0]
            # Get the data of the selected row
            selected_row = table_data[selected_row_idx]
            sel_run_name = selected_row["run_name"]
            
            df_samples = pd.read_csv('data/multiqc_lanes.csv')
            df_samples = df_samples.loc[df_samples["run_name"]==sel_run_name]
            
            if df_samples.shape[0] > 0:
                fig = lane_reads(df_samples)
            else:
                fig = {}
        else:
            # Return an empty figure if no row is selected
            fig = {}

        return fig
    
    @app.callback(
        Output('unknown_barcodes', 'figure'),
        Input('runs-table', 'selected_rows'),
        Input('runs-table', 'data')
    )
    def update_unknown_barcodes(selected_rows, table_data):
        if selected_rows:
            # Get the index of the selected row
            selected_row_idx = selected_rows[0]
            # Get the data of the selected row
            selected_row = table_data[selected_row_idx]
            sel_run_name = selected_row["run_name"]
            
            df_samples = pd.read_csv('data/multiqc_lanes.csv')
            df_samples = df_samples.loc[df_samples["run_name"]==sel_run_name]
            print(df_samples)
            if df_samples.shape[0] > 0:
                fig = unkonwn_barcodes(df_samples)
            else:
                fig = {}
        else:
            # Return an empty figure if no row is selected
            fig = {}

        return fig