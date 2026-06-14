from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.secret_key = "secret_key_123"

# Dummy user credentials
USER = {
    "username": "admin",
    "password": "admin123"
}

# Sample jobs
jobs = [
    {"Job Title": "Data Analyst", "Skills": "Python SQL Excel Power BI"},
    {"Job Title": "Machine Learning Engineer", "Skills": "Python Machine Learning TensorFlow"},
    {"Job Title": "Web Developer", "Skills": "HTML CSS JavaScript React"},
    {"Job Title": "Backend Developer", "Skills": "Python Django Flask SQL"},
    {"Job Title": "Data Scientist", "Skills": "Python Pandas NumPy Statistics"}
]

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def authenticate():
    username = request.form["username"]
    password = request.form["password"]

    if username == USER["username"] and password == USER["password"]:
        session["user"] = username
        return redirect(url_for("dashboard"))

    return "Invalid Username or Password"

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    if "user" not in session:
        return redirect(url_for("login"))

    user_skills = request.form["skills"]

    df = pd.DataFrame(jobs)

    docs = df["Skills"].tolist()
    docs.append(user_skills)

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(docs)

    similarity = cosine_similarity(matrix[-1], matrix[:-1])

    df["Score"] = similarity[0]
    results = df.sort_values(by="Score", ascending=False)

    recommendations = results.to_dict(orient="records")

    return render_template(
        "recommendations.html",
        recommendations=recommendations
    )

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
