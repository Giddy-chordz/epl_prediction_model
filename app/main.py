from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from . import feature_engine
from config import API_TOKEN
import requests
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "epl_model.pkl")
encoder_path = os.path.join(BASE_DIR, "label_encoder.pkl")

model = pickle.load(open(model_path, 'rb'))
encoder = pickle.load(open(encoder_path, 'rb'))


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
API_TOKEN = API_TOKEN

HEADERS = {
    "X-Auth-Token": API_TOKEN
}

#endpoint to get standings
@app.get("/standings")
def get_standings():
    url = "https://api.football-data.org/v4/competitions/PL/standings"
    r = requests.get(url, headers=HEADERS)
    return r.json()

#endpoint to get fixtures
@app.get("/fixtures")
def get_fixtures():
    url = "https://api.football-data.org/v4/matches?competitions=PL&status=SCHEDULED&limit=50"
    
    r = requests.get(url, headers=HEADERS)

    # optional safety check
    if r.status_code != 200:
        return {
            "error": "Failed to fetch fixtures",
            "status_code": r.status_code,
            "response": r.text
        }

    return r.json()

#create a prediction endpoint
@app.post('/predict')
def predict(home_team: str, away_team: str, db: Session = Depends(get_db)):


    home_form_5 = feature_engine.home_team_form(home_team, db)
    away_form_5 = feature_engine.away_team_form(away_team, db)

    form_diff = feature_engine.team_form_diff(home_team, away_team, db)

    home_goal_scored_5, home_concede_5, home_goal_diff_5 = feature_engine.total_home_goals(home_team, db)
    away_goal_scored_5, away_concede_5, away_goal_diff_5 = feature_engine.total_away_goals(away_team, db)

    goal_diff_strength = feature_engine.teams_goal_diff(home_team, away_team, db)

    tight_match = abs(goal_diff_strength)

    X_vals = [[
        home_form_5,
        away_form_5,
        form_diff,
        home_goal_scored_5,
        away_goal_scored_5,
        home_concede_5,
        away_concede_5,
        home_goal_diff_5,
        away_goal_diff_5,
        goal_diff_strength,
        tight_match
    ]]

    proba = model.predict_proba(X_vals)[0]

    classes = encoder.classes_

    best_index = proba.argmax()
    prediction = classes[best_index]
    confidence = float(proba[best_index])

    probabilities = {
        cls: float(prob)
        for cls, prob in zip(classes, proba)
    }

    return {
        "home_team": home_team,
        "away_team": away_team,
        "prediction": prediction,
        "confidence": round(confidence, 3),
        "probabilities": probabilities
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)