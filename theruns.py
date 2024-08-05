from flask import Flask, render_template
import json
import utils

app = Flask(__name__)

data = utils.build_data()

@app.route("/")
def root():
    return render_template(
        "index.html",
        runs=data["runs"],
        common_routes=data["common_routes"],
        format_run_date=utils.format_run_date,
        format_run_time=utils.format_run_time,
    )

@app.route("/runs")
def runs_index():
    return render_template("runs.html")

@app.route("/runs/new")
def runs_new():
    return render_template("runs.html")

@app.route("/routes")
def routes_index():
    return render_template("routes.html")

@app.route("/insights")
def insights_index():
    return render_template("insights.html")

@app.route("/settings")
def settings_index():
    return render_template("settings.html")

@app.route("/help")
def help_index():
    return render_template("help.html")


@app.route("/api/routes", methods=["GET"])
def get_routes():
    return json.dumps(data["routes"])