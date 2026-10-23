
import os
import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from cricket_api import get_live_matches

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Cricbuzz LiveStats")
st.write("Your Cricket Live Statistics Dashboard")
st.caption("Cricket match information powered by CricketData API.")

# Automatically refresh every 10 minutes
st_autorefresh(
    interval=10 * 60 * 1000,
    key="dashboard_refresh"
)

if st.button("🔄 Refresh Dashboard"):
    st.rerun()

st.divider()

# Load live data; use CSV demo data if the API fails
try:
    with st.spinner("Loading cricket match data..."):
        cricket_data = get_live_matches()

    data_source = "Live CricketData API"

except Exception as error:
    csv_path = os.path.join("data", "matches.csv")

    if os.path.exists(csv_path):
        cricket_data = pd.read_csv(csv_path)
        data_source = "Demo Data (API temporarily unavailable)"

        st.warning(
            "Live data is temporarily unavailable. "
            "Showing demo data instead."
        )

        # Display the reason the API request failed
        st.caption(f"API error details: {error}")

    else:
        st.error(
            "Live data is unavailable and the demo CSV was not found."
        )
        st.caption(f"API error details: {error}")
        st.stop()

# Show which data source is being used
st.caption(f"Data source: {data_source}")

# Make sure the required dashboard columns exist
required_columns = [
    "match",
    "team1",
    "team2",
    "status",
    "score",
    "venue",
    "date",
    "matchStarted",
    "matchEnded"
]

for column in required_columns:
    if column not in cricket_data.columns:
        if column in ["matchStarted", "matchEnded"]:
            cricket_data[column] = False
        else:
            cricket_data[column] = "Not available"

if cricket_data.empty:
    st.warning("No matches are available to display.")

else:
    # Dashboard statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🏏 Total Matches", len(cricket_data))

    with col2:
        started = (
            cricket_data["matchStarted"]
            .astype(str)
            .str.lower()
            .isin(["true", "1"])
        )

        ended = (
            cricket_data["matchEnded"]
            .astype(str)
            .str.lower()
            .isin(["true", "1"])
        )

        st.metric(
            "🔴 Matches In Progress",
            int((started & ~ended).sum())
        )

    with col3:
        teams = (
            set(cricket_data["team1"].dropna().astype(str))
            | set(cricket_data["team2"].dropna().astype(str))
        )

        st.metric("👥 Teams", len(teams))

    st.divider()

    # Filter matches by status
    st.subheader("🔎 Filter Matches")

    statuses = ["All"] + sorted(
        cricket_data["status"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_status = st.selectbox(
        "Choose match status",
        statuses
    )

    if selected_status == "All":
        displayed_matches = cricket_data.copy()
    else:
        displayed_matches = cricket_data[
            cricket_data["status"].astype(str) == selected_status
        ].copy()

    st.caption(
        f"Showing {len(displayed_matches)} "
        f"of {len(cricket_data)} matches"
    )

    # Match cards
    st.subheader("🏏 Match Cards")

    if displayed_matches.empty:
        st.info("No matches found for this status.")

    else:
        for _, match in displayed_matches.iterrows():
            with st.container(border=True):
                st.markdown(f"### {match['match']}")

                left, right = st.columns(2)

                with left:
                    st.write(f"**Team 1:** {match['team1']}")

                with right:
                    st.write(f"**Team 2:** {match['team2']}")

                st.markdown("#### 🏆 Score")
                st.write(match["score"])

                st.info(f"📌 Status: {match['status']}")

                st.write(f"📍 **Venue:** {match['venue']}")

                if (
                    pd.notna(match["date"])
                    and str(match["date"]).strip()
                ):
                    st.caption(f"📅 Match date: {match['date']}")

    st.divider()

    # Chart
    st.subheader("📈 Matches by Status")

    status_counts = (
        cricket_data["status"]
        .fillna("Unknown")
        .value_counts()
    )

    st.bar_chart(status_counts)

    # Search
    st.divider()
    st.subheader("🔍 Search Matches")

    search = st.text_input(
        "Enter a team name or match name",
        placeholder="Example: India"
    )

    if search.strip():
        search_mask = (
            cricket_data["match"]
            .astype(str)
            .str.contains(search, case=False, na=False)
            | cricket_data["team1"]
            .astype(str)
            .str.contains(search, case=False, na=False)
            | cricket_data["team2"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        )

        search_results = cricket_data[search_mask]

        st.write(f"Search results: {len(search_results)}")

        if search_results.empty:
            st.warning("No matching matches found.")

        else:
            st.dataframe(
                search_results,
                width="stretch",
                hide_index=True
            )

    # Full data table
    with st.expander("📋 View All Match Data"):
        st.dataframe(
            cricket_data,
            width="stretch",
            hide_index=True
        )

st.caption(
    "Independent educational project. Match information depends on "
    "the CricketData API. Demo data is shown when the API is unavailable."
)
