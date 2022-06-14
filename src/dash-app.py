from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

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
              'maxWidth': '250px',
              'font-family': 'arial',
              'letterSpacing': '1px',
              'textAlign': 'center'}

style_table = {'borderRadius': '5px',
               'overflow': 'hidden',
               'border': '1px solid black',
               'tableLayout': 'fixed',
               'width': '350px'}


app = Dash(__name__)

app.layout = html.Div([

    html.Div([html.H1("NBA War Room Dashboard", className='banner')]),

    html.Div([
        html.Div(dash_table.DataTable(data=west_teams_df.to_dict('records'),
                                      columns=[{"name": i, "id": i}
                                               for i in west_teams_df.columns],
                                      style_cell=style_cell,
                                      style_table=style_table),
             className='data-table left'
                 ),

        html.Div(dash_table.DataTable(data=east_teams_df.to_dict('records'),
                                      columns=[{"name": i, "id": i}
                                               for i in east_teams_df.columns],
                                      style_cell=style_cell,
                                      style_table=style_table),
             className='data-table right'
                 )
    ],  className='table-container'),

])


if __name__ == '__main__':
    app.run_server(debug=True, port=8055)
