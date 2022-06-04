import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.express as px
from plotly.graph_objects import Layout
import pandas as pd

df = pd.read_csv("world_countires_population.csv")
df = df[df["Year"] <= 2020]

app = dash.Dash(__name__)
server = app.server

app.title = "Wold Population Dashboard"

app.layout = html.Div(
    children=[
        html.H1(children="World Population Dashboard"),
        html.Div(
            className="container",
            children=[
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="years",
                            options=[{"label": i, "value": i} for i in df["Year"].unique()],
                            value=df["Year"].max(),
                            persistence=True
                        ),
                        dcc.Graph(id='map_graph'),
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="countries",
                            options=[{"label": i, "value": i} for i in df["Country"].unique()],
                            value=[df["Country"].unique()[0]],
                            persistence=True,
                            multi=True
                        ),
                        dcc.Graph(id='line_graph'),
                    ]
                )
            ]
        )
    ]
)

@app.callback(Output('map_graph', 'figure'), Input('years', 'value'))
def map_graph_update(year):
    fig = px.choropleth(
        data_frame=df[df['Year'] == year],
        locations="CountryCode",
        # hover_name="Country",
        color="PopTotal",
        hover_data={'Country': True},
    )
    fig.update_layout(margin=dict(t=30, b=30, l=0, r=0))
    return fig

@app.callback(Output('line_graph', 'figure'), Input('countries', 'value'))
def map_graph_update(country):
    fig = px.line(
        data_frame=df[df['Country'].isin(country)],
        x="Year",
        y="PopTotal",
        color="Country",
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)