#ingest live data from football-data api
from datetime import datetime
from models import Match

def data_ingestion(matches, db):

    for match in matches:

        # prevent duplicates
        existing = db.query(Match).filter(Match.id == match["id"]).first()
        if existing:
            continue

        utc = datetime.fromisoformat(
            match["utcDate"].replace("Z", "")
        )

        new_match = Match(
            id=match["id"],
            HomeTeam=match["homeTeam"]["name"],
            AwayTeam=match["awayTeam"]["name"],
            FTHG=match["score"]["fullTime"]["home"],
            FTAG=match["score"]["fullTime"]["away"],
            UtcDate=utc
        )

        db.add(new_match)

    db.commit()