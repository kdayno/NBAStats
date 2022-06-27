from dash import Dash, html, dcc, dash_table, Output, Input, callback
import dash_mantine_components as dmc
import pandas as pd
from dash_iconify import DashIconify


df = pd.read_csv(
    '/Users/kdayno/Development/02-PROJECTS/NBAWarRoomDashboard/data/nba_season_2021_final_standings_v2.csv')
west_teams_df = df.loc[df['confName'] == 'West',
                       ['fullName', 'win', 'loss', 'winPct', 'gamesBehind']]

west_teams_df.rename(columns={'fullName': 'Western Conference',
                              'win': 'W',
                              'loss': 'L',
                              'winPct': 'W %',
                              'gamesBehind': 'GB'}, inplace=True)

west_teams_df.sort_values(by='W', ascending=False, inplace=True)

east_teams_df = df.loc[df['confName'] == 'East',
                       ['fullName', 'win', 'loss', 'winPct', 'gamesBehind']]

east_teams_df.rename(columns={'fullName': 'Eastern Conference',
                              'win': 'W',
                              'loss': 'L',
                              'winPct': 'W %',
                              'gamesBehind': 'GB'}, inplace=True)

east_teams_df.sort_values(by='W', ascending=False, inplace=True)


style_cell = {'height': '10px',
              'minWidth': '10px',
              'width': '250px',
              'maxWidth': '200px',
              'font-family': 'Helvetica',
              'textAlign': 'center'}


style_table = {'width': '350px',
               'overflow': 'hidden',
               'borderRadius': '5px',
               'border': '1px solid black'}


app = Dash(__name__)

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
                class_name="dash-header",
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
                                                        "NBA STATS DASHBOARD"),
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
                                                        color="#FFFFFF",
                                                    ),
                                                    radius=30,
                                                    size=35,
                                                    variant="filled",
                                                    style={
                                                        "background-color": "#051B2D"}
                                                ),
                                                variant="subtle",
                                                size="md",
                                                class_name="menu-button",
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
            style={"height": "120px"}),

        dmc.Col(
            dmc.Text("Regular Season Standings",
                     style={"fontSize": 30,
                            "textAlign": "center",
                            "fontWeight": "bold", }
                     ),
            span=6,
            offset=0.25,
        ),

        dmc.Col(
            dmc.Text("Season At A Glance",
                     style={"fontSize": 30,
                            "textAlign": "center",
                            "fontWeight": "bold"}
                     ),
            span=5

        ),

        dmc.Col(
            html.Div(
                dash_table.DataTable(data=west_teams_df.to_dict('records'),
                                     columns=[{"name": i, "id": i}
                                              for i in west_teams_df.columns],
                                     style_cell=style_cell,
                                     style_table=style_table)
            ),
            span=3,
            offset=0.25,
            style={"height": "500px",
                   "backgroundColor": "#FFFFFF",
                   "boxShadow": "0 10px 15px 0 rgba(0, 0, 0, 0.19)"}
        ),

        dmc.Col(
            html.Div(
                dash_table.DataTable(data=east_teams_df.to_dict('records'),
                                     columns=[{"name": i, "id": i}
                                              for i in east_teams_df.columns],
                                     style_cell=style_cell,
                                     style_table=style_table)
            ),
            span=3,
            style={"height": "500px",
                   "width": "1000px",
                   "backgroundColor": "#FFFFFF",
                   "boxShadow": "10px 10px 15px 0 rgba(0, 0, 0, 0.19)"}
        ),

        dmc.Col(
            span=5.9
        ),

        dmc.Col(
            span=12
        ),

        dmc.Col(
            span=12
        ),

        dmc.Col(
            dcc.Dropdown(
                ['Conference', 'Division'],
                'Conference',
                clearable=False,
                searchable=False
            ),
            span=2,
            offset=2
        )
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
