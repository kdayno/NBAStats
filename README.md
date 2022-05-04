NBA War Room Dashboard 
======

## What is the project?

The purpose of the NBA War Room Dashboard project is to build a dashboard that is inspired by the Toronto Raptor's "War Room". The goal is provide insights and analysis into the league, teams, and players within the NBA. The dashboard will consist of three reports: League Analysis, Player Analysis, and Team analysis. Each report will contain a variety of data visuals. The data to support the dashboard will be sourced from publicly available JSON endpoints that contain NBA statistical data and will be stored in a Microsoft SQL Server database.

The project will be built using the following technologies for each component:
- Data Pipeline: Python
- Data Visualization: Dash
- Deployment & Hosting: Docker & Heroku

## What is the MVP?

The minimum viable product is a dashboard that renders in a web browser and is accessible via the Internet.

## Technical Architecture Diagram

![Technical Architecture Diagram](/Users/kdayno/Development/02-PROJECTS/NBAWarRoomDashboard/docs/NBAWarRoomDashboard_SolutionArchitecture_v1.0.png)

## Technologies
- Python
  - Pandas
  - Requests
  - SQLAlchemy
- Microsoft SQL Server
- Dash
- Docker
- Heroku



## Resources

<i> A list of articles, videos, websites, and books used during development and deployment.</i>

### Development
- [Docker Handbook](https://www.freecodecamp.org/news/the-docker-handbook/)
- [Pandas Datatypes](https://pbpython.com/pandas_dtypes.html)
- [SQLAlchemy Datatypes](https://docs.sqlalchemy.org/en/14/core/type_basics.html)
- [Pandas Creating Dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
- [Pandas Changing Column Datatypes](https://stackoverflow.com/questions/15891038/change-column-type-in-pandas)
- [TSQL Convert getdate() to EST](https://stackoverflow.com/questions/4712616/convert-getdate-to-est)
- [TSQL AT TIME ZONE function](https://docs.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql?view=sql-server-ver15)
- [Sleep method in Python Time module (built-in module)](https://docs.python.org/3/library/time.html#time.sleep)
- [Python Delete element from Dictionary](https://stackoverflow.com/questions/5844672/delete-an-element-from-a-dictionary)
- [Python Check for Object Type wiht isinstance()](https://stackoverflow.com/questions/25231989/how-to-check-if-a-variable-is-a-dictionary-in-python)
- [Python isinstance() function](https://www.w3schools.com/python/ref_func_isinstance.asp)
- [Table Design Best Practices for ETL](https://towardsdatascience.com/table-design-best-practices-for-etl-200accee9cc9)
- [Pandas Insert Column into DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.insert.html)
- [SQL Alchemy Working with Engine & Connections; Creating multilple connections](https://docs.sqlalchemy.org/en/13/core/connections.html#basic-usage)
- [Pandas Function for Rearranging Columns in Dataframe](https://towardsdatascience.com/reordering-pandas-dataframe-columns-thumbs-down-on-standard-solutions-1ff0bc2941d5)
- [Data Project Folder Structure](https://dzone.com/articles/data-science-project-folder-structure)

### Deployment