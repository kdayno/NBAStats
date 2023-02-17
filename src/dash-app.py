from dash import Dash, html, dcc, Output, Input, callback, no_update
import dash_mantine_components as dmc
import pandas as pd
from dash_iconify import DashIconify
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


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

team_tricodes = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI',
                 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
                 'HOU', 'IND', 'LAC', 'LAL', 'MEM',
                 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
                 'OKC', 'ORL', 'PHI', 'PHX', 'POR',
                 'SAC', 'SAS', 'TOR', 'UTA', 'WAS', ]

file_path = r'/Users/kdayno/Development/02-PROJECTS/NBAStats/data/nba_standings_2021_2022_season.csv'

df = pd.read_csv(file_path, parse_dates=['Date'])

eastern_conf = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI',
                'CLE', 'DET', 'IND', 'MIA', 'MIL',
                'NYK', 'ORL', 'PHI', 'TOR', 'WAS']
western_conf = ['DAL', 'DEN', 'GSW',  'HOU', 'LAC',
                'LAL', 'MEM', 'MIN', 'NOP', 'OKC',
                'PHX', 'POR', 'SAC', 'SAS', 'UTA']

atlantic_div = ['BKN', 'BOS', 'NYK', 'PHI', 'TOR']

central_div = ['CHI', 'CLE', 'DET', 'IND', 'MIL']

southeast_div = ['ATL', 'CHA', 'MIA', 'ORL', 'WAS']

northwest_div = ['DEN', 'MIN', 'OKC', 'POR', 'UTA']

pacific_div = ['GSW', 'LAC', 'LAL', 'PHX', 'SAC']

southwest_div = ['DAL', 'HOU', 'MEM', 'NOP', 'SAS']

conf_conditions = [
    (df['Team'].isin(eastern_conf)),
    (df['Team'].isin(western_conf))
]

conferences = ['Eastern', 'Western']

div_conditions = [
    (df['Team'].isin(atlantic_div)),
    (df['Team'].isin(central_div)),
    (df['Team'].isin(southeast_div)),
    (df['Team'].isin(northwest_div)),
    (df['Team'].isin(pacific_div)),
    (df['Team'].isin(southwest_div)),
]

divisons = ['Atlantic', 'Central', 'Southeast',
            'Northwest', 'Pacific', 'Southwest']

df['Conference'] = np.select(conf_conditions, conferences)
df['Division'] = np.select(div_conditions, divisons)

df = df.sort_values(by='Date', ascending=True)
df['Season Week'] = df['Date'].dt.strftime('%W')
df['Season Week'].replace(week_mapping, inplace=True)
df = df.groupby(['Season Week', 'Team', 'Conference',
                'Division'], as_index=False)['W'].max()
df.sort_values(by='Season Week', ascending=True, inplace=True)
df = df.loc[df['Season Week'] < 27]


app = Dash(__name__)


def create_home_link(label):
    return dmc.Text(
        label,
        size="xl",
        style={"fontSize": 34, "color": "#FFFFFF"}
    )


