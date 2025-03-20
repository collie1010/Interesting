# -*- coding: utf-8 -*-
"""
Created on Fri May 31 09:04:10 2024

@author: HW-T06
"""

import time
from nba_api.live.nba.endpoints import ScoreBoard, playbyplay
import datetime

def fetch_live_games():
    scoreboard = ScoreBoard()
    games = scoreboard.games.get_dict()
    live_games = [game for game in games if game['gameStatus'] == 2]  # Status 2 indicates the game is live
    return live_games

def fetch_play_by_play(game_id):
    pbp = playbyplay.PlayByPlay(game_id=game_id)
    return pbp.get_dict()['game']['actions']

def display_latest_play_by_play(game):
    game_id = game['gameId']
    play_by_play = fetch_play_by_play(game_id)
    latest_plays = play_by_play[-6:]  # Get the last 5 play-by-play events

    home_team = game['homeTeam']['teamName']
    away_team = game['awayTeam']['teamName']

    descriptions = []

    for play in latest_plays:
        description = play['description']
        
        # Attach team name if the play involves a player
        if 'teamTricode' in play:
            team_tricode = play['teamTricode']
            description = f"{team_tricode}: {description}"
        
        descriptions.append(description)

    return descriptions

def main():
    while True:
        live_games = fetch_live_games()
        
        if not live_games:
            print("No live games currently.")
        else:
            for game in live_games:
                game_id = game['gameId']
                home_team = game['homeTeam']['teamName']
                away_team = game['awayTeam']['teamName']
                home_score = game['homeTeam']['score']
                away_score = game['awayTeam']['score']
                status = game['gameStatusText']
                
                print(f"{away_team} vs {home_team}: {away_score} - {home_score} ({status})")
                
                # Fetch and print the latest 5 play-by-play events with team names
                print("Latest plays:")
                descriptions = display_latest_play_by_play(game)
                for desc in reversed(descriptions):
                    print(desc)
        
        
        print("\n---\n")
        time.sleep(15)

if __name__ == '__main__':
    main()
