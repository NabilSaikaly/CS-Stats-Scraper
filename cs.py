import requests 
import datetime
from bs4 import BeautifulSoup
import pandas as pd 
import sys

help_message = """
Welcome to the CSGO Stats Scraper by NS - Help Documentation.
This Program allows its users to scrape the latest CSGO Stats for Top Players and teams,
without being limited by the website's Time Filter, hence cs.py will allow the user to surf the whole database.

-- Below are the methods on how to run this program -- 

The Faster Usage Ability (From the CMD/TERMINAL directly) can be performed in 3 methods:
Method 1 (Specifying Start Date & End Date) Example:
	py cs.py 2022-07-03 2022-10-23
Method 2 (Specifying Start Date only, End Date will be considered as of today) Example:
	py cs.py 2022-07-03
Method 3 (Searching for a specific player's stats!) Example searching for player name 'Nabil':
	py cs.py search for Nabil

The Regular Usage, is by running the program normally from the CMD/TERMINAL,
the flow of execution will be explained in run-time.

The Program allows its users to:
1- TPT: Search for the Top Players and Teams, for a specific time range upon user's request or ALL Time Stats.
2- SP: Search for a specific player in the top leaderboards and retrieve this player's stats.


Thanks for using our CSGO Stats Scraper.
github: nabilsaikaly 

Happy Gaming! May you find your name up there!"""

# This Block is intended for the Faster Usage Ability of cs.py (For experienced cs.py end-users)
arguments_list = sys.argv
if (len(arguments_list) > 1):
	regular_flow_execution = False
	target_player_bool = False
	if len(arguments_list) == 2:
		year,month,day = arguments_list[1].split("-")
		startDate = datetime.date(int(year),int(month),int(day))
		endDate = datetime.date.today()
	elif len(arguments_list) == 3:
		year,month,day = arguments_list[1].split("-")
		startDate = datetime.date(int(year),int(month),int(day))
		year,month,day = arguments_list[2].split("-")
		endDate = datetime.date(int(year),int(month),int(day))
		if (endDate > datetime.date.today()):
			endDate = datetime.date.today()
	elif len(arguments_list) == 4:
		if ( (arguments_list[1].lower() == "search") and (arguments_list[2].lower() == "for") ):
			quick_search_bool = True
			target_player = arguments_list[3]
			target_player_bool = True
		else:
			quick_search_bool = False
			quit()
else:
	regular_flow_execution = True



# Functions constructing cs.py:

def date_logic(start_end):
	"""Logical evaluation of the dates given by the user"""
	date_input = input(start_end)
	if (date_input.lower()=='today'):
		return datetime.date.today()
	else:
		year,month,day = date_input.split("-")
		evaluated_date = datetime.date(int(year),int(month),int(day))
		if (evaluated_date> datetime.date.today()):
			print(f"User specified a future date, results will be fetched up till today's date: {datetime.date.today()}")
			evaluated_date = datetime.date.today()
		return evaluated_date


def range_constructor():
	"""Constructs the date-range upon which to retrieve the stats, uses date_logic() to evaluate given dates"""
	alltime_request = input("[Y] To Retrieve the All Time Top Stats - [N] To specify date range, Choose between Y/N: ")
	if alltime_request.lower() == "y":
		startDate, endDate = None, None
	else:
		message = """	
		[+] Enter the 'From' and 'To' Dates upon which to retrieve the stats.
		[+] Use the following format: YYYY-MM-DD
		[!] Enter 'Today' if you require today's date.\n"""
		print(message)
		startDate = date_logic("From: ")
		endDate = date_logic("To: ")
	return startDate, endDate
	


