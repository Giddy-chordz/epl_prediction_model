#ingest live data from football-data api
from datetime import datetime
from models import Match

def data_ingestion(matches, db):

    for match in matches:

        # STRICT DUPLICATE PREVENTION
        existing = db.query(Match).filter(Match.id == match["id"]).first()
        if existing:
            continue

        if match.get("status") != "FINISHED":
            continue

        utc = datetime.fromisoformat(match["utcDate"].replace("Z", ""))

        new_match = Match(
            id=match["id"],
            HomeTeam=match["homeTeam"]["name"],
            AwayTeam=match["awayTeam"]["name"],
            FTHG=match["score"]["fullTime"]["home"] or 0,
            FTAG=match["score"]["fullTime"]["away"] or 0,
            UtcDate=utc
        )

        db.add(new_match)

    db.commit()