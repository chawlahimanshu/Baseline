from nba_api.stats.endpoints import playergamelog, scoreboardv2, commonteamroster
from nba_api.stats.static import players, teams
import pandas as pd
import requests

# ============================================================
# SECTION 1 - PLAYER STATS
# ============================================================

# Load all players once at the top so we don't call it repeatedly
all_players = players.get_players()

def get_player_id(player_name):
    """Convert a player name to their NBA ID"""
    for player in all_players:
        if player['full_name'].lower() == player_name.lower():
            return player['id']
    return None

def get_player_stats(player_name):
    """Pull last 10 games for a player"""
    player_id = get_player_id(player_name)
    
    if player_id is None:
        print(f"Player '{player_name}' not found.")
        return None
    
    # Try current season first, fall back to last season
    for season in ['2025-26', '2024-25']:
        try:
            gamelog = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=season
            )
            df = gamelog.get_data_frames()[0]
            if len(df) > 0:
                print(f"Found {len(df)} games in {season} season")
                break
        except:
            continue
    
    # Take only last 10 games
    df = df.head(10)
    
    # Save to CSV
    filename = f"../data/{player_name.replace(' ', '_')}_last10.csv"
    df.to_csv(filename, index=False)
    print(f"Saved last 10 games to {filename}")
    
    return df

def get_rolling_averages(df, windows=[5, 10]):
    """Calculate rolling averages for key stats"""
    stats = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'MIN']
    
    for window in windows:
        for stat in stats:
            if stat in df.columns:
                df[f'{stat}_last_{window}'] = df[stat].rolling(window).mean()
    
    return df

# ============================================================
# SECTION 2 - INJURY REPORT
# ============================================================

def get_injury_report():
    """Pull current NBA injury report from ESPN"""
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/injuries"
    response = requests.get(url)
    data = response.json()
    
    injured_players = {}
    
    for team in data['injuries']:
        for player in team['injuries']:
            name = player['athlete']['displayName']
            status = player['status']
            detail = player.get('shortComment', 'No details')
            injured_players[name.lower()] = {
                'status': status,
                'detail': detail
            }
    
    return injured_players

# ============================================================
# SECTION 3 - TODAY'S ROSTER + INJURY STATUS
# ============================================================

def get_team_players_today(team_name):
    """Show who is playing today for a team and their injury status"""
    
    # Step 1 - find the team ID
    all_teams = teams.get_teams()
    matching = [t for t in all_teams if team_name.lower() in t['full_name'].lower()]
    
    if not matching:
        print(f"Team '{team_name}' not found.")
        return None
    
    team = matching[0]
    team_id = team['id']
    print(f"Found team: {team['full_name']} (ID: {team_id})")
    
    # Step 2 - check if team is playing today
    board = scoreboardv2.ScoreboardV2()
    games_df = board.get_data_frames()[0]
    
    team_playing = games_df[
        (games_df['HOME_TEAM_ID'] == team_id) |
        (games_df['VISITOR_TEAM_ID'] == team_id)
    ]
    
    if len(team_playing) == 0:
        print(f"{team['full_name']} are not playing today.")
        return None
    
    print(f"{team['full_name']} are playing today!")
    
    # Step 3 - get their roster
    roster = commonteamroster.CommonTeamRoster(team_id=team_id)
    roster_df = roster.get_data_frames()[0]
    
    # Step 4 - get injury report and cross reference
    print("\nCurrent Roster + Injury Status:")
    print("-" * 50)
    injuries = get_injury_report()
    
    active = []
    injured = []
    
    for _, player in roster_df.iterrows():
        name = player['PLAYER']
        position = player['POSITION']
        injury_info = injuries.get(name.lower())
        
        if injury_info:
            status = injury_info['status']
            detail = injury_info['detail']
            injured.append(f"❌ {name} ({position}) — {status}: {detail}")
        else:
            active.append(f"✅ {name} ({position}) — Active")
    
    print("\nACTIVE PLAYERS:")
    for p in active:
        print(p)
    
    print("\nINJURED PLAYERS:")
    for p in injured:
        print(p)
    
    return roster_df


# ============================================================
# RUN IT
# ============================================================

if __name__ == "__main__":
    # Test 1 - get player stats
    print("=" * 50)
    print("PLAYER STATS")
    print("=" * 50)
    df = get_player_stats("LeBron James")
    if df is not None:
        print(df[['GAME_DATE', 'MATCHUP', 'PTS', 'REB', 'AST']].to_string())
    
    # Test 2 - get team roster + injuries
    print("\n" + "=" * 50)
    print("TEAM ROSTER + INJURIES")
    print("=" * 50)
    get_team_players_today("Lakers")