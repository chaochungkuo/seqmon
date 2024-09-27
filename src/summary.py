import plotly.express as px
from dash import dcc
import pandas as pd

def summary_total(df):
    """
    Generates a scatter plot with 'total' as Y-axis, 'date' as X-axis, and color-coded by 'sequencer'.
    """
    # Create the scatter plot
    fig = px.scatter(
        df,
        x='date',
        y='total',
        color='sequencer_x',
        title='Total Reads',
        labels={'date': 'Date', 'total': 'Total'},
        hover_name='run_name',
        hover_data={'sequencer_x': True, 'total': True, 'date': True}
    )

    # Update the layout of the plot
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total',
        margin=dict(l=40, r=40, t=40, b=40),
        legend_title_text='Sequencer',
        legend=dict(
            orientation="v",  # Horizontal legend
            yanchor="top",
            y=-0.2,  # Position below the plot
            xanchor="center",
            x=0.5  # Centered horizontally
        )
    )

    return fig

def summary_undetermined(df):
    """
    Generates a scatter plot with 'undetermined' as Y-axis, 'date' as X-axis, and color-coded by 'sequencer'.
    """
    df["undetermined_pct"] = df["undetermined_pct"] * 100
    # Create the scatter plot
    fig = px.scatter(
        df,
        x='date',
        y='undetermined_pct',
        color='sequencer_x',
        title='Undetermined Reads (%)',
        labels={'date': 'Date', 'undetermined_pct': 'Undetermined (%)'},
        hover_name='run_name',
        hover_data={'sequencer_x': True, 'undetermined_pct': True, 'date': True}
    )

    # Update the layout of the plot
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Undetermined (%)',
        margin=dict(l=40, r=40, t=40, b=40),
        legend_title_text='Sequencer',
        legend=dict(
            orientation="v",  # Horizontal legend
            yanchor="top",
            y=-0.2,  # Position below the plot
            xanchor="center",
            x=0.5  # Centered horizontally
        )
    )

    return fig