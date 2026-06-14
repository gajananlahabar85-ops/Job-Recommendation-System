import streamlit as st
import sqlite3
import pandas as pd

# Database Connection
conn = sqlite3.connect("jobs_system.db", check_same_thread=False)
cursor = conn.cursor()

# User Login Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS login (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()

# Recommendation Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    skill TEXT,
    recommendation TEXT
)
""")

conn.commit()

# Default Login
cursor.execute("SELECT * FROM login")
if cursor.fetchone() is None:
    cursor.execute(
        "INSERT INTO login(username,password) VALUES (?,?)",
        ("admin","1234")
    )
    conn.commit()


# Login Function
def check_login(username, password):
    cursor.execute(
        "SELECT * FROM login WHERE username=? AND password=?",
        (username,password)
    )
    return cursor.fetchone()


# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Login Page
if not st.session_state.logged_in:

    st.title("Job Recommendation System Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if check_login(username,password):
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Login")


# Main Project
else:

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


        cursor.execute(
            "INSERT INTO users(name,skill,recommendation) VALUES (?,?,?)",
            (name,skill,job)
        )

        conn.commit()

        st.success(f"Recommended Job: {job}")


    st.subheader("Recommended Candidates")

    df = pd.read_sql_query(
        "SELECT * FROM users",
        conn
    )

    st.dataframe(df)


    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
