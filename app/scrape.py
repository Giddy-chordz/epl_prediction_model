import requests
from app.database import SessionLocal
from app.data_ingestion import data_ingestion
from app.config import API_TOKEN

url = "https://api.football-data.org/v4/competitions/PL/matches"

headers = {
    "X-Auth-Token": API_TOKEN
}

res = requests.get(url, headers=headers)

if res.status_code != 200:
    print("API failed:", res.text)
    exit()

data = res.json()
matches = data["matches"]

db = SessionLocal()

try:
    data_ingestion(matches, db)
finally:
    db.close()