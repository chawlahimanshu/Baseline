import time
import os
import json
from nba_api.stats.endpoints import playergamelog, scoreboardv2, commonteamroster
from nba_api.stats.static import players, teams
import pandas as pd
import requests

all_players = players.get_players()

CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

def get_player_id(player_name):
    for player in all_players:
        if player['full_name'].lower() == player_name.lower():
            return player['id']
    return None

def get_player_stats(player_name):
    cache_file = os.path.join(CACHE_DIR, f"{player_name.replace(' ', '_')}.csv")
    
    # Return cached data if it exists and is from today
    if os.path.exists(cache_file):
        modified_time = os.path.getmtime(cache_file)
        if time.time() - modified_time < 86400:  # 24 hours
            return pd.read_csv(cache_file)
    
    player_id = get_player_id(player_name)
    if player_id is None:
        return None
    
    all_years_data = []
    for season in ['2021-22', '2022-23', '2023-24', '2024-25']:
        try:
            gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season)
            df = gamelog.get_data_frames()[0]
            df = df[['GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV']]
            all_years_data.append(df)
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching {season}: {e}")
    
    if not all_years_data:
        return None
        
    combined = pd.concat(all_years_data, ignore_index=True)
    combined.to_csv(cache_file, index=False)
    return combined

def getInjuryReport():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/injuries"
    response = requests.get(url)
    data = response.json()
    injured_players = {}
    for team in data['injuries']:
        for player in team['injuries']:
            name = player['athlete']['displayName']
            status = player['status']
            details = player.get('shortComment', 'No details')
            team_name = team['displayName']
            injured_players[name] = {
                'status': status,
                'details': details,
                'team': team_name
            }
    return injured_players

def get_team_injuries(team1, team2):
    injuries = getInjuryReport()
    team_injuries = {team1: [], team2: []}
    for player, info in injuries.items():
        if team1.lower() in info['team'].lower():
            team_injuries[team1].append((player, info['status']))
        elif team2.lower() in info['team'].lower():
            team_injuries[team2].append((player, info['status']))
    return team_injuries