from flask import Flask, render_template, request, redirect
import recommender
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def enter():

    if request.method == "POST":
        return redirect("/dashboard")

    return render_template("enter.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    recommendations = []

    if request.method == "POST":

        interest = request.form["interest"]

        recommendations = recommender.recommend_courses(interest)

    return render_template("dashboard.html",
                           recommendations=recommendations)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
