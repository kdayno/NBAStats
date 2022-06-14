import pyodbc
import sqlalchemy as sa
from requests import get
import pandas as pd
import urllib
import datetime as dt
from sql_column_dtypes import player_career_stats_column_dtypes, team_column_dtypes, player_profile_column_dtypes, season_schedule_column_dtypes
import time
import nba_stats_api as api
import sql_secrets as s


connection_string = f"DRIVER={s.driver};SERVER={s.server};DATABASE={s.database};UID={s.username};PWD={s.password};Port=1433;"
params = urllib.parse.quote_plus(connection_string)
engine = sa.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


# INSTANTIATE API OBJECT
api = api.NBAStatsAPI()

print("Data ingestion starting...")

# LOAD DATA INTO LANDING.TEAMS TABLE
teams_data_df = pd.DataFrame(api.team_data)

with engine.connect() as connection:
    teams_data_df.to_sql('teams', connection, schema='landing',
                         if_exists='append', index=False, dtype=team_column_dtypes)

# LOAD DATA INTO LANDING.PLAYER_PROFILES TABLE
player_profiles_data_df = pd.DataFrame(api.player_profile_data)
player_profiles_data_df.drop(
    columns=['teamSitesOnly', 'teams', 'draft'], inplace=True)

with engine.connect() as connection:
    player_profiles_data_df.to_sql('player_profiles', connection, schema='landing',
                                   if_exists='append', index=False, chunksize=100, dtype=player_profile_column_dtypes)

# LOAD DATA INTO LANDING.SEASON_SCHEDULE TABLE
schedule_data_df = pd.DataFrame(api.season_schedule_data)
schedule_data_df.drop(
    columns=['period', 'nugget', 'hTeam', 'vTeam', 'watch', 'playoffs', 'tags', 'playoffs_vTeam', 'playoffs_hTeam'], inplace=True)

with engine.connect() as connection:
    schedule_data_df.to_sql('season_schedule', connection, schema='landing',
                            if_exists='append', index=False, chunksize=100, dtype=season_schedule_column_dtypes)

# LOAD DATA INTO LANDING.PLAYER_CAREER_STATS TABLE
player_career_stats_df = pd.DataFrame(api.get_all_players_career_stats_data())

with engine.connect() as connection:
    player_career_stats_df.to_sql(
        'player_career_stats', connection, schema='landing', if_exists='append', index=False, chunksize=100, dtype=player_career_stats_column_dtypes)

# LOAD DATA INTO LANDING.BOX_SCORE_BASIC_GAME_STATS TABLE
box_score_basic_game_stats_df = pd.DataFrame(
    api.get_all_box_score_basic_game_stats_data())

with engine.connect() as connection:
    box_score_basic_game_stats_df.to_sql(
        'box_score_basic_game_stats', connection, schema='landing', if_exists='replace', index=False, chunksize=100
    )

# LOAD DATA INTO LANDING.BOX_SCORE_DETAILED_GAME_STATS TABLES
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
        'box_score_detailed_game_stats_1', connection, schema='landing', if_exists='replace', index=False, chunksize=1000
    )

with engine.connect() as connection:
    box_score_detailed_game_stats_df_2.to_sql(
        'box_score_detailed_game_stats_2', connection, schema='landing', if_exists='replace', index=False, chunksize=1000
    )

with engine.connect() as connection:
    box_score_detailed_game_stats_df_3.to_sql(
        'box_score_detailed_game_stats_3', connection, schema='landing', if_exists='replace', index=False, chunksize=1000
    )

print("Data ingestion complete.")
