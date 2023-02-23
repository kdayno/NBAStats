import pyodbc
import requests as r
import pandas as pd
import datetime as dt
import time


class NBAStatsAPI:

    base_url = "https://data.nba.net"
    all_json = "/prod/v1/today.json"

    def __init__(self):
        # Dict with JSON endpoints
        self._data_links = self._get_all_data_links()
        # List of dicts with each dict containing data for a team
        self._team_data = self._get_all_team_data()
        # List of dicts with each dict containing data for a player
        self._player_profile_data = self._get_all_player_profiles_data()
        # List of dicts with each dict containing data for a scheduled game
        self._season_schedule_data = self._get_season_schedule_data()
        # List of dicts with each dict containing game id and game date
        self._game_ids_and_dates = self.__extract_data_attributes(
            self._season_schedule_data, ['gameId', 'startDateEastern'])
        # List of dicts with each dict containing person id
        self._player_ids = self.__extract_data_attributes(
            self._player_profile_data, ['personId', 'temporaryDisplayName'])
        # Date data was last refreshed
        self._date_last_refreshed = dt.datetime.strptime(
            self._data_links['currentDate'], '%Y%m%d')

    @property
    def data_links(self):
        return self._data_links

    @property
    def team_data(self):
        return self._team_data

    @property
    def player_profile_data(self):
        return self._player_profile_data

    @property
    def season_schedule_data(self):
        return self._season_schedule_data

    def get_all_players_career_stats_data(self):
        all_players_career_stats = []

        for player in self._player_ids:

            person_id = player['personId']

            player_data_endpoint = self.data_links['playerProfile'].replace(
                '{{personId}}', person_id)

            player_career_summary_data = r.get(
                NBAStatsAPI.base_url + player_data_endpoint).json()

            if 'league' in player_career_summary_data.keys():

                player_career_summary_data = player_career_summary_data[
                    'league']['standard']['stats']['careerSummary']

                career_player_stats = {
                    f"career_summary_{key}": value for key, value in player_career_summary_data.items()}
                career_player_stats['personId'] = person_id

                all_players_career_stats.append(career_player_stats)

        return all_players_career_stats

    def get_all_box_score_basic_game_stats_data(self):

        all_games_box_score_basic_stats = []

        for game in self._game_ids_and_dates:

            game_id = game['gameId']
            game_date = game['startDateEastern']

            game_data_endpoint = self.data_links['boxscore']

            game_data_endpoint = self.data_links['boxscore'].replace(
                '{{gameDate}}', game_date).replace('{{gameId}}', game_id)
            game_box_score_data = r.get(
                NBAStatsAPI.base_url + game_data_endpoint).json()

            basic_game_data = self._flatten_dict(
                game_box_score_data.get('basicGameData'))

            basic_game_data_dict = {
                f"bgd_{key}": value for key, value in basic_game_data.items()}
            basic_game_data_dict['gameId_gameDate'] = f"{game_id}_{game_date}"

            all_games_box_score_basic_stats.append(basic_game_data_dict)

        return all_games_box_score_basic_stats

    def get_all_box_score_detailed_game_stats_data(self):

        all_games_box_score_detailed_stats = []

        for game in self._game_ids_and_dates:

            # Throttles GET requests to avoid server errors from endpoints
            time.sleep(1)

            game_id = game['gameId']
            game_date = game['startDateEastern']

            game_data_endpoint = self.data_links['boxscore']

            game_data_endpoint = self.data_links['boxscore'].replace(
                '{{gameDate}}', game_date).replace('{{gameId}}', game_id)
            game_box_score_data = get(
                NBAStatsAPI.base_url + game_data_endpoint).json()

            detailed_game_data = self._flatten_dict(
                game_box_score_data.get('stats'))

            if detailed_game_data != None:
                detailed_game_data_dict = {
                    f"dgd_{key}": value for key, value in detailed_game_data.items()}
                detailed_game_data_dict['gameId'] = game_id
                detailed_game_data_dict['gameDate'] = game_date

                all_games_box_score_detailed_stats.append(
                    detailed_game_data_dict)

        return all_games_box_score_detailed_stats

    def get_game_data(self, game_date: str, game_id: str):
        '''
        Returns data for a specific game given the "gameId" and "gameDate"
        '''

        game_data_link = self.data_links['boxscore']
        game_data_link = game_data_link.replace('{{gameDate}}', f'{game_date}')
        game_data_link = game_data_link.replace('{{gameId}}', f'{game_id}')

        game_data_endpoint = r.get(
            NBAStatsAPI.base_url + game_data_link).json()
        game_data = game_data_endpoint['basicGameData']

        return game_data

    def _get_all_data_links(self):
        data = r.get(NBAStatsAPI.base_url + NBAStatsAPI.all_json).json()
        links = data['links']

        return links

    def _get_all_team_data(self):
        team_data_endpoint = r.get(
            NBAStatsAPI.base_url + self.data_links['teams']).json()
        team_data = team_data_endpoint['league']['standard']
        team_data = list(
            filter(lambda x: x['isNBAFranchise'] == True, team_data))

        return team_data

    def _get_all_player_profiles_data(self):
        player_data_endpoint = r.get(
            NBAStatsAPI.base_url + self.data_links['leagueRosterPlayers']).json()
        player_data = player_data_endpoint['league']['standard']

        # EXTRACTS NESTED PLAYER DATA
        for player_dict in player_data:

            # EXTRACTS DATA FROM "teamSitesOnly" DICT
            player_dict = self.__extract_nested_dict(
                player_dict, 'teamSitesOnly')

            # EXTRACTS DATA FROM "draft" DICT
            player_dict = self.__extract_nested_dict(player_dict, 'draft')

            # EXTRACT DATA from "teams" LIST OF DICTS
            teams_dict = player_dict.get('teams')

            if teams_dict != None:
                counter = 1

                for team in teams_dict:
                    for key in team:
                        player_dict[f"teamhist_{counter}_{key}"] = team[key]
                    counter += 1

        return player_data

    def _get_season_schedule_data(self):
        schedule_data_endpoint = r.get(
            NBAStatsAPI.base_url + self.data_links['leagueSchedule']).json()
        schedule_data = schedule_data_endpoint['league']['standard']

        # EXTRACTS NESTED SCHEDULE DATA
        for scheduled_game_dict in schedule_data:
            scheduled_game_dict = self.__extract_nested_dict(
                scheduled_game_dict, 'period')
            scheduled_game_dict = self.__extract_nested_dict(
                scheduled_game_dict, 'nugget')
            scheduled_game_dict = self.__extract_nested_dict(
                scheduled_game_dict, 'hTeam')
            scheduled_game_dict = self.__extract_nested_dict(
                scheduled_game_dict, 'vTeam')
            scheduled_game_dict = self.__extract_nested_dict(
                scheduled_game_dict, 'playoffs')

        return schedule_data

    def _flatten_dict(self, parent: dict):
        '''
        Extracts data from any nested dictionaries or lists that exists within the inputted dictionary
        '''
        dict_exists = True
        list_exists = True

        while dict_exists is True or list_exists is True:

            dict_exists = self.__check_for_dict(parent)
            list_exists = self.__check_for_list(parent)

            keys_type_dict = self.__get_keys_type_dict(parent)
            keys_type_list = self.__get_keys_type_list(parent)

            for key in keys_type_dict:
                self.__extract_nested_dict(parent, key)
                del parent[key]

            for key in keys_type_list:
                nested_list = parent[key]
                self.__extract_nested_list(parent, key, nested_list)
                del parent[key]

        return parent

    def __check_for_dict(self, parent: dict):
        '''
        Helper Function: Used in "flatten_dict" function to check parent dictionary for nested dictionaries
        '''
        if parent != None:
            for key in parent:
                value = parent[key]

                if isinstance(value, dict):
                    return True

        return False

    def __check_for_list(self, parent: dict):
        '''
        Helper Function: Used in "flatten_dict" function to check parent dictionary for nested lists
        '''
        if parent != None:
            for key in parent:
                value = parent[key]

                if isinstance(value, list):
                    return True

        return False

    def __get_keys_type_dict(self, parent: dict):
        '''
        Helper Function: Used in "flatten_dict" function to get all keys in parent dictionary that have values of type dict
        '''
        keys = []

        if parent != None:
            for key in parent:
                value = parent[key]

                if isinstance(value, dict):
                    keys.append(key)

        return keys

    def __get_keys_type_list(self, parent: dict):
        '''
        Helper Function: Used in "flatten_dict" function to get all keys in parent dictionary that have values of type list
        '''
        keys = []

        if parent != None:
            for key in parent:
                value = parent[key]

                if isinstance(value, list):
                    keys.append(key)

        return keys

    def __extract_nested_dict(self, parent: dict, nested_key: str):
        '''
        Helper Function: Used in "flatten_dict" function to extract data within nested dictionaries
        '''

        nested = parent.get(f'{nested_key}')

        if nested != None:
            for key in nested:
                parent[f"{nested_key}_{key}"] = nested[key]

        return parent

    def __extract_nested_list(self, parent: dict, nested_key: str, nested_list: list):
        '''
        Helper Function: Used in "flatten_dict" function to extract data within nested lists
        '''

        counter = 1

        for item in nested_list:
            parent[f"{nested_key}_{counter}"] = item
            counter += 1

        return parent

    def __extract_data_attributes(self, input_list_of_dicts: list, data_attributes: list):
        '''
        Extracts specific data attribute(s) from exisiting dataset(s) and stores it in a list of dictionaries.
        The outputted list can then be used as an input to extract additional data from other NBA Statisitcs JSON Endpoints.

        Use Case: Retrieve all game ids and game dates in a list of dictionaries to use in retrieving box score data for each game

        Parameters
        ----------
        input_list_of_dicts : list
            List of dictionaries
        data_attributes : list
            List of strings 

        Returns
        ----------
        list
            List of dictionaries that contains the specified data attributes

        Example Format: output_list = [{'gameId':'0012100001','startDateEastern':'20211003'}, {'gameId': '0012100002', 'startDateEastern': '20211004'}, ...]
        '''

        output_list = []

        for input_dict in input_list_of_dicts:

            temp_dict = {key: value for key,
                         value in input_dict.items() if (key in data_attributes)}
            output_list.append(temp_dict)

        return output_list

    def __str__(self):
        return f"Data Last Refreshed On: {self._date_last_refreshed.strftime('%B %d, %Y')}"
