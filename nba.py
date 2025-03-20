# -*- coding: utf-8 -*-
"""
Created on Thu May 30 09:06:37 2024

@author: HW-T06
"""

from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import teams
from nba_api.stats.static import players
import pandas as pd


# Get all NBA teams
nba_teams = teams.get_teams()
player = players.get_active_players()
# print(nba_teams)



def fetch_players_with_ids():
    player_list = players.get_players()
    return player_list

def main():
    full_name = []
    player_id = []
    df = pd.DataFrame()
    player_list = fetch_players_with_ids()
    print("List of NBA Players with their Player IDs:")
    for player in player_list:
        full_name.append(player['full_name'])
        player_id.append(player['id'])
        # print(f"Name: {player['full_name']}, Player ID: {player['id']}")
    df['Name'] = full_name
    df['Player ID'] = player_id
    print(df)
    

if __name__ == '__main__':
    main()

from nba_api.stats.endpoints import teamdetails

team_id = 1610612744  # Golden State Warriors
team_details = teamdetails.TeamDetails(team_id = team_id)
print(team_details.get_data_frames()[1])
from nba_api.stats.endpoints import teamgamelog

team_id = 1610612743  # Golden State Warriors
gamelog = teamgamelog.TeamGameLog(team_id=team_id, season='2023-24')
print(gamelog.get_data_frames()[0]) 

from nba_api.stats.endpoints import leaguegamefinder

gamefinder = leaguegamefinder.LeagueGameFinder(season_type_nullable='Playoffs', season_nullable='2023-24')
games = gamefinder.get_data_frames()[0]
print(games)

from nba_api.live.nba.endpoints import playbyplay

pbp = playbyplay.PlayByPlay(game_id='0042300315')
play_by_play = pbp.get_dict()
print(play_by_play) 
