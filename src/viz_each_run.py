import plotly.express as px
from dash import dcc
import pandas as pd
import ast


def sample_reads(df):
    # Add a color column based on whether the sample is "Undetermined"
    df['color'] = df['Sample'].apply(lambda x: 'red' if x == 'undetermined' else 'blue')
    fig = px.bar(df, orientation='h',
                 y="Sample", x='total',
                 labels={'Sample': 'Sample', 'total': 'Total Reads'},
                 title=f"{df['run_name'].iloc[0]}",
                 color='color',  # Use the color column to define the bar colors
                 color_discrete_map={'red': '#EF553B', 'blue': '#636EFA'}  # Map the color values to actual colors
                 )
    
    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    
    return fig


def lane_reads(df):
    df['lane'] = df['Sample'].str.split(' - ').str[-1]
    fig = px.bar(df, orientation='h',
                y="lane", x='total',
                labels={'lane': 'Lane', 'total': 'Total Reads'},
                title=f"{df['run_name'].iloc[0]}"
            )
    # Update the layout of the plot
    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def unkonwn_barcodes(df):
    counts = {}
    for barcodes in df['unknown_barcodes']:
        cc = ast.literal_eval(barcodes)
        for b, c in cc.items():
            if b not in counts.keys():
                counts[b] = c
            else:
                counts[b] += c
    dff = pd.DataFrame(list(counts.items()), columns=['barcodes', 'reads'])
    dff = dff.sort_values(by='reads', ascending=True).head(10)

    fig = px.bar(dff, orientation='h',
                y="barcodes", x='reads',
                labels={'barcodes': 'Unkown Barcodes', 'reads': 'Total Reads'},
                title=f"Unkown Barcodes of {df['run_name'].iloc[0]}"
            )
    # Update the layout of the plot
    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        yaxis=dict(
            tickfont=dict(family="Courier New, monospace")  # Set the y-axis tick labels to monospaced font
        )
    )
    return fig