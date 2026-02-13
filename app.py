# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load CSVs
df0 = pd.read_csv("daily_sales_data_0.csv")
df1 = pd.read_csv("daily_sales_data_1.csv")
df2 = pd.read_csv("daily_sales_data_2.csv")

# Combine datasets
df = pd.concat([df0, df1, df2], ignore_index=True)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Pink Morsels Sales Dashboard"

# App layout
app.layout = html.Div(
    style={
        'background-color': '#1e1e2f',
        'color': '#ffffff',
        'font-family': 'Segoe UI, sans-serif',
        'min-height': '100vh',
        'padding': '20px'
    },
    children=[
        html.H1("Pink Morsels Sales Dashboard", 
                style={'text-align': 'center', 'color': '#ff6f91', 'margin-bottom': '30px'}),
        
        # Region selector card
        html.Div(
            style={
                'background': 'linear-gradient(135deg, #2c2c54, #1e1e2f)',
                'padding': '20px',
                'border-radius': '15px',
                'width': '50%',
                'margin': 'auto',
                'box-shadow': '0px 0px 15px #ff6f91'
            },
            children=[
                html.Label("Select Region:", style={'font-weight': 'bold', 'font-size': '18px'}),
                dcc.RadioItems(
                    id='region-selector',
                    options=[
                        {'label': 'North', 'value': 'north'},
                        {'label': 'East', 'value': 'east'},
                        {'label': 'South', 'value': 'south'},
                        {'label': 'West', 'value': 'west'},
                        {'label': 'All', 'value': 'all'}
                    ],
                    value='all',
                    labelStyle={'display': 'inline-block', 'margin-right': '20px', 'font-size': '16px', 'color': '#ffffff'}
                ),
            ]
        ),
        
        html.Br(),
        
        # Sales line chart
        html.Div(
            style={
                'background': '#2c2c54',
                'padding': '20px',
                'border-radius': '15px',
                'margin-top': '20px',
                'box-shadow': '0px 0px 15px #ff6f91'
            },
            children=[
                dcc.Graph(id='sales-line-chart')
            ]
        )
    ]
)

# Callback for updating graph
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-selector', 'value')
)
def update_chart(selected_region):
    if selected_region != 'all':
        filtered_df = df[df['Region'].str.lower() == selected_region]
    else:
        filtered_df = df.copy()
    
    fig = px.line(
        filtered_df,
        x='Date',
        y='Sales',
        color='Region',
        title=f"Sales Trend - {selected_region.capitalize() if selected_region != 'all' else 'All Regions'}",
        template='plotly_dark'
    )
    fig.update_layout(
        title={'x':0.5, 'xanchor': 'center', 'font': {'size': 22, 'color': '#ff6f91'}},
        xaxis_title="Date",
        yaxis_title="Sales",
        font={'family': 'Segoe UI', 'size': 14, 'color': '#ffffff'},
        legend={'bgcolor': '#1e1e2f', 'bordercolor': '#ff6f91', 'borderwidth': 1}
    )
    fig.update_traces(mode='lines+markers', line={'width': 3})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
