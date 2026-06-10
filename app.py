import streamlit as st
import sqlite3
import pandas as pd

# Database Connection
conn = sqlite3.connect("jobs.db", check_same_thread=False)
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    skill TEXT,
    recommendation TEXT
)
""")
conn.commit()

st.title("Job Recommendation System")

name = st.text_input("Enter Your Name")

skill = st.selectbox(
    "Select Your Skill",
    ["Python", "Java", "HTML/CSS", "Data Analytics"]
)

if st.button("Get Recommendation"):

    if skill == "Python":
        job = "Python Developer"
    elif skill == "Java":
        job = "Java Developer"
    elif skill == "HTML/CSS":
        job = "Web Developer"
    else:
        job = "Data Analyst"

    # Save to Database
    cursor.execute(
        "INSERT INTO users(name, skill, recommendation) VALUES (?, ?, ?)",
        (name, skill, job)
    )
    conn.commit()

    st.success(f"Recommended Job: {job}")

# Show Stored Records
st.subheader("Recommended Candidates")

df = pd.read_sql_query("SELECT * FROM users", conn)

if not df.empty:
    st.dataframe(df)
else:
    st.info("No records found")