app.layout = dmc.Grid(
    children=[
        dmc.Col(
            dmc.Header(
                className="dash-header",
                height=75,
                fixed=True,
                p="xs",
                children=[
                    dmc.Container(
                        fluid=True,
                        children=[dmc.Group(
                            position="apart",
                            align="center",
                            spacing="lg",
                            children=[
                                dmc.Group(
                                    children=[
                                        html.Img(src=app.get_asset_url(
                                            'nba-logo-transparent.png'), style={'height': '50px', 'width': '25px'}),
                                        dcc.Link(
                                            [
                                                dmc.MediaQuery(
                                                    create_home_link(
                                                        "NBA STATS"),
                                                    smallerThan="sm",
                                                    styles={"display": "none"},
                                                ),
                                                dmc.MediaQuery(
                                                    create_home_link(
                                                        "NBA STATS"),
                                                    largerThan="sm",
                                                    styles={"display": "none"},
                                                ),
                                            ],
                                            href='/',
                                            style={"textDecoration": "none"},
                                        ),
                                    ]),
                                dmc.Group(
                                    children=[
                                        dmc.Tooltip(
                                            dmc.Button(
                                                dmc.ThemeIcon(
                                                    DashIconify(
                                                        icon="dashicons:menu-alt",
                                                        width=35,
                                                        # color="#FFFFFF",
                                                    ),
                                                    radius=30,
                                                    size=35,
                                                    variant="filled",
                                                    style={
                                                        "background-color": "#051B2D"}
                                                ),
                                                variant="subtle",
                                                size="md",
                                                className="menu-button",
                                                id="drawer-button"
                                            ),
                                            label="Menu",
                                            position="bottom",
                                        ),
                                        dmc.Drawer(
                                            title="Drawer Menu",
                                            id="drawer",
                                            padding="md",
                                            position="right"
                                        )
                                    ]
                                )
                            ]
                        )
                        ]
                    )
                ]
            ),
            span=12,
            style={"height": "80px"}),

        dmc.Col(
            dmc.Stack([

                dmc.Text("Conference",
                         style={"fontSize": 16,
                                "textAlign": "center",
                                "fontWeight": "bold",
                                "color": "#FFFFFF"}
                         ),

                dmc.ChipGroup([
                    dmc.Chip(
                        children='Western',
                        value='Western',
                        variant="outline",
                        size='md',
                        id='chip-west'
                    ),
                    dmc.Chip(
                        children='Eastern',
                        value='Eastern',
                        variant="outline",
                        size='md',
                        id='chip-east'
                    ),

                ],
                    id="conference-filter",
                    multiple=True,
                    position='center',
                    style={'marginBottom': 25},
                ),

                dmc.Text("Division",
                         style={"fontSize": 16,
                                "textAlign": "center",
                                "fontWeight": "bold",
                                "color": "#FFFFFF"}
                         ),

                dmc.MultiSelect(
                    data=[div for div in sorted(df['Division'].unique())],
                    value=[],
                    searchable=True,
                    clearable=True,
                    nothingFound="No options found",
                    placeholder="Select a division",
                    style={'marginBottom': 25},
                    id='division-filter'
                ),

                dmc.Text("Team",
                         style={"fontSize": 16,
                                "textAlign": "center",
                                "fontWeight": "bold",
                                "color": "#FFFFFF"}
                         ),

                dmc.MultiSelect(
                    data=[team for team in sorted(df['Team'].unique())],
                    value=[],
                    searchable=True,
                    clearable=True,
                    nothingFound="No options found",
                    placeholder="Select a team",
                    style={'marginBottom': 25},
                    id='team-filter'
                ),

                dmc.Button(
                    "Reset filters",
                    # leftIcon=DashIconify(
                    #     icon="carbon:settings-check"),
                    variant="gradient",
                    gradient={"from": "silver", "to": "gray"},
                    id='reset-filters-button'
                ),

            ],
                style={"height": 650, "width": 230, "paddingTop": 100, "paddingRight": 20, "paddingLeft": 20,
                       "backgroundColor": "#07243B", "borderRadius": "10px", "opacity": 80,
                       "boxShadow": "5px 5px 5px grey"},
                spacing='sm'),
            span=2,
            offset=0.4
        ),

        dmc.Col(
            html.Div([
                dmc.LoadingOverlay(
                    children=[dcc.Graph(id='standings-scatter-plot',
                                        style={'border-radius': '10px', 'background-color': '#FFFFFF',
                                               'width': 1100, 'height': 750, "boxShadow": "5px 5px 5px 5px lightgrey"},
                                        config={'displayModeBar': 'hover',
                                                'autosizable': False,
                                                'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'zoom2d', 'resetScale2d', 'toImage'],
                                                'displaylogo': False,
                                                'doubleClick': 'reset'}
                                        )
                              ],
                    loaderProps={"variant": "oval",
                                 "color": "blue", "size": "xl"},
                    overlayColor='#E0E0E0',
                    overlayOpacity='50',
                    radius='10px',
                    style={"width": 1100, "height": 750,
                           "background-color": "#F6F6F6"},
                    styles={"background-color": "#F6F6F6"},
                )]),
            span=9,
            offset=0.4,
        ),

    ]
)


@callback(
    Output('drawer', 'opened'),
    Input('drawer-button', 'n_clicks'),
    prevent_initial_call=True,
)
def drawer_menu(n_clicks):
    return True


@callback(
    Output('division-filter', 'value'),
    Input('conference-filter', 'value'),
)
def set_division_options(input_conf):
    if input_conf == None:
        return no_update
    else:
        dff = df[df['Conference'].isin(input_conf)]
        return [d for d in sorted(dff['Division'].unique())]


@callback(
    Output('chip-east', 'checked'),
    Output('chip-west', 'checked'),
    Output('conference-filter', 'value'),
    Input('reset-filters-button', 'n_clicks'),
    prevent_initial_call=True,
)
def reset_filters(click):
    if click:
        return (False, False, [])


@callback(
    Output('team-filter', 'value'),
    Input('division-filter', 'value'),
)
def set_team_options(input_div):
    dff = df[df['Division'].isin(input_div)]
    return [team for team in sorted(dff['Team'].unique())]


@callback(
    Output('standings-scatter-plot', 'figure'),
    Input('conference-filter', 'value'),
    Input('division-filter', 'value'),
    Input('team-filter', 'value'),
)
def update_graph(input_conf, input_div, input_team):

    if (input_team is None) | (input_team == []):
        dff = df
        fig = px.scatter(dff, x="Season Week", y="W", animation_frame="Season Week", animation_group="Team", text="Team",
                         color="Team", hover_name="Team", color_discrete_map=color_discrete_map,
                         title="<b>2021-2022 Season</b>",)

    else:
        dff = df[(df['Team'].isin(input_team))]

        fig = px.scatter(dff, x="Season Week", y="W", animation_frame="Season Week", animation_group="Team", text="Team",
                         color="Team", hover_name="Team", color_discrete_map=color_discrete_map,
                         title="<b>2021-2022 Season</b>",)

    # Sets plot to display final team standings by default
    last_frame_num = int(len(fig.frames) - 1)
    fig.layout['sliders'][0]['active'] = last_frame_num
    fig = go.Figure(data=fig['frames'][last_frame_num]
                    ['data'], frames=fig['frames'], layout=fig.layout)

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

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8055)
