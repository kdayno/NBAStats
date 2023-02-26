import dash
from dash import html
import dash_mantine_components as dmc
from .menu_bar import menubar


dash.register_page(__name__)

layout = dmc.Grid(
    children=[
        dmc.Col(
            menubar(),
            span=12,
            style={"height": "80px"}
        ),

        dmc.Col(
            html.H1(children='This is the NBA Stats League page')
        ),
    ]
)
