#ingest live data from football-data api
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from ..models import Match


def data_ingestion(matches, db: Session):

    for match in matches:

        new_match = Match(
            id=match["id"],
            UtcDate=match["utcDate"],
            HomeTeam=match["homeTeam"]["name"],
            AwayTeam=match["awayTeam"]["name"],
            FTHG=match["score"]["fullTime"]["home"],
            FTAG=match["score"]["fullTime"]["away"]
        )

        db.add(new_match)

    db.commit()