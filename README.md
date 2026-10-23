# Cricbuzz LiveStats

A real-time cricket match dashboard built using Python and Streamlit. The application fetches cricket match information from the CricketData API and displays match status, scores, teams, venues, and dates.

## Features

- Live cricket match data from an API
- Automatic refresh every 10 minutes
- Manual refresh option
- Match status filtering
- Search matches by keyword
- Match statistics and charts
- Detailed match data table
- API key stored in environment variables

## Technologies Used

- Python
- Streamlit
- Pandas
- Requests
- Streamlit Autorefresh
- Python-dotenv
- CricketData API

## Project Structure

```text
cricbuzz-livestats/
├── app.py
├── cricket_api.py
├── test_api.py
├── requirements.txt
├── .gitignore
└── data/
    └── matches.csv
```

**Security note:** The `.env` file is used locally and must not be uploaded to GitHub.

## Run Locally

1. Clone or download this repository.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```text
   CRICKET_API_KEY=your_api_key_here
   ```

4. Start the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

5. Open the local URL shown in the terminal.

## API Information

This project uses the CricketData API to retrieve cricket match information. API access and data availability depend on the provider's plan and service.

## Disclaimer

This is an independent educational project and is not affiliated with or endorsed by Cricbuzz or CricketData. Match information may be delayed or unavailable. This dashboard is intended for learning and demonstration purposes.
