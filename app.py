import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import glob
import os

# --- STEP 1: LOAD AND PROCESS DATA ---
path = 'data'
all_files = glob.glob(os.path.join(path, "daily_sales_data_*.csv"))

data_frames = []
for filename in all_files:
    df_temp = pd.read_csv(filename)
    data_frames.append(df_temp)

df = pd.concat(data_frames, ignore_index=True)
df = df[df['product'] == 'pink morsel']
df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)
df['sales'] = df['price'] * df['quantity']
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

# --- STEP 2: INITIALIZE DASH APP ---
app = dash.Dash(__name__)
app.title = "Soul Foods: Pink Morsels"

# --- STEP 3: APP LAYOUT WITH STYLISH CSS ---
app.layout = html.Div(
    style={
        'background-color': '#1B1B1B',   # dark background
        'color': '#E0E0E0',              # light text
        'font-family': '"Roboto", sans-serif',
        'padding': '50px',
        'min-height': '100vh'
    },
    children=[
        # --- Title ---
        html.H1(
            "Pink Morsels Sales Visualiser", 
            style={
                'text-align': 'center',
                'color': '#FF6EC7',
                'margin-bottom': '50px',
                'font-weight': '700',
                'letter-spacing': '1px',
                'text-shadow': '2px 2px 6px #000000'
            }
        ),
        
        # --- Filter Panel (Single Row) ---
        html.Div(
            style={
                'background-color': '#2A2A2A',
                'padding': '20px 30px',
                'border-radius': '20px',
                'box-shadow': '0 10px 20px rgba(0,0,0,0.6)',
                'width': 'fit-content',
                'margin': '0 auto 40px auto',
                'border': '1px solid #444',
                'display': 'flex',         # horizontal row
                'align-items': 'center',   # vertical alignment
                'gap': '25px'              # space between label and buttons
            },
            children=[
                html.Label(
                    "Filter by Region:", 
                    style={
                        'font-weight': '700', 
                        'font-size': '20px', 
                        'color': '#FF6EC7',
                        'margin': '0'
                    }
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
                        'margin-right': '20px',
                        'font-size': '16px',
                        'padding': '6px 14px',
                        'cursor': 'pointer',
                        'border-radius': '10px',
                        'transition': 'all 0.2s ease',
                        'background-color': '#3A3A3A',
                        'color': '#E0E0E0'
                    },
                    inputStyle={'margin-right': '8px'}
                ),
            ]
        ),
        
        # --- Graph Container ---
        html.Div(
            style={
                'background-color': '#2C2C2C',
                'padding': '30px',
                'border-radius': '20px',
                'box-shadow': '0 12px 24px rgba(0,0,0,0.7)',
                'border': '1px solid #444'
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
        plot_bgcolor='#2C2C2C',
        paper_bgcolor='#2C2C2C',
        font_color='#E0E0E0',
        title_font_color='#FF6EC7',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#444'),
    )
    
    fig.update_traces(line_color='#FF6EC7' if selected_region != 'all' else None)
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
