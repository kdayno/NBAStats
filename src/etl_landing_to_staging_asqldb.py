import pyodbc
import sqlalchemy as sa
import pandas as pd
import urllib
import nba_stats_api as api
import secrets as s
from utilities import move_col


connection_string = f"DRIVER={s.driver};SERVER={s.server};DATABASE={s.database};UID={s.username};PWD={s.password};Port=1433;"
params = urllib.parse.quote_plus(connection_string)
engine = sa.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


# ETL DATA FROM "landing.teams" TO "staging.teams"
with engine.connect() as connection:
    # Extract
    selected_columns = ['teamId', 'city', 'fullName', 'confName', 'tricode',
                        'teamShortName', 'divName', 'nickname', 'altCityName']

    teams_df = pd.read_sql_table(
        table_name='teams', con=connection, schema='landing', columns=selected_columns)

    # Transform
    rename_column_mapping = {'teamId': 'TeamID',
                             'city': 'CityName',
                             'fullName': 'TeamFullName',
                             'confName': 'ConferenceName',
                             'tricode': 'CityTriCode',
                             'teamShortName': 'TeamShortName',
                             'divName': 'DivisionName',
                             'nickname': 'TeamNickName',
                             'altCityName': 'AlternativeCityName'
                             }

    teams_df.rename(columns=rename_column_mapping,
                    inplace=True, errors='raise')

    organize_column_mapping = ['TeamID', 'TeamFullName', 'CityName',
                               'TeamNickName', 'ConferenceName', 'DivisionName',
                               'CityTriCode', 'TeamShortName', 'AlternativeCityName']

    teams_df = teams_df[organize_column_mapping]

    # Load
    teams_df.to_sql(name='teams',
                         con=connection, schema='staging', if_exists='replace', index=False)


# ETL DATA FROM "landing.season_schedule" TO "staging.season_schedule"
with engine.connect() as connection:
    # Extract
    selected_columns = ['gameId', 'gameUrlCode', 'startTimeUTC', 'startDateEastern', 'hTeam_teamId',
                        'hTeam_score', 'hTeam_win', 'hTeam_loss', 'vTeam_teamId', 'vTeam_score', 'vTeam_win', 'vTeam_loss']

    season_schedule_df = pd.read_sql_table(
        table_name='season_schedule', con=connection, schema='landing', columns=selected_columns)

    # Transform
    season_schedule_df[['gameIdCopy', 'gameMatchUp']
                       ] = season_schedule_df.loc[:, 'gameUrlCode'].str.split('/', expand=True)

    season_schedule_df.drop(
        columns=['gameUrlCode', 'gameIdCopy'], inplace=True)

    def winner_check(row):
        if row['hTeam_score'] > row['vTeam_score']:
            return row['hTeam_teamId']
        else:
            return row['vTeam_teamId']

    season_schedule_df['GameMatchUpWinnerTeamID'] = season_schedule_df.apply(
        lambda row: winner_check(row), axis=1)

    # Rename Columns
    rename_column_mapping = {'gameId': 'GameID',
                             'gameMatchUp': 'GameMatchUpTriCode',
                             'startTimeUTC': 'GameStartTimeUTC',
                             'startDateEastern': 'GameDate',
                             'hTeam_teamId': 'HomeTeamID',
                             'hTeam_score': 'HomeTeamFinalScore',
                             'hTeam_win': 'HomeTeamCurrentWinCount',
                             'hTeam_loss': 'HomeTeamCurrentLossCount',
                             'vTeam_teamId': 'AwayTeamID',
                             'vTeam_score': 'AwayTeamFinalScore',
                             'vTeam_win': 'AwayTeamCurrentWinCount',
                             'vTeam_loss': 'AwayTeamCurrentLossCount'}

    season_schedule_df.rename(columns=rename_column_mapping,
                              inplace=True, errors='raise')

    organize_column_mapping = ['GameID', 'GameMatchUpTriCode', 'GameDate', 'GameStartTimeUTC',
                               'HomeTeamID', 'HomeTeamFinalScore', 'HomeTeamCurrentWinCount', 'HomeTeamCurrentLossCount',
                               'AwayTeamID', 'AwayTeamFinalScore', 'AwayTeamCurrentWinCount', 'AwayTeamCurrentLossCount',
                               'GameMatchUpWinnerTeamID']

    season_schedule_df = season_schedule_df[organize_column_mapping]

    # Load
    season_schedule_df.to_sql(name='season_schedule',
                              con=connection, schema='staging', if_exists='append', index=False)


# landing_player_profiles
# landing_player_career_stats
# landing_box_score_basic_game_stats
# landing_box_score_detailed_game_stats
