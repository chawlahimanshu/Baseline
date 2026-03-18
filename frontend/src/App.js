
import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/games")
      .then(res => setGames(res.data.games))
      .catch(err => console.error(err));
  }, []);

  const handleGameClick = (game) => {
    setSelectedGame(game);
    setPredictions(null);
    setLoading(true);
    axios.get(`http://127.0.0.1:5000/predict/${game.home_team}/${game.away_team}`)
      .then(res => {
        setPredictions(res.data.predictions);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  return (
    <div className="app">
      <h1>🏀 Baseline</h1>
      <p className="subtitle">NBA Prop Predictions</p>

      {!selectedGame ? (
        <div className="games-grid">
          {games.map(game => (
            <div key={game.game_id} className="game-card" onClick={() => handleGameClick(game)}>
              <div className="teams">{game.away_team} @ {game.home_team}</div>
              <div className="status">{game.status}</div>
            </div>
          ))}
        </div>
      ) : (
        <div className="predictions">
          <button className="back-btn" onClick={() => setSelectedGame(null)}>← Back to Games</button>
          <h2>{selectedGame.away_team} @ {selectedGame.home_team}</h2>

          {loading ? (
            <div className="loading">Loading predictions... this may take a few minutes</div>
          ) : predictions ? (
            <div className="teams-container">
              <div className="team-predictions">
                <h3>{selectedGame.home_team}</h3>
                {predictions.home
                  .sort((a, b) => b.predicted_points - a.predicted_points)
                  .map(p => (
                    <div key={p.player} className="player-row">
                      <span className="player-name">{p.player}</span>
                      <span className="player-pts">{p.predicted_points} pts</span>
                    </div>
                  ))}
              </div>
              <div className="team-predictions">
                <h3>{selectedGame.away_team}</h3>
                {predictions.away
                  .sort((a, b) => b.predicted_points - a.predicted_points)
                  .map(p => (
                    <div key={p.player} className="player-row">
                      <span className="player-name">{p.player}</span>
                      <span className="player-pts">{p.predicted_points} pts</span>
                    </div>
                  ))}
              </div>
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
}

export default App;