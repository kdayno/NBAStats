from dash import Dash, html, dcc, dash_table, Output, Input, callback
import dash_mantine_components as dmc
import pandas as pd
from dash_iconify import DashIconify
import plotly.express as px
import plotly.graph_objects as go


week_mapping = {'42': 1, '43': 2, '44': 3, '45': 4, '46': 5,
                '47': 6, '48': 7, '49': 8, '50': 9, '51': 10, '52': 11,
                '00': 11, '01': 12, '02': 13, '03': 14, '04': 15, '05': 16,
                '06': 17, '07': 18, '08': 19, '09': 20, '10': 21, '11': 22,
                '12': 23, '13': 24, '14': 25, '15': 25}

file_path = r'/Users/kdayno/Development/02-PROJECTS/NBAWarRoomDashboard/data/nba_standings_2021_2022_season.csv'

df = pd.read_csv(file_path, parse_dates=['Date'])
df = df.sort_values(by='Date', ascending=True)

df['Season Week'] = df['Date'].dt.strftime('%W')
df['Season Week'].replace(week_mapping, inplace=True)
df = df.groupby(['Season Week', 'Team'], as_index=False)['W'].max()
df.sort_values(by='Season Week', ascending=True, inplace=True)
df = df.loc[df['Season Week'] < 27]

color_discrete_map = {'ATL': '#C8102E', 'BKN': '#000000', 'BOS': '#007A33', 'CHA': '#1D1160', 'CHI': '#CE1141',
                      'CLE': '#860038', 'DAL': '#00538C', 'DEN': '#FEC524', 'DET': '#C8102E', 'GSW': '#1D428A',
                      'HOU': '#CE1141', 'IND': '#FDBB30', 'LAC': '#C8102E', 'LAL': '#FFC72C', 'MEM': '#5D76A9',
                      'MIA': '#98002E', 'MIL': '#00471B', 'MIN': '#0C2340', 'NOP': '#0C2340', 'NYK': '#F58426',
                      'OKC': '#007AC1', 'ORL': '#0077C0', 'PHI': '#006BB6', 'PHX': '#E56020', 'POR': '#E03A3E',
                      'SAC': '#5A2D81', 'SAS': '#C4CED4', 'TOR': '#CE1141', 'UTA': '#002B5C', 'WAS': '#002B5C'}

fig = px.scatter(df, x="Season Week", y="W", animation_frame="Season Week", animation_group="Team", text="Team",
                 color="Team", hover_name="Team", range_x=[0, 25.99], range_y=[0, 83], color_discrete_map=color_discrete_map)

last_frame_num = int(len(fig.frames) - 1)
fig.layout['sliders'][0]['active'] = last_frame_num
fig = go.Figure(data=fig['frames'][last_frame_num]
                ['data'], frames=fig['frames'], layout=fig.layout)

fig.update_traces(marker=dict(size=12,
                              line=dict(width=2)),
                  selector=dict(mode='markers'))

fig.update_yaxes(
    dtick="5",
    title="Wins")

fig.update_xaxes(dtick="1")

fig.update_traces(textposition='middle left')

fig.update_layout(
    width=1100,
    height=750,
    font=dict(
        family="Helvetica",
        size=12,
    ),
    showlegend=False,
)


app = Dash(__name__)

# Layout:
# Row 1 > Navigation Bar
# Row 2 > Table Visuals + Scatterplot Visual
# Row 3 > Dropdown Menu for Table Visuals


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
            dmc.Text("2021-2022 Season",
                     style={"fontSize": 30,
                            "textAlign": "center",
                            "fontWeight": "bold"}
                     ),
            span=12

        ),
        dmc.Col(
            dmc.Stack([

                dmc.Text("Conference",
                         style={"fontSize": 16,
                                "textAlign": "center",
                                "fontWeight": "bold", }
                         ),

                dmc.ChipGroup([
                    dmc.Chip(
                        x,
                        value=x,
                        variant="outline",
                        size='md'
                    )
                    for x in ['Western', 'Eastern']
                ],
                    id="conference-values",
                    multiple=True,
                    position='center',
                    style={'marginBottom': 25},
                ),

                dmc.Text("Division",
                         style={"fontSize": 16,
                                "textAlign": "center",
                                "fontWeight": "bold", }
                         ),

                dmc.MultiSelect(
                    data=['Atlantic', 'Central', 'Southeast',
                          'Northwest', 'Pacific', 'Southwest'],
                    searchable=True,
                    clearable=True,
                    nothingFound="No options found",
                    placeholder="Select a division",
                    style={'marginBottom': 25},
                ),

                dmc.Text("Team",
                         style={"fontSize": 16,
                                "textAlign": "center",
                                "fontWeight": "bold", }
                         ),

                dmc.MultiSelect(
                    data=['ATL', 'BKN', 'BOS', 'CHA', 'CHI',
                          'CLE', 'DAL', 'DEN', 'DET', 'GSW',
                          'HOU', 'IND', 'LAC', 'LAL', 'MEM',
                          'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
                          'OKC', 'ORL', 'PHI', 'PHX', 'POR',
                          'SAC', 'SAS', 'TOR', 'UTA', 'WAS', ],
                    searchable=True,
                    clearable=True,
                    nothingFound="No options found",
                    placeholder="Select a team",
                    style={'marginBottom': 25},
                ),

                dmc.Button(
                    "Reset filters",
                    variant="light",
                ),


            ],
                style={"height": 800, "paddingTop": 100},
                spacing='sm'),
            span=2,
            offset=0.2
        ),

        dmc.Col(
            dcc.Graph(
                id='season_standings',
                figure=fig),
            span=9,
            offset=0.25
        ),

    ]
)


@ callback(
    Output("drawer", "opened"),
    Input("drawer-button", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_menu(n_clicks):
    return True


if __name__ == '__main__':
    app.run_server(debug=True, port=8055)
