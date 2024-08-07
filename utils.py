from constants import ConstantRunColumns
import os
import glob
import pandas as pd
import datetime
import uuid

def build_data():
    data = {}
    add_routes_data(data)
    add_runs_data(data)
    add_common_routes(data)

    return data

def add_routes_data(data):
    route_paths = glob.glob("./data/runroutes/*.csv")
    routes = []

    for route_path in route_paths:
        frame = pd.read_csv(route_path)
        route = {}
        routes.append(route)
        route["path"] = route_path
        route["name"] = os.path.splitext(os.path.basename(route_path))[0]
        route["splits"] = parse_splits(frame)

    data["routes"] = routes

def add_runs_data(data):
    runs = []

    for route in data["routes"]:
        frame = pd.read_csv(route["path"])
        distance = 0
        for split in route["splits"]:
            distance += split["distance"]
        for _, row in frame.iterrows():
            time = 0
            for split_time in row.drop(ConstantRunColumns.ALL_COLUMNS):
                time += split_time
            run = {}
            runs.append(run)
            run["route_name"] = route["name"]
            run["distance"] = "{:.1f}".format(distance)
            run["date"] = row[ConstantRunColumns.DATE]
            run["id"] = row[ConstantRunColumns.ID]
            run["time"] = time

    runs = sorted(runs, key=sort_by_date_string)
    data["runs"] = runs

def add_common_routes(data):
    common_routes = []
    route_counts = {}
    for run in data["runs"][:10]:
        if run["route_name"] not in route_counts:
            route_counts[run["route_name"]] = 0
        route_counts[run["route_name"]] += 1
    most_common_routes = sorted(list(route_counts.items()), key=lambda c: -c[1])
    for route in most_common_routes[:2]:
        common_routes.append(([r for r in data["routes"] if r.get("name")==route[0]][0]))
    data["common_routes"] = common_routes

def parse_split_title(split_title, df=None):
    [raw_number, raw_distance, raw_name] = split_title.split("@")
    fastest = None
    slowest = None
    average = None

    if df is not None and len(df) > 0:
        fastest = int(df[split_title].min())
        slowest = int(df[split_title].max())
        average = int(df[split_title].mean())

    return {
        "number": int(raw_number),
        "name": raw_name.replace("_", " "),
        "distance": float(raw_distance),
        "col_name": split_title,
        "fastest": fastest,
        "slowest": slowest,
        "average": average,
    }

def parse_splits(df):
    relevant_columns = list(set(df.columns) - set(ConstantRunColumns.ALL_COLUMNS))
    relevant_columns = relevant_columns
    splits = [parse_split_title(col, df) for col in relevant_columns]

    return splits

def sort_by_date_string(obj):
    date_string = obj["date"]
    date = datetime.datetime.strptime(date_string, "%m/%d/%Y")
    return -int(date.strftime('%Y%m%d'))

def format_run_date(date_string):
    date = datetime.datetime.strptime(date_string, "%m/%d/%Y")
    return date.strftime("%A, %B %-d %Y")

def format_run_time(time):
    seconds_in_a_minute = 60
    seconds_in_an_hour = seconds_in_a_minute * 60
    complete_hours = time // seconds_in_an_hour
    time -= seconds_in_an_hour * complete_hours
    complete_minutes = time // seconds_in_a_minute
    time -= seconds_in_a_minute * complete_minutes
    h = str(int(complete_hours)).zfill(2)
    m = str(int(complete_minutes)).zfill(2)
    s = str(int(round(time))).zfill(2)
    return f"{h}:{m}:{s}"

def append_run(route_name, split_row):
    frame_path = f"./data/runroutes/{route_name}.csv"
    frame = pd.read_csv(frame_path)
    new_row = { **split_row }
    new_row[ConstantRunColumns.DATE] = datetime.datetime.now().strftime("%m/%d/%Y")
    new_row[ConstantRunColumns.ID] = str(uuid.uuid4())
    frame = pd.concat([frame, pd.DataFrame([new_row])])
    frame.to_csv(frame_path, index=False)

    return new_row
    