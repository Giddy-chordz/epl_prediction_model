import requests
import pandas as pd

#using football-data.org API to get the matches data for the English Premier League (PL)
url = "https://api.football-data.org/v4/competitions/PL/matches"

#set the headers with the API token for authentication
headers = {
    "X-Auth-Token": "12c0151a71964fcdb24ada0e2381e5fc"
}

res = requests.get(url, headers=headers)
data = res.json()

#print(res.status_code)
#print(res.text)

#extracting the relevant data from the API response and creating a DataFrame
matches = data['matches']
matches_data = []
for match in matches:
    match_info = {
        'match_id': match['id'],
        'utc_date': match['utcDate'],
        'home_team': match['homeTeam']['name'],
        'away_team': match['awayTeam']['name'],
        'status': match['status'],
        'score_full_time_home': match['score']['fullTime']['home'],
        'score_full_time_away': match['score']['fullTime']['away']
    }

    matches_data.append(match_info)

matches_df = pd.DataFrame(matches_data)
print(matches_df.head())