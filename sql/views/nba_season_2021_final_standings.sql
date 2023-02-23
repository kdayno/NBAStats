SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[nba_season_2021_final_standings] AS
    SELECT teams.TeamFullName AS 'Team Name', game_stats.HomeTeamCurrentWinCount AS 'Win Count', game_stats.HomeTeamCurrentLossCount AS ' Loss Count', teams.ConferenceName AS 'Conference'
    FROM [staging].[box_score_basic_game_stats] AS game_stats
    JOIN [staging].[teams] AS teams ON game_stats.HomeTeamTriCode = teams.CityTriCode
    WHERE [GameDate] = '20220410'
    UNION 
    SELECT teams.TeamFullName AS 'Team Name', game_stats.AwayTeamCurrentWinCount AS 'WinCount', game_stats.AwayTeamCurrentLossCount AS ' LossCount', teams.ConferenceName AS 'Conference'
    FROM [staging].[box_score_basic_game_stats] AS game_stats
    JOIN [staging].[teams] AS teams ON game_stats.AwayTeamTriCode = teams.CityTriCode
    WHERE [GameDate] = '20220410'
GO
