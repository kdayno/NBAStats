SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[nba_season_2021_team_wins] AS
SELECT [GameDate],
    CASE
        WHEN [HomeTeamTriCode] = 'ATL' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'ATL' THEN [AwayTeamCurrentWinCount]
    END AS 'ATL',
    CASE
        WHEN [HomeTeamTriCode] = 'BOS' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'BOS' THEN [AwayTeamCurrentWinCount]
    END AS 'BOS',
    CASE
        WHEN [HomeTeamTriCode] = 'BKN' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'BKN' THEN [AwayTeamCurrentWinCount]
    END AS 'BKN',
    CASE
        WHEN [HomeTeamTriCode] = 'CHA' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'CHA' THEN [AwayTeamCurrentWinCount]
    END AS 'CHA',
    CASE
        WHEN [HomeTeamTriCode] = 'CHI' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'CHI' THEN [AwayTeamCurrentWinCount]
    END AS 'CHI',
    CASE
        WHEN [HomeTeamTriCode] = 'CLE' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'CLE' THEN [AwayTeamCurrentWinCount]
    END AS 'CLE',
    CASE
        WHEN [HomeTeamTriCode] = 'DAL' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'DAL' THEN [AwayTeamCurrentWinCount]
    END AS 'DAL',
    CASE
        WHEN [HomeTeamTriCode] = 'DEN' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'DEN' THEN [AwayTeamCurrentWinCount]
    END AS 'DEN',
    CASE
        WHEN [HomeTeamTriCode] = 'DET' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'DET' THEN [AwayTeamCurrentWinCount]
    END AS 'DET',
    CASE
        WHEN [HomeTeamTriCode] = 'GSW' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'GSW' THEN [AwayTeamCurrentWinCount]
    END AS 'GSW',
    CASE
        WHEN [HomeTeamTriCode] = 'HOU' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'HOU' THEN [AwayTeamCurrentWinCount]
    END AS 'HOU',
    CASE
        WHEN [HomeTeamTriCode] = 'IND' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'IND' THEN [AwayTeamCurrentWinCount]
    END AS 'IND',
    CASE
        WHEN [HomeTeamTriCode] = 'LAC' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'LAC' THEN [AwayTeamCurrentWinCount]
    END AS 'LAC',
    CASE
        WHEN [HomeTeamTriCode] = 'LAL' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'LAL' THEN [AwayTeamCurrentWinCount]
    END AS 'LAL',
    CASE
        WHEN [HomeTeamTriCode] = 'MEM' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'MEM' THEN [AwayTeamCurrentWinCount]
    END AS 'MEM',
    CASE
        WHEN [HomeTeamTriCode] = 'MIA' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'MIA' THEN [AwayTeamCurrentWinCount]
    END AS 'MIA',
    CASE
        WHEN [HomeTeamTriCode] = 'MIL' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'MIL' THEN [AwayTeamCurrentWinCount]
    END AS 'MIL',
    CASE
        WHEN [HomeTeamTriCode] = 'MIN' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'MIN' THEN [AwayTeamCurrentWinCount]
    END AS 'MIN',
    CASE
        WHEN [HomeTeamTriCode] = 'NOP' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'NOP' THEN [AwayTeamCurrentWinCount]
    END AS 'NOP',
    CASE
        WHEN [HomeTeamTriCode] = 'NYK' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'NYK' THEN [AwayTeamCurrentWinCount]
    END AS 'NYK',
    CASE
        WHEN [HomeTeamTriCode] = 'OKC' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'OKC' THEN [AwayTeamCurrentWinCount]
    END AS 'OKC',
    CASE
        WHEN [HomeTeamTriCode] = 'ORL' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'ORL' THEN [AwayTeamCurrentWinCount]
    END AS 'ORL',
    CASE
        WHEN [HomeTeamTriCode] = 'PHI' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'PHI' THEN [AwayTeamCurrentWinCount]
    END AS 'PHI',
    CASE
        WHEN [HomeTeamTriCode] = 'PHX' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'PHX' THEN [AwayTeamCurrentWinCount]
    END AS 'PHX',
    CASE
        WHEN [HomeTeamTriCode] = 'POR' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'POR' THEN [AwayTeamCurrentWinCount]
    END AS 'POR',
    CASE
        WHEN [HomeTeamTriCode] = 'SAC' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'SAC' THEN [AwayTeamCurrentWinCount]
    END AS 'SAC',
    CASE
        WHEN [HomeTeamTriCode] = 'SAS' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'SAS' THEN [AwayTeamCurrentWinCount]
    END AS 'SAS',
    CASE
        WHEN [HomeTeamTriCode] = 'TOR' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'TOR' THEN [AwayTeamCurrentWinCount]
    END AS 'TOR',
    CASE
        WHEN [HomeTeamTriCode] = 'UTA' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'UTA' THEN [AwayTeamCurrentWinCount]
    END AS 'UTA',
    CASE
        WHEN [HomeTeamTriCode] = 'WAS' THEN [HomeTeamCurrentWinCount]
        WHEN [AwayTeamTriCode] = 'WAS' THEN [AwayTeamCurrentWinCount]
    END AS 'WAS'
    FROM [staging].[box_score_basic_game_stats]
    WHERE  [SeasonStageCategoryName] = 'Regular Season'

GO