def top_players_teams(startDate, endDate):
	"""The Function that scrapes statistics of top teams and players from the website and generates the reports"""
	if (startDate==None) and (endDate==None):
		url ="https://www.hltv.org/stats"
	else:
		url =f"https://www.hltv.org/stats?startDate={startDate}&endDate={endDate}"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')

	top_players_list = list()
	player_ranking_list = list()
	player_maps_list = list()

	top_teams_list = list()
	team_ranking_list = list()
	team_maps_list = list()

	all_top_players_info = soup.find_all('div', class_="col")[0]
	all_top_teams_info = soup.find_all('div',class_="col")[1]

	# Top Players Scraper 
	for player in all_top_players_info:
		if str(type(player)) == "<class 'bs4.element.Tag'>":
			player = str(player)
			player_soup = BeautifulSoup(player,'html.parser')
			try:
				player_name = player_soup.find('div', class_ = "top-x-box standard-box").find('a', class_="name").string
			except AttributeError:
				pass
			else:
				player_rating = player_soup.find('div', class_="rating").find('span').string
				player_nb_maps = player_soup.find('div', class_ = "average gtSmartphone-only").find('span').string
				top_players_list.append(player_name)
				player_ranking_list.append(player_rating)
				player_maps_list.append(player_nb_maps)

	# Top Teams Scraper 
	for team in all_top_teams_info:
		if str(type(team)) == "<class 'bs4.element.Tag'>":
			team = str(team)
			team_soup = BeautifulSoup(team,'html.parser')
			try:
				team_name = team_soup.find('div',class_ ="top-x-box standard-box").find('a', class_="name").string
			except AttributeError:
				pass
			else:
				team_rating = team_soup.find('div', class_="rating").find('span').string
				team_nb_maps = team_soup.find('div', class_="average gtSmartphone-only").find('span').string
				top_teams_list.append(team_name)
				team_ranking_list.append(team_rating)
				team_maps_list.append(team_nb_maps)

	# Table Reports Generator in top_players_teams(startDate, endDate)
	player_table_report = pd.DataFrame(data={'Player   ':top_players_list, 'Rating':player_ranking_list, '  Maps':player_maps_list})
	team_table_report = pd.DataFrame(data={'Team   ':top_teams_list, 'Rating':team_ranking_list, '  Maps':team_maps_list})
	request = input("Retrieve reports for players/teams/both: ")
	if request.lower()=="players":
		print("\nTop Players: ","\n",player_table_report)
	elif request.lower()=="teams":
		print("\n\nTop Teams: ","\n",team_table_report)
	else:
		print("\nTop Players: ","\n",player_table_report)
		print("\n\nTop Teams: ","\n",team_table_report)
	

def find_player_stats(target_player, df):
	"""Determines stats of a user specified player, given the dataframe to scrape"""
	target_player_name_count = 0
	for player_number in range(0,len(df)-1):
		if df.iloc[player_number]['Player'] == target_player:
			print("\n")
			print(df.iloc[player_number])
			target_player_name_count += 1
	if target_player_name_count == 0:
		print(f"[!ERROR!] {target_player} couldn't be found in the top leaderboards.\n[!] Player Names are CASE Sensitive.")

def all_players_list():
	"""Function that retrieves ALL players from the top leaderboards,
	and allows the user to search for a specific player using find_player_stats(target_player) function"""
	url = "https://www.hltv.org/stats/players"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	players_name_list=list()
	maps_list=list()
	rounds_list=list()
	k_d_diff_list=list()
	k_d_list=list()
	rating_list=list()
	players_dictionary = {"Player":players_name_list, "Maps":maps_list, "Rounds":rounds_list, "K-D Diff":k_d_diff_list, "K/D":k_d_list, "Rating":rating_list}

	for element_tag in soup.find_all("tbody"):
		for row in element_tag.find_all("tr"):
			count=0
			for col in row.find_all("td"):
				col = str(col)
				player_soup = BeautifulSoup(col, "html.parser")
				try:
					name = player_soup.find('a').string
				except:
					pass
				else:
					if str(type(name)) == "<class 'bs4.element.NavigableString'>":
						players_name_list.append(name)			
				if count == 2:
					maps_list.append(player_soup.string)
				elif count == 3:
					rounds_list.append(player_soup.string)
				elif count == 4:
					k_d_diff_list.append(player_soup.string)
				elif count == 5:
					k_d_list.append(player_soup.string)
				elif count == 6:
					rating_list.append(player_soup.string)
				count += 1
	df = pd.DataFrame(data=players_dictionary)


	if (target_player_bool == True): #Handling the Fast Usage Ability of cs.py
		find_player_stats(target_player, df)
	
	elif (target_player_bool == False): #Handling the Regular Usage Ability of cs.py
		print(f"\nRetrieved Stats for {len(df)} TOP players in CSGO!")
		request = input(f"Specify player name to retrieve his/her starts or 'ALL' to show ALL {len(df)} players' stats: ")
		if request.lower() == "all":
			print(df.head(len(df)-1))
		else:
			find_player_stats(request, df)




## Main Method controlling the actual flow of execution

#Main Method for the Regular Usage of cs.py
if (regular_flow_execution == True):
	active=True 
	while (active==True):
		user_request = input("\nSpecify your request from: TPT, SP, H for Help and X to exit the program: ")
		if user_request.lower() == "tpt":
			startDate, endDate = range_constructor()
			top_players_teams(startDate, endDate)

		elif user_request.lower() == "sp":
			target_player_bool = False
			all_players_list()

		elif user_request.lower() == 'h':
			print(help_message + " \n")

		elif user_request.lower() == "x":
			print("\n\n Thanks for using our CSGO Stats Scraper - github: nabilsaikaly - Happy Gaming!")
			active=False

#Main Method for the Faster Usage Ability of cs.py
elif (regular_flow_execution == False):
	if len(arguments_list) == 4:
		all_players_list()
	else:
		top_players_teams(startDate, endDate)
