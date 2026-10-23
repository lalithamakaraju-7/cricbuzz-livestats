
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)

API_URL = "https://api.cricapi.com/v1/currentMatches"


def get_live_matches():
    api_key = os.getenv("CRICKET_API_KEY")

    if not api_key:
        raise ValueError(
            "CRICKET_API_KEY is missing. Check your .env file."
        )

    response = requests.get(
        API_URL,
        params={"apikey": api_key, "offset": 0},
        timeout=20,
    )
    response.raise_for_status()

    result = response.json()

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
            f"{s.get('r', 0)}/{s.get('w', 0)} "
            f"({s.get('o', 0)} overs)"
            for s in scores
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
