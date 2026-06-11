import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.scrape import matches
from app.database import SessionLocal
from app.data_ingestion import data_ingestion

db = SessionLocal()
data_ingestion(matches, db)

print("DONE")

db.close()