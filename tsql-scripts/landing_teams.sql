CREATE TABLE [dbo].[landing_teams](
	[city] [varchar](50) NULL,
	[fullName] [varchar](50) NULL,
	[isNBAFranchise] [bit] NULL,
	[confName] [varchar](10) NULL,
	[tricode] [varchar](10) NULL,
	[teamShortName] [varchar](50) NULL,
	[divName] [varchar](50) NULL,
	[isAllStar] [bit] NULL,
	[nickname] [varchar](50) NULL,
	[urlName] [varchar](50) NULL,
	[teamId] [varchar](100) NULL,
	[altCityName] [varchar](50) NULL,
	[created_timestamp] [datetime] NOT NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[landing_teams] ADD  CONSTRAINT [DF_landing_teams_created_timestamp]  DEFAULT CONVERT(DATETIME,GETDATE() AT TIME ZONE CURRENT_TIMEZONE_ID() AT TIME ZONE 'Eastern Standard Time') FOR [created_timestamp]
GO

