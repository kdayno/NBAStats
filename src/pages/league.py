
import pathlib

import dash
from dash import html, dcc
import dash_mantine_components as dmc
from .menu_bar import menubar
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df = pd.read_csv(DATA_PATH.joinpath(
    "nba_standings_2021_2022_season_refined.csv"), parse_dates=['Date'])

week_mapping = {'42': 1, '43': 2, '44': 3, '45': 4, '46': 5,
                '47': 6, '48': 7, '49': 8, '50': 9, '51': 10, '52': 11,
                '00': 11, '01': 12, '02': 13, '03': 14, '04': 15, '05': 16,
                '06': 17, '07': 18, '08': 19, '09': 20, '10': 21, '11': 22,
                '12': 23, '13': 24, '14': 25, '15': 25}

color_discrete_map = {'ATL': '#C8102E', 'BKN': '#000000', 'BOS': '#007A33', 'CHA': '#1D1160', 'CHI': '#CE1141',
                      'CLE': '#860038', 'DAL': '#00538C', 'DEN': '#FEC524', 'DET': '#C8102E', 'GSW': '#1D428A',
                      'HOU': '#CE1141', 'IND': '#FDBB30', 'LAC': '#C8102E', 'LAL': '#FFC72C', 'MEM': '#5D76A9',
                      'MIA': '#98002E', 'MIL': '#00471B', 'MIN': '#0C2340', 'NOP': '#0C2340', 'NYK': '#F58426',
                      'OKC': '#007AC1', 'ORL': '#0077C0', 'PHI': '#006BB6', 'PHX': '#E56020', 'POR': '#E03A3E',
                      'SAC': '#5A2D81', 'SAS': '#C4CED4', 'TOR': '#CE1141', 'UTA': '#002B5C', 'WAS': '#002B5C'}


df = df.sort_values(by='Date', ascending=True)
df['Season Week'] = df['Date'].dt.strftime('%W')
df['Season Week'].replace(week_mapping, inplace=True)
df = df.groupby(['Season Week', 'Team', 'Conference', 'Conference Indicator',
                'Division', 'Division Indicator', 'Date'], as_index=False)['W'].max()
df.sort_values(by='Season Week', ascending=True, inplace=True)
df = df.loc[df['Season Week'] < 27]

fig = px.scatter(df, x="Season Week", y="W", animation_frame="Season Week",
                         animation_group="Team", text="Team", color="Team", hover_name="Team",
                         color_discrete_map=color_discrete_map, title="<b>2021-2022 Season</b>",)

fig.update_traces(marker=dict(size=12,
                                  line=dict(width=2)),
                      selector=dict(mode='markers'))

fig.update_yaxes(
    dtick="5",
    title="Wins",
    range=[0, 83])

fig.update_xaxes(
    dtick="1",
    title="Week",
    range=[0, 25.99])

fig.update_traces(textposition='middle left')

fig.update_layout(
    title_font_size=32,
    title_font_color="#000000",
    title_x=0.5,
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family="Helvetica",
        size=12,
    ),
    showlegend=False,
)

layout = dmc.Grid(
    children=[
        dmc.Col(
            menubar(),
            span=12,
            style={"height": "80px"}
        ),

        dmc.Col(
            html.H1(children='This is the NBA Stats League page'),
            span=12,
        ),

        dmc.Col(
            dcc.Graph(figure=fig,
                      style={'border-radius': '10px', 'background-color': '#FFFFFF',
                                               'width': 1100, 'height': 750, 
                                               "boxShadow": "5px 5px 5px 5px lightgrey"},)
        ),
    ]
)
