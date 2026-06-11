
#model input feature engineering
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Match

#define a function to get the last 5 matches
def get_home_last_matches(team: str, db: Session):

    matches = (
        db.query(Match)
        .filter(
                Match.HomeTeam == team
        )
        .order_by(
            Match.UtcDate.desc()
        )
        .limit(5)
        .all()
    )

    return matches

#get away last 5 matches
def get_away_last_matches(team: str, db: Session):
    
    matches = db.query(Match).filter(
                                    Match.AwayTeam == team).order_by(
                                        Match.UtcDate.desc()
                                    ).limit(5).all()
    return matches
                                   
#creating a function that gets the total team points for both home and away for the last 5 matches
#home and away form in the last recent games
def home_team_form(team, db: Session):
    matches = get_home_last_matches(team, db)

    total_home_points = 0

    for match in matches:
        
        if match.HomeTeam == team:
            if match.FTHG > match.FTAG:
                total_home_points += 3
            elif match.FTHG < match.FTAG:
                total_home_points += 0
            else:
                total_home_points += 1 

    Home_form_5 = total_home_points/5

    return Home_form_5

#create a function to define the team form when they are away
def away_team_form(team, db: Session):
    total_away_points = 0

    matches = get_away_last_matches(team, db)

    for match in matches:

        if match.AwayTeam == team:

            if match.FTAG > match.FTHG:
                total_away_points += 3
            elif match.FTAG < match.FTHG:
                total_away_points += 0
            else:
                total_away_points += 1
    
    Away_form_5 = total_away_points/5

    return Away_form_5


#create a function to calculate form difference between the home team and away team
def team_form_diff(HomeTeam, AwayTeam, db: Session):
    form_diff = home_team_form(HomeTeam, db) - away_team_form(AwayTeam, db)

    return form_diff


#create a function to define the home and away goals scored in the past 5 games for both home and away team
def total_home_goals(team, db: Session):
    matches = get_home_last_matches(team, db)

    home_team_goals_scored = 0

    home_team_goals_concede = 0

    for match in matches:
            
            home_team_goals_scored += match.FTHG
            home_team_goals_concede += match.FTAG

    home_goal_scored_5 = home_team_goals_scored    
    home_concede_5 = home_team_goals_concede

    home_goal_diff_5 = home_goal_scored_5 - home_concede_5


    return (home_goal_scored_5, 
            home_concede_5,
            home_goal_diff_5)

#define a function to get total goals scored when team are away and the total goal difference
def total_away_goals(team, db: Session):
    matches = get_away_last_matches(team, db)

    total_away_scored = 0
    total_away_concede = 0

    for match in matches:

            total_away_scored += match.FTAG
            total_away_concede += match.FTHG

    away_scored_5 = total_away_scored
    away_concede_5 = total_away_concede

    away_goal_diff_5 = away_scored_5 - away_concede_5

    return (away_scored_5,
            away_concede_5,
            away_goal_diff_5)

#define a function to calculate goal diff strenght of away and home team
def teams_goal_diff(home_team, away_team, db: Session):

    home_goal_scored_5, home_concede_5, home_goal_diff_5 = total_home_goals(home_team, db)

    away_scored_5, away_concede_5, away_goal_diff_5 = total_away_goals(away_team, db)

    goal_diff_strength = home_goal_diff_5 - away_goal_diff_5

    return goal_diff_strength