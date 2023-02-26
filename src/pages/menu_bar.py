from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def create_home_link(label):
    return dmc.Text(
        label,
        size="xl",
        style={"fontSize": 34, "color": "#FFFFFF"}
    )


def menubar():
    return dmc.Header(
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
                                html.Img(src='../assets/nba-logo-transparent.png',
                                         style={'height': '50px', 'width': '25px'}),
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
                                                width=26,
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
                                    title="",
                                    id="drawer",
                                    padding="md",
                                    position="right",
                                    children=[
                                        dmc.Text(
                                            children=[
                                                dmc.ThemeIcon(
                                                    DashIconify(
                                                        icon="material-symbols:home",
                                                        className='menu-icons'
                                                    ),
                                                    className='menu-icons'
                                                ),
                                                dcc.Link(
                                                    'Home',
                                                    href='/',
                                                    className='menu-links')
                                            ]),
                                        dmc.Text(
                                            children=[
                                                dmc.ThemeIcon(
                                                    DashIconify(
                                                        icon="mdi:bracket",
                                                        className='menu-icons'
                                                    ),
                                                    className='menu-icons'
                                                ),
                                                dcc.Link(
                                                    'League',
                                                    href='league',
                                                    className='menu-links')
                                            ]),
                                        dmc.Text(
                                            children=[
                                                dmc.ThemeIcon(
                                                    DashIconify(
                                                        icon="fluent:people-team-24-filled",
                                                        className='menu-icons'
                                                    ),
                                                    className='menu-icons'
                                                ),
                                                dcc.Link(
                                                    'Teams',
                                                    href='teams',
                                                    className='menu-links')
                                            ]),
                                    ]
                                )
                            ]
                        )
                    ]
                )
                ]
            )
        ]
    )
