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


# ETL DATA FROM "landing.player_profiles" TO "staging.player_profiles"
with engine.connect() as connection:

    selected_columns = ['firstName', 'lastName', 'temporaryDisplayName', 'personId', 'teamId', 'jersey',
                        'pos', 'heightFeet', 'heightInches', 'heightMeters', 'weightPounds', 'weightKilograms',
                        'dateOfBirthUTC', 'nbaDebutYear', 'yearsPro', 'collegeName', 'lastAffiliation',
                        'country', 'teamSitesOnly_playerCode', 'teamSitesOnly_posFull', 'draft_teamId',
                        'draft_pickNum', 'draft_roundNum', 'draft_seasonYear', 'teamhist_1_teamId',
                        'teamhist_1_seasonStart', 'teamhist_1_seasonEnd', 'teamhist_2_teamId',
                        'teamhist_2_seasonStart', 'teamhist_2_seasonEnd', 'teamhist_3_teamId',
                        'teamhist_3_seasonStart', 'teamhist_3_seasonEnd']

    player_profiles_df = pd.read_sql_table(
        table_name='player_profiles', con=connection, schema='landing', columns=selected_columns)

    player_profiles_df = player_profiles_df[selected_columns]

    rename_column_mapping = {'firstName': 'PlayerFirstName',
                             'lastName': 'PlayerLastName',
                             'temporaryDisplayName': 'PlayerFullName',
                             'personId': 'PersonID',
                             'teamId': 'TeamID',
                             'jersey': 'JerseyNumber',
                             'pos': 'PlayerPositionCode',
                             'heightFeet': 'HeightFeet',
                             'heightInches': 'HeightInches',
                             'heightMeters': 'HeightMeters',
                             'weightPounds': 'WeightPounds',
                             'weightKilograms': 'WeightKilograms',
                             'dateOfBirthUTC': 'BirthDateUTC',
                             'nbaDebutYear': 'NBADebutYear',
                             'yearsPro': 'YearsProCount',
                             'collegeName': 'CollegeName',
                             'lastAffiliation': 'LastAffiliation',
                             'country': 'CountryName',
                             'teamSitesOnly_playerCode': 'PlayerAlternativeFullName',
                             'teamSitesOnly_posFull': 'PlayerPositionName',
                             'draft_teamId': 'DraftTeamID',
                             'draft_pickNum': 'DraftPickNumber',
                             'draft_roundNum': 'DraftRoundNumber',
                             'draft_seasonYear': 'DraftSeasonYear',
                             'teamhist_1_teamId': 'PreviousTeam1ID',
                             'teamhist_1_seasonStart': 'PreviousTeam1StartYear',
                             'teamhist_1_seasonEnd': 'PreviousTeam1EndYear',
                             'teamhist_2_teamId': 'PreviousTeam2ID',
                             'teamhist_2_seasonStart': 'PreviousTeam2StartYear',
                             'teamhist_2_seasonEnd': 'PreviousTeam2EndYear',
                             'teamhist_3_teamId': 'PreviousTeam3ID',
                             'teamhist_3_seasonStart': 'PreviousTeam3StartYear',
                             'teamhist_3_seasonEnd': 'PreviousTeam3EndYear'}

    player_profiles_df.rename(
        columns=rename_column_mapping, inplace=True, errors='raise')

    player_profiles_df = move_col(
        player_profiles_df, ['PersonID', 'TeamID'], 'PlayerFirstName', 'Before')
    player_profiles_df = move_col(
        player_profiles_df, ['PlayerPositionName'], 'PlayerPositionCode', 'Before')

    # Load
    player_profiles_df.to_sql(name='player_profiles', con=connection,
                              schema='staging', if_exists='replace', index=False, chunksize=100)


# ETL DATA FROM "landing.player_career_stats" TO "staging.player_career_stats"
with engine.connect() as connection:

    # Extract
    selected_columns = ['career_summary_tpp', 'career_summary_ftp', 'career_summary_fgp',
                        'career_summary_ppg', 'career_summary_rpg', 'career_summary_apg',
                        'career_summary_bpg', 'career_summary_mpg', 'career_summary_spg',
                        'career_summary_assists', 'career_summary_blocks', 'career_summary_steals',
                        'career_summary_turnovers', 'career_summary_offReb', 'career_summary_defReb',
                        'career_summary_totReb', 'career_summary_fgm', 'career_summary_fga',
                        'career_summary_tpm', 'career_summary_tpa', 'career_summary_ftm',
                        'career_summary_fta', 'career_summary_pFouls', 'career_summary_points',
                        'career_summary_gamesPlayed', 'career_summary_gamesStarted', 'career_summary_plusMinus',
                        'career_summary_min', 'career_summary_dd2', 'career_summary_td3', 'personId']

    player_career_stats_df = pd.read_sql_table(
        table_name='player_career_stats', con=connection, schema='landing', columns=selected_columns)

    # Transform
    rename_column_mapping = {'career_summary_tpp': 'TPPercentage',
                             'career_summary_ftp': 'FreeThrowPercentage',
                             'career_summary_fgp': 'FieldGoalPercentage',
                             'career_summary_ppg': 'PointsPerGameAverage',
                             'career_summary_rpg': 'ReboundsPerGameAverage',
                             'career_summary_apg': 'AssistsPerGameAverage',
                             'career_summary_bpg': 'BlocksPerGameAverage',
                             'career_summary_mpg': 'MinutesPerGameAverage',
                             'career_summary_spg': 'StealsPerGameAverage',
                             'career_summary_assists': 'TotalAssistsCount',
                             'career_summary_blocks': 'TotalBlocksCount',
                             'career_summary_steals': 'TotalStealsCount',
                             'career_summary_turnovers': 'TotalTurnoversCount',
                             'career_summary_offReb': 'TotalOffensiveReboundsCount',
                             'career_summary_defReb': 'TotalDefensiveReboundsCount',
                             'career_summary_totReb': 'TotalReboundsCount',
                             'career_summary_fgm': 'TotalFieldGoalsMadeCount',
                             'career_summary_fga': 'TotalFieldGoalsAttemptedCount',
                             'career_summary_tpm': 'Total3-PointFieldGoalsMadeCount',
                             'career_summary_tpa': 'Total3-PointFieldGoalsAttemptedCount',
                             'career_summary_ftm': 'TotalFreeThrowsMadeCount',
                             'career_summary_fta': 'TotalFreeThrowsAttemptedCount',
                             'career_summary_pFouls': 'TotalPersonalFoulsCount',
                             'career_summary_points': 'TotalPointsCount',
                             'career_summary_gamesPlayed': 'TotalGamesPlayedCount',
                             'career_summary_gamesStarted': 'TotalGamesStartedCount',
                             'career_summary_plusMinus': 'PlusMinus',
                             'career_summary_min': 'TotalMinutesPlayedCount',
                             'career_summary_dd2': 'TotalDoubleDoublesCount',
                             'career_summary_td3': 'TotalTripleDoublesCount',
                             'personId': 'PersonID'}

    player_career_stats_df.rename(columns=rename_column_mapping, inplace=True)

    player_career_stats_df = move_col(player_career_stats_df, cols_to_move=[
                                      'PersonID'], ref_col='TPPercentage', place='Before')

    # Load
    player_career_stats_df.to_sql(name='player_career_stats', con=connection,
                                  schema='staging', if_exists='replace', index=False, chunksize=100)


# landing_box_score_basic_game_stats
# landing_box_score_detailed_game_stats
