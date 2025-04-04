# src/strava_api/auth.py
import json
import os
import requests
from pathlib import Path

# --- Strava App Credentials ---
CLIENT_ID = '154461'
CLIENT_SECRET = '7e89b8fc0a1f182e0aa48cb6f044e7aba23fea66'

# --- File to store access and refresh tokens ---
TOKEN_FILE = Path(__file__).parent / 'tokens.json'

def save_tokens(tokens):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f)

def load_tokens():
    if not TOKEN_FILE.exists():
        raise FileNotFoundError("Token file not found. Run auth_flow() to create it.")
    with open(TOKEN_FILE) as f:
        return json.load(f)

def refresh_access_token():
    tokens = load_tokens()
    refresh_token = tokens['refresh_token']

    response = requests.post(
        url='https://www.strava.com/oauth/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
    )

    if response.status_code != 200:
        raise Exception(f"❌ Failed to refresh token: {response.text}")

    new_tokens = response.json()
    save_tokens(new_tokens)
    return new_tokens['access_token']

def auth_flow():
    """One-time step: run this after authorizing in browser"""
    code = input("Paste the code from the browser redirect URL: ")

    response = requests.post(
        url="https://www.strava.com/oauth/token",
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
    )

    if response.status_code != 200:
        raise Exception(f"❌ Failed to get tokens: {response.text}")

    tokens = response.json()
    save_tokens(tokens)
    print("✅ Tokens saved to tokens.json!")

# Uncomment to generate tokens (run once after browser auth)
auth_flow()


