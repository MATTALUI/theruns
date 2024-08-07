import seaborn as sns
import glob
import pandas as pd
import utils
from constants import ConstantRunColumns
import os
import matplotlib as mp
import matplotlib.dates as md
import matplotlib.pyplot as plt

def generate_run_pace_report(report):
    run_id = report.get("run_id")
    target_pace_src = f"./static/images/reports/run-pace-{run_id}.png"
    report["src"] = target_pace_src[1:]
    # if os.path.exists(target_pace_src):
    #     return
    route_paths = glob.glob("./data/runroutes/*.csv")
    run_row = None

    for route_path in route_paths:
        frame = pd.read_csv(route_path)
        frame = frame[frame[ConstantRunColumns.ID] == run_id]
        if len(frame) == 1:
            run_row = frame.drop(ConstantRunColumns.ALL_COLUMNS, axis=1).values.tolist()[0]
            break

    paces = []
    for i in range(len(run_row)):
        split_name = frame.columns.tolist()[i]
        split_data = utils.parse_split_title(split_name)
        seconds = run_row[i]
        split_distance = split_data["distance"]
        pace = round(seconds / split_distance)
        paces.append({
            "Split Number": split_data["number"],
            "Pace": pace
        })
    pace_frame = pd.DataFrame(paces)
    print(pace_frame.head())
    mp.pyplot.switch_backend('Agg')
    sns.set_theme(style="darkgrid")
    ax = sns.lineplot(
        data=pace_frame,
        x="Split Number",
        y="Pace",
    )
    ax.set_title("Split Paces")
    ax.yaxis.set_major_formatter(lambda v,s: utils.format_run_time(v))
    ax.figure.savefig(target_pace_src)
    plt.close()