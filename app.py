import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------- LOGIN SYSTEM ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Wrong Username or Password")


# ---------------- JOB RECOMMENDATION ----------------

def recommend_jobs(user_skill):

    df = pd.read_csv("jobs.csv")

    vectorizer = TfidfVectorizer()

    skill_vectors = vectorizer.fit_transform(df["Skills"])

    user_vector = vectorizer.transform([user_skill])

    similarity = cosine_similarity(
        user_vector,
        skill_vectors
    )

    df["Match Score"] = similarity[0] * 100

    result = df.sort_values(
        by="Match Score",
        ascending=False
    )

    return result.head(5)

def dashboard():

    st.title("💼 Job Recommendation System")

    job_title = st.text_input("Job Title")

    skills = st.text_input(
        "Skills (Example: Python, SQL, Excel)"
    )

    if st.button("Recommend Jobs"):

        if skills:

            result = recommend_jobs(skills)

            st.subheader("Recommended Jobs")

           st.dataframe(
    result[["Job Title", "Skills", "Match Score"]]
)
        else:
            st.warning("Enter your skills")

# ---------------- MAIN ----------------

if st.session_state.logged_in:
    dashboard()

else:
    login_page()
