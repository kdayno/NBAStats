import pyodbc
import sqlalchemy as sa
from requests import get
import pandas as pd
import urllib
import datetime as dt
from sql_column_dtypes import player_career_stats_column_dtypes, team_column_dtypes, player_profile_column_dtypes, season_schedule_column_dtypes
import time
import nba_stats_api as api
import secrets as s


connection_string = f"DRIVER={s.driver};SERVER={s.server};DATABASE={s.database};UID={s.username};PWD={s.password};Port=1433;"
params = urllib.parse.quote_plus(connection_string)
engine = sa.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


# INSTANTIATE API OBJECT
api = api.NBAStatsAPI()

print("Data ingestion starting...")

# LOAD DATA INTO LANDING_TEAMS TABLE
teams_data_df = pd.DataFrame(api.team_data)

with engine.connect() as connection:
    teams_data_df.to_sql('landing_teams', connection,
                         if_exists='append', index=False, dtype=team_column_dtypes)

# LOAD DATA INTO LANDING_PLAYER_PROFILES TABLE
player_profiles_data_df = pd.DataFrame(api.player_profile_data)
player_profiles_data_df.drop(
    columns=['teamSitesOnly', 'teams', 'draft'], inplace=True)

with engine.connect() as connection:
    player_profiles_data_df.to_sql('landing_player_profiles', connection,
                                   if_exists='append', index=False, chunksize=100, dtype=player_profile_column_dtypes)

# LOAD DATA INTO LANDING_SEASON_SCHEDULE TABLE
schedule_data_df = pd.DataFrame(api.season_schedule_data)
schedule_data_df.drop(
    columns=['period', 'nugget', 'hTeam', 'vTeam', 'watch', 'playoffs', 'tags', 'playoffs_vTeam', 'playoffs_hTeam'], inplace=True)

with engine.connect() as connection:
    schedule_data_df.to_sql('landing_season_schedule', connection,
                            if_exists='append', index=False, chunksize=100, dtype=season_schedule_column_dtypes)

# LOAD DATA INTO LANDING_PLAYER_CAREER_STATS TABLE
player_career_stats_df = pd.DataFrame(api.get_all_players_career_stats_data())

with engine.connect() as connection:
    player_career_stats_df.to_sql(
        'landing_player_career_stats', connection, if_exists='append', index=False, chunksize=100, dtype=player_career_stats_column_dtypes)

# LOAD DATA INTO LANDING_BOX_SCORE_BASIC_GAME_STATS TABLE
box_score_basic_game_stats_df = pd.DataFrame(
    api.get_all_box_score_basic_game_stats_data())

with engine.connect() as connection:
    box_score_basic_game_stats_df.to_sql(
        'landing_box_score_basic_game_stats', connection, if_exists='replace', index=False, chunksize=100
    )

# LOAD DATA INTO LANDING_BOX_SCORE_DETAILED_GAME_STATS TABLES
# Data has to be split into 3 tables due to MS SQL Server's 1024 column limit per table
box_score_detailed_game_stats_df = pd.DataFrame(
    api.get_all_box_score_detailed_game_stats_data()
)

game_ids = box_score_detailed_game_stats_df.loc[:, 'gameId']
game_dates = box_score_detailed_game_stats_df.loc[:, 'gameDate']

box_score_detailed_game_stats_df_1 = box_score_detailed_game_stats_df.iloc[:, 0:1000]
box_score_detailed_game_stats_df_1.insert(0, 'gameDate', game_dates)
box_score_detailed_game_stats_df_1.insert(0, 'gameId', game_ids)

box_score_detailed_game_stats_df_2 = box_score_detailed_game_stats_df.iloc[:, 1000:2000]
box_score_detailed_game_stats_df_2.insert(0, 'gameDate', game_dates)
box_score_detailed_game_stats_df_2.insert(0, 'gameId', game_ids)

box_score_detailed_game_stats_df_3 = box_score_detailed_game_stats_df.iloc[:, 2000:]
box_score_detailed_game_stats_df_3.drop(
    columns=['gameId', 'gameDate'], inplace=True)
box_score_detailed_game_stats_df_3.insert(0, 'gameDate', game_dates)
box_score_detailed_game_stats_df_3.insert(0, 'gameId', game_ids)

with engine.connect() as connection:
    box_score_detailed_game_stats_df_1.to_sql(
        'landing_box_score_detailed_game_stats_1', connection, if_exists='replace', index=False, chunksize=1000
    )

with engine.connect() as connection:
    box_score_detailed_game_stats_df_2.to_sql(
        'landing_box_score_detailed_game_stats_2', connection, if_exists='replace', index=False, chunksize=1000
    )

with engine.connect() as connection:
    box_score_detailed_game_stats_df_3.to_sql(
        'landing_box_score_detailed_game_stats_3', connection, if_exists='replace', index=False, chunksize=1000
    )

print("Data ingestion complete.")
