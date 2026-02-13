import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import glob
import os

# --- STEP 1: LOAD AND PROCESS DATA ---
# Using glob to find all sales files in the 'data' folder
path = 'data'
all_files = glob.glob(os.path.join(path, "daily_sales_data_*.csv"))

data_frames = []
for filename in all_files:
    df_temp = pd.read_csv(filename)
    data_frames.append(df_temp)

# Combine datasets
df = pd.concat(data_frames, ignore_index=True)

# Filter for 'pink morsel' only
df = df[df['product'] == 'pink morsel']

# Process 'price' to remove '$' and convert to float
df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)

# Calculate 'Sales' (price * quantity)
df['sales'] = df['price'] * df['quantity']

# Convert 'date' column to datetime (lowercase 'date' as seen in your CSV)
df['date'] = pd.to_datetime(df['date'])

# Sort by date for a clean line chart
df = df.sort_values(by='date')

# --- STEP 2: INITIALIZE DASH APP ---
app = dash.Dash(__name__)
app.title = "Soul Foods: Pink Morsels"

# --- STEP 3: APP LAYOUT WITH CSS ---
app.layout = html.Div(
    style={
        'background-color': '#111111',
        'color': '#E1E1E1',
        'font-family': '"Open Sans", sans-serif',
        'padding': '40px',
        'min-height': '100vh'
    },
    children=[
        html.H1(
            "Pink Morsels Sales Visualiser", 
            style={
                'text-align': 'center', 
                'color': '#FF69B4', 
                'margin-bottom': '40px',
                'text-shadow': '2px 2px 4px #000000'
            }
        ),
        
        # Selection Control Panel
        html.Div(
            style={
                'background-color': '#222222',
                'padding': '30px',
                'border-radius': '15px',
                'box-shadow': '0 4px 8px 0 rgba(255, 105, 180, 0.2)',
                'width': 'fit-content',
                'margin': '0 auto 30px auto',
                'border': '1px solid #333'
            },
            children=[
                html.Label(
                    "Filter by Region:", 
                    style={'font-weight': 'bold', 'font-size': '20px', 'display': 'block', 'margin-bottom': '15px', 'color': '#FF69B4'}
                ),
                dcc.RadioItems(
                    id='region-selector',
                    options=[
                        {'label': 'North', 'value': 'north'},
                        {'label': 'East', 'value': 'east'},
                        {'label': 'South', 'value': 'south'},
                        {'label': 'West', 'value': 'west'},
                        {'label': 'All Regions', 'value': 'all'}
                    ],
                    value='all',
                    labelStyle={
                        'display': 'inline-block', 
                        'margin-right': '25px', 
                        'font-size': '18px',
                        'cursor': 'pointer'
                    },
                    inputStyle={'margin-right': '8px'}
                ),
            ]
        ),
        
        # Graph Container
        html.Div(
            style={
                'background-color': '#222222',
                'padding': '20px',
                'border-radius': '15px',
                'box-shadow': '0 8px 16px 0 rgba(0, 0, 0, 0.5)'
            },
            children=[
                dcc.Graph(id='sales-line-chart')
            ]
        )
    ]
)

# --- STEP 4: CALLBACK FOR INTERACTIVITY ---
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-selector', 'value')
)
def update_chart(selected_region):
    if selected_region != 'all':
        filtered_df = df[df['region'] == selected_region]
    else:
        filtered_df = df
    
    fig = px.line(
        filtered_df,
        x='date',
        y='sales',
        color='region' if selected_region == 'all' else None,
        title=f"Sales Trend: {selected_region.capitalize()}",
        template='plotly_dark'
    )
    
    fig.update_layout(
        plot_bgcolor='#222222',
        paper_bgcolor='#222222',
        font_color='#E1E1E1',
        title_font_color='#FF69B4',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#444'),
    )
    
    fig.update_traces(line_color='#FF69B4' if selected_region != 'all' else None)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
