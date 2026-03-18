# Baseline 🏀

> ML-powered NBA player prop prediction engine that helps you make smarter betting decisions.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18-61DAFB)
![Flask](https://img.shields.io/badge/Flask-REST%20API-green)
![XGBoost](https://img.shields.io/badge/ML-XGBoost-orange)

---

## What It Does

Baseline predicts NBA player point totals for any given matchup using historical game data, rolling performance trends, and real-time injury reports. Select a game from today's schedule — Baseline shows every player on both rosters with a data-driven point prediction.

---

## Features

- 🏀 **Live Game Schedule** — pulls today's NBA games in real time
- 🔮 **Player Predictions** — XGBoost regression model trained on 4 seasons of NBA data
- 📊 **Feature Engineering** — rolling averages, opponent matchup history, rest days, home/away splits
- 🏥 **Injury Awareness** — real-time injury data via ESPN API
- ⚡ **Smart Caching** — player stats cached locally to prevent API rate limiting
- 🌐 **REST API** — Flask backend serving predictions as JSON
- 💻 **React Dashboard** — clean dark UI for browsing games and predictions
- ☁️ **AWS Deployment** — Lambda + S3 + CloudFront with Terraform *(in progress)*

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML Model | XGBoost, scikit-learn, Pandas, NumPy |
| Data Sources | NBA Stats API, ESPN Injury API |
| Backend | Python, Flask, Flask-CORS |
| Frontend | React, Axios |
| Cloud | AWS Lambda, S3, CloudFront *(in progress)* |
| Infrastructure | Terraform *(in progress)* |
| Version Control | Git, GitHub |

---

## Project Structure

```
baseline/
├── backend/
│   ├── data_pipeline.py   # NBA & ESPN API data ingestion + caching
│   ├── model.py           # Feature engineering + XGBoost model
│   └── app.py             # Flask REST API
├── frontend/
│   └── src/
│       ├── App.js         # Main React component
│       └── App.css        # Styling
├── data/                  # Local cache (gitignored)
├── notebooks/             # Exploratory analysis
├── requirements.txt       # Python dependencies
└── README.md
```

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Health check |
| `GET /games` | Today's NBA games with team abbreviations and tip-off times |
| `GET /predict/<home>/<away>` | Point predictions for every player on both rosters |

---

## Model Performance

| Metric | Value |
|---|---|
| Algorithm | XGBoost Regression |
| Training Data | 4 NBA Seasons (2021–2025) |
| Games Trained On | 250+ per player |
| Mean Absolute Error | 7.2 points |

---

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- pip

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/chawlahimanshu/Baseline.git
cd Baseline

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run Flask API
cd backend
python app.py
```

API runs at `http://127.0.0.1:5000`

### Frontend Setup

```bash
# In a new terminal
cd frontend
npm install
npm start
```

App runs at `http://localhost:3000`

---

## Roadmap

- [x] Data pipeline (NBA Stats API + ESPN Injury API)
- [x] XGBoost prediction model
- [x] Smart caching layer
- [x] Flask REST API
- [x] React dashboard
- [ ] AWS deployment with Terraform
- [ ] Improve MAE below 5.0
- [ ] Add rebounds and assists predictions
- [ ] Player prop comparison vs sportsbook lines

---

## Author

**Himanshu Chawla**
- GitHub: [@chawlahimanshu](https://github.com/chawlahimanshu)
- LinkedIn: [linkedin.com/in/himanshuchawla-](https://linkedin.com/in/himanshuchawla-)