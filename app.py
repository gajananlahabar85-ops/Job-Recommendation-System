import streamlit as st

st.title("Job Recommendation System")

name = st.text_input("Enter Your Name")

skill = st.selectbox(
    "Select Your Skill",
    ["Python", "Java", "HTML/CSS", "Data Analytics"]
)

if st.button("Get Recommendation"):
    if skill == "Python":
        st.success("Recommended Job: Python Developer")
    elif skill == "Java":
        st.success("Recommended Job: Java Developer")
    elif skill == "HTML/CSS":
        st.success("Recommended Job: Web Developer")
    elif skill == "Data Analytics":
        st.success("Recommended Job: Data Analyst")
