# src/strava_api/fetch.py
import pandas as pd
import requests
from auth import refresh_access_token

def get_recent_activities(access_token, per_page=5):
    url = 'https://www.strava.com/api/v3/athlete/activities'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'per_page': per_page, 'page': 1}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch activities: {response.text}")
    return response.json()

def save_activities_to_excel(activities, filename="recent_activities.xlsx"):
    df = pd.json_normalize(activities)
    df.to_excel(filename, index=False)
    print(f"📁 Saved {len(activities)} activities to {filename}")

if __name__ == "__main__":
    token = refresh_access_token()
    activities = get_recent_activities(token)
    save_activities_to_excel(activities)
