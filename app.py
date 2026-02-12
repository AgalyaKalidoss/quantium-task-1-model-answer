import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("formatted_sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "backgroundColor": "#0f172a",
        "color": "white",
        "padding": "20px",
        "minHeight": "100vh"
    },
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={"textAlign": "center", "marginBottom": "20px"}
        ),

        html.Div(
            style={
                "width": "50%",
                "margin": "auto",
                "padding": "10px",
                "backgroundColor": "#1e293b",
                "borderRadius": "10px"
            },
            children=[
                html.Label("Select Region:", style={"fontWeight": "bold"}),

                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={"marginTop": "10px"}
                ),
            ]
        ),

        html.Br(),

        dcc.Graph(id="sales-line-chart")
    ]
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    if selected_region != "all":
        filtered_df = df[df["Region"] == selected_region]
    else:
        filtered_df = df

    fig = px.line(
        filtered_df,
        x="Date",
        y="Sales",
        title="Pink Morsel Sales Over Time",
        labels={"Date": "Date", "Sales": "Total Sales"}
    )

    fig.update_layout(
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        font_color="white"
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
