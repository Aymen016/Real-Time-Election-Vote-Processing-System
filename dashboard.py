import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import psycopg2

# Function to fetch voting statistics from PostgreSQL database
@st.cache_data(ttl=60)
def fetch_voting_stats():
    conn = psycopg2.connect("host=localhost dbname=voting user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM voters")
    total_voters = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT voter_id) FROM votes")
    participated_voters = cur.fetchone()[0]

    st.metric("Total Registered Voters", total_voters)
    st.metric("Voters Who Participated", participated_voters)

    cur.execute("SELECT count(*) FROM voters")
    voters_count = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM candidates")
    candidates_count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return voters_count, candidates_count

# Function to fetch votes data from PostgreSQL
def fetch_votes_data():
    conn = psycopg2.connect("host=localhost dbname=voting user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("""
        SELECT
            c.candidate_id,
            c.candidate_name,
            c.party_affiliation,
            COUNT(v.voter_id) AS total_votes
        FROM candidates c
        LEFT JOIN votes v ON c.candidate_id = v.candidate_id
        GROUP BY c.candidate_id, c.candidate_name, c.party_affiliation
        ORDER BY total_votes DESC
    """)
    results = cur.fetchall()
    conn.close()
    return results

# Function to plot a bar chart
def plot_colored_bar_chart(results_df):
    plt.figure(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(results_df)))
    plt.bar(results_df['candidate_name'], results_df['total_votes'], color=colors)
    plt.xlabel('Candidate Name')
    plt.ylabel('Total Votes')
    plt.title('Vote Counts Per Candidate')
    plt.xticks(rotation=90)
    return plt

# Function to update and display data
def update_data():
    st.text(f"Last refreshed: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Fetch voting stats
    voters_count, candidates_count = fetch_voting_stats()
    #st.metric("Total Voters", voters_count)
    st.metric("Total Candidates", candidates_count)
    
    # Fetch and process votes data
    results = fetch_votes_data()
    results_df = pd.DataFrame(results, columns=["candidate_id", "candidate_name", "party_affiliation", "total_votes"])

    if results_df.empty:
        st.warning("No data found.")
        return

    # Display the DataFrame
    st.subheader("Election Results")
    st.write(results_df)

    # Identify the leading candidate
    leading_candidate = results_df.iloc[results_df['total_votes'].idxmax()]

    # Display leading candidate information
    st.markdown("---")
    st.header("Leading Candidate")
    st.write(f"Name: {leading_candidate['candidate_name']}")
    st.write(f"Party: {leading_candidate['party_affiliation']}")
    st.write(f"Total Votes: {leading_candidate['total_votes']}")

    # Display charts
    bar_fig = plot_colored_bar_chart(results_df)
    st.pyplot(bar_fig)

# Sidebar for refreshing the data
def sidebar():
    refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 10)
    st_autorefresh(interval=refresh_interval * 1000, key="auto_refresh")
    if st.sidebar.button("Refresh Now"):
        update_data()

# Main App
st.title("Real-time Election Dashboard")
sidebar()
update_data()
