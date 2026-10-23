
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)

API_URL = "https://api.cricapi.com/v1/currentMatches"


def get_live_matches():
    """Fetch current cricket matches from CricketData API."""

    api_key = os.getenv("CRICKET_API_KEY")

    if not api_key:
        raise ValueError(
            "CRICKET_API_KEY is missing. Check your .env file "
            "or Streamlit Cloud Secrets."
        )

    try:
        response = requests.get(
            API_URL,
            params={
                "apikey": api_key,
                "offset": 0,
            },
            timeout=20,
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(
                f"Cricket API HTTP error {response.status_code}. "
                f"Response: {response.text[:300]}"
            ) from e

        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError as e:
            raise ValueError(
                "Cricket API returned an invalid JSON response."
            ) from e

    except requests.exceptions.Timeout as e:
        raise ValueError(
            "Cricket API request timed out. Please try again later."
        ) from e

    except requests.exceptions.ConnectionError as e:
        raise ValueError(
            "Could not connect to CricketData API. Check the connection."
        ) from e

    if result.get("status") != "success":
        raise ValueError(
            "Cricket API error: "
            + str(result.get("reason", "Unknown error"))
        )

    matches = []

    for item in result.get("data", []):
        teams = item.get("teams", [])
        scores = item.get("score", [])

        score_text = " | ".join(
            f"{score.get('r', 0)}/{score.get('w', 0)} "
            f"({score.get('o', 0)} overs)"
            for score in scores
        ) or "Score not available"

        matches.append({
            "match": item.get("name", "Unknown match"),
            "team1": teams[0] if len(teams) > 0 else "Unknown",
            "team2": teams[1] if len(teams) > 1 else "Unknown",
            "status": item.get("status", "Status unavailable"),
            "score": score_text,
            "venue": item.get("venue", "Not available"),
            "date": item.get("date", ""),
            "match_type": item.get("matchType", ""),
            "matchStarted": item.get("matchStarted", False),
            "matchEnded": item.get("matchEnded", False),
        })

    return pd.DataFrame(matches)
