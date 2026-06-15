import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page Config
st.set_page_config(
    page_title="Job Recommendation System",
    page_icon="💼",
    layout="wide"
)

# Load Dataset
df = pd.read_csv("jobs.csv")
st.write(df.columns)

# Simple Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Credentials")

def recommend_jobs(user_skills):
    docs = df["Skill"].tolist()
    docs.append(user_skill)

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(docs)

    scores = cosine_similarity(matrix[-1], matrix[:-1])[0]

    df_copy = df.copy()
    df_copy["Match Score"] = scores

    return df_copy.sort_values(
        by="Match Score",
        ascending=False
    )

if not st.session_state.logged_in:
    login()

else:
    st.title("💼 AI Job Recommendation System")

    st.sidebar.success("Logged In")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    skills = st.text_area(
        "Enter Your Skills",
        placeholder="Python, SQL, Machine Learning"
    )

    if st.button("Recommend Jobs"):

        if skills.strip():

            results = recommend_jobs(skills)

            st.subheader("🎯 Recommended Jobs")

            for _, row in results.iterrows():

                st.card = st.container()

                with st.card:
                    st.markdown(
                        f"""
                        ### {row['Job Title']}
                        **Required Skills:** {row['Skills']}
                        
                        **Match Score:** {row['Match Score']:.2f}
                        """
                    )

                    st.progress(
                        min(
                            int(row["Match Score"] * 100),
                            100
                        )
                    )
