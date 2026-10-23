
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CRICKET_API_KEY")

if not api_key:
    print("API key not found. Check your .env file.")
else:
    url = "https://api.cricapi.com/v1/currentMatches"

    try:
        response = requests.get(
            url,
            params={"apikey": api_key, "offset": 0},
            timeout=20
        )

        print("HTTP status:", response.status_code)

        if response.ok:
            data = response.json()
            print("API response received.")
            print("Response status:", data.get("status", "Not provided"))
            print("Matches returned:", len(data.get("data", [])))

            if data.get("status") != "success":
                print("The API reported an error. Check your API account.")

        else:
            print("API request failed. Check your API key and API documentation.")

    except requests.RequestException:
        print("Connection error. Check your internet connection and try again.")
