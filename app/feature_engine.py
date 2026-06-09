
#model input feature engineering
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Match

#define a function to get the last 5 matches
def get_last_matches(team: str, db: Session):

    matches = (
        db.query(Match)
        .filter(
            or_(
                Match.HomeTeam == team,
                Match.AwayTeam == team
            )
        )
        .order_by(
            Match.UtcDate.desc()
        )
        .limit(5)
        .all()
    )

    return matches



