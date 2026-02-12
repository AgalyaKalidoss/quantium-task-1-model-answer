import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load processed data
df = pd.read_csv("formatted_sales_data.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Sort by date
df = df.sort_values("Date")

# Create line chart
fig = px.line(
    df,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time",
    labels={
        "Date": "Date",
        "Sales": "Total Sales"
    }
)

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser", style={"textAlign": "center"}),
    
    dcc.Graph(
        id="sales-line-chart",
        figure=fig
    )
])

if __name__ == "__main__":
    app.run(debug=True)

