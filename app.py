from flask import Flask, render_template, request, redirect
import os
import recommender

app = Flask(__name__)


# ==========================
# ENTER PAGE (Terms & Conditions)
# ==========================
@app.route("/", methods=["GET", "POST"])
def enter():

    if request.method == "POST":
        return redirect("/dashboard")

    return render_template("enter.html")


# ==========================
# DASHBOARD PAGE
# ==========================
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    recommendations = []

    if request.method == "POST":

        interest = request.form.get("interest")

        if interest:
            recommendations = recommender.recommend_courses(interest)

    return render_template(
        "dashboard.html",
        recommendations=recommendations
    )


# ==========================
# LOGOUT ROUTE → Redirect to Enter page
# ==========================
@app.route("/logout")
def logout():
    return redirect("/")


# ==========================
# RUN APP (Render compatible)
# ==========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
