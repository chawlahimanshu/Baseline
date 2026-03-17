# Baseline 🏀

> ML-powered NBA player prop prediction engine that helps you make smarter betting decisions.

---

## What It Does

Baseline predicts NBA player point totals for any given matchup using historical game data, rolling performance trends, and real-time injury reports. Enter a player, their opponent, and whether they're home or away — Baseline gives you a data-driven prediction.

---

## Features

- 🔮 **Player Prediction** — XGBoost regression model trained on 4 seasons of NBA game data
- 📊 **Feature Engineering** — Rolling averages, opponent matchup history, rest days, home/away splits
- 🏥 **Injury Awareness** — Real-time injury data via ESPN API
- 🌐 **REST API** — Flask backend serving predictions as JSON *(in progress)*
- 💻 **Dashboard** — React frontend for interacting with predictions *(in progress)*
- ☁️ **Cloud Deployed** — AWS Lambda + S3 + CloudFront with Terraform IaC *(in progress)*

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML Model | XGBoost, scikit-learn, Pandas, NumPy |
| Data Sources | NBA Stats API, ESPN Injury API |
| Backend | Python, Flask |
| Frontend | React |
| Cloud | AWS Lambda, S3, CloudFront |
| Infrastructure | Terraform |
| Version Control | Git, GitHub |

---

## Project Structure

```
baseline/
├── backend/
│   ├── data_pipeline.py   # NBA & ESPN API data ingestion
│   ├── model.py           # Feature engineering + XGBoost model
│   └── app.py             # Flask REST API (in progress)
├── frontend/              # React dashboard (in progress)
├── data/                  # Stored datasets
├── notebooks/             # Exploratory analysis
└── README.md
```

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
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/chawlahimanshu/Baseline.git
cd Baseline

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Run a Prediction

```bash
cd backend
python model.py
```

Then follow the prompts:
```
Enter player name: LeBron James
Enter opponent (e.g. BOS): BOS
Home or away? (1 for home, 0 for away): 0
```

---

## Roadmap

- [x] Data pipeline (NBA Stats API + ESPN Injury API)
- [x] XGBoost prediction model
- [ ] Flask REST API
- [ ] React dashboard
- [ ] AWS deployment with Terraform
- [ ] Improve MAE below 5.0
- [ ] Expand to rebounds and assists props

---

## Author

**Himanshu Chawla**
- GitHub: [@chawlahimanshu](https://github.com/chawlahimanshu)
- LinkedIn: [linkedin.com/in/himanshuchawla-](https://linkedin.com/in/himanshuchawla-)