# CS-Stats-Retriever: cs.py
This program retrieves the latest Counter-Strike: Global Offensive Game (CS:GO) stats for Top Players and Top Teams.
It consists of a web scraper that scrapes [H1TV](https://www.hltv.org)'s database and retrieves the corresponding stats upon the end-user's request/filtering.
Other than CS:GO players, this program is useful to anyone who wants to learn webscraping via Python's Requests, BS4-BeautifulSoup and some pandas (to create DataFrames).

## Python Libraries Required
- requests
- bs4
- pandas
- datetime
- sys

## Benefits of this program
Several CSGO Players reached out and addressed that they need a program to scrape H1TV's stats since it is the most reliable website
and they need to do it directly while playing their game or in the lobby, without actually opening a web-browser, going to the website, specifying the filtering
requirements and viewing the reports.
"cs.py" fulfills these requirements and is able to data-scrape H1TV's database and filter on specific date-ranges to retrieve the required reports. In addition, the program allows its end-users to search for a specific player and retrieve his/her performance and stats if the player belongs to the Top Players Tier.
There are two main executions to run this program:
- **The Faster Ability Usage** (achieved by listing specific arguments)
- **The Regular Usage**


## Program Documentation (Also available while running the program)


**The Faster Usage Ability** (From the CMD/TERMINAL with specific arguments) can be performed in 3 methods:
1. Specifying Start Date & End Date where Date Format is YYYY-MM-DD: 
	- `python3 cs.py 2022-07-03 2022-10-23`
2. Specifying Start Date only, End Date will be considered as of today:
	- `python3 cs.py 2022-07-03`
3. Searching for a specific player's stats! Example searching for player name 'Nabil':
	- `python3 cs.py search for Nabil`



**The Regular Usage**, is by running the program normally from the CMD/TERMINAL,
the flow of execution is explained in run-time.
The Program will prompt the user to choose between 'TPT' or 'SP':
1. TPT: Search for the Top Players and Teams of All Time or given a specific time range upon user's request.
2. SP: Search for a specific player in the top leaderboards and retrieve this player's stats.


Thanks for using cs.py, for any technical questions concerning the code or related to the program itself please feel free to reach out on saikalyn@gmail.com

Nabil
