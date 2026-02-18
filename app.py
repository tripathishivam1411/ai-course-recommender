from flask import Flask, render_template, request, redirect, session
import recommender
import database

app = Flask(__name__)
app.secret_key = "secret123"

database.create_tables()

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if database.register_user(username, password):
            return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if database.login_user(username, password):
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():

    if "user" not in session:
        return redirect("/login")

    recommendations = []

    if request.method == "POST":

        interest = request.form["interest"]
        results = recommender.recommend_courses(interest)

        for course in results:
            database.save_history(
                session["user"],
                interest,
                course["Course Name"]
            )

        recommendations = results

    return render_template(
        "dashboard.html",
        user=session["user"],
        recommendations=recommendations
    )

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
