from flask import Flask, jsonify
from flask_cors import CORS
from data_pipeline import get_player_stats
from model import build_features, train_model, predict
from nba_api.stats.endpoints import scoreboardv2, commonteamroster
from nba_api.stats.static import teams
import pandas as pd
import time

app = Flask(__name__)
CORS(app)

all_teams = teams.get_teams()
team_lookup = {team['id']: team['abbreviation'] for team in all_teams}
team_id_lookup = {team['abbreviation']: team['id'] for team in all_teams}

@app.route('/')
def home():
    return jsonify({"message": "Baseline API is running"})

@app.route('/games')
def get_games():
    try:
        scoreboard = scoreboardv2.ScoreboardV2()
        games = scoreboard.get_data_frames()[0]
        game_list = []
        seen = set()
        for _, game in games.iterrows():
            game_id = game["GAME_ID"]
            if game_id in seen:
                continue
            seen.add(game_id)
            game_list.append({
                "game_id": game_id,
                "home_team": team_lookup.get(game["HOME_TEAM_ID"], "Unknown"),
                "away_team": team_lookup.get(game["VISITOR_TEAM_ID"], "Unknown"),
                "status": game["GAME_STATUS_TEXT"]
            })
        return jsonify({"games": game_list})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/predict/<home_team>/<away_team>')
def predict_game(home_team, away_team):
    results = {"home_team": home_team, "away_team": away_team, "predictions": {"home": [], "away": []}}
    
    for side, team_abbr, is_home in [("home", home_team, 1), ("away", away_team, 0)]:
        try:
            team_id = team_id_lookup.get(team_abbr.upper())
            if not team_id:
                continue
            roster = commonteamroster.CommonTeamRoster(team_id=team_id)
            players = roster.get_data_frames()[0]
            time.sleep(1)
            
            for _, player in players.iterrows():
                player_name = player["PLAYER"]
                try:
                    df = get_player_stats(player_name)
                    if df is None or len(df) < 10:
                        continue
                    df = build_features(df)
                    model = train_model(df)
                    opponent = away_team if is_home else home_team
                    predicted_pts = predict(model, df, opponent, is_home)
                    results["predictions"][side].append({
                        "player": player_name,
                        "predicted_points": round(float(predicted_pts), 1)
                    })
                    time.sleep(0.5)
                except Exception:
                    continue
        except Exception as e:
            results["predictions"][side] = {"error": str(e)}
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)