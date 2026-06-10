from fastapi import FastAPI, response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from . import feature_engine
import pickle

model = pickle.load(open('epl_model.pkl', 'rb'))
encoder = pickle.load(open('label_encoder.pkl', 'rb'))

app = FastAPI()

#create a prediction endpoint
@app.post('/predict')
def predict(home_team: str, away_team: str, db: Session = Depends(get_db)):
    home_team_form_5 = feature_engine.home_team_form(home_team, db)
    away_team_form_5 = feature_engine.away_team_form(away_team,db)

    form_diff = feature_engine.team_form_diff(home_team, away_team, db)

    home_goal_scored_5, home_concede_5, home_goal_diff_5 = feature_engine.total_home_goals(home_team, db)
    away_scored_5, away_concede_5, away_goal_diff_5 = feature_engine.total_away_goals(away_team, db)

    goal_diff_strngth = feature_engine.teams_goal_diff
