from flask import Flask, render_template, request
import json
import utils
import reports

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

@app.route("/runs", methods=["GET"])
def runs_index():
    return render_template(
        "runs.html",
        runs=data["runs"],
        format_run_date=utils.format_run_date,
        format_run_time=utils.format_run_time,
    )

@app.route("/runs/new", methods=["GET"])
def runs_new():
    return render_template(
        "run-form.html"
    )

@app.route("/runs/<run_id>", methods=["GET"])
def runs_show(run_id):
    run_info = utils.build_run_show_data(data, run_id)
    return render_template(
        "run.html",
        format_run_date=utils.format_run_date,
        format_run_time=utils.format_run_time,
        **run_info,
    )

@app.route("/routes", methods=["GET"])
def routes_index():
    return render_template(
        "routes.html",
        routes=data["routes"],
    )

@app.route("/routes/<route_name>", methods=["GET"])
def routes_show(route_name):
    return render_template("routes.html")

@app.route("/insights", methods=["GET"])
def insights_index():
    return render_template(
        "insights.html",
        stats=data["general_stats"],
    )

@app.route("/insights/runs/<run_id>", methods=["GET"])
def insights_run_show(run_id):
    return render_template(
        "insights.html",
        stats=data["general_stats"],
    )

@app.route("/settings", methods=["GET"])
def settings_index():
    return render_template("settings.html")

@app.route("/help", methods=["GET"])
def help_index():
    return render_template("help.html")


################################################################################
# API ROUTES
################################################################################
@app.route("/api/routes", methods=["GET"])
def get_routes():
    return json.dumps(data["routes"])

@app.route("/api/runs", methods=["POST"])
def create_run():
    global data
    run_data = request.get_json()
    final_row = utils.append_run(run_data.get("route_name"), run_data.get("row"))
    data = utils.build_data()
    return json.dumps(final_row)

@app.route("/api/reports/runs-pace")
def report_run_splits():
    report = {}
    run_id = request.args.get("run_id")
    report["type"] = "runs-splits"
    report["run_id"] = run_id
    reports.generate_run_pace_report(report)
    return json.dumps(report)

@app.route("/api/reports/runs-overview")
def report_run_overview():
    report = {}
    run_id = request.args.get("run_id")
    report["type"] = "runs-overview"
    report["run_id"] = run_id
    reports.generate_run_overview_report(report)
    return json.dumps(report)