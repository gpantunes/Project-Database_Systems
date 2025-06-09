import os
import json
import pandas as pd
from glob import glob

import sys
print("Using Python from:", sys.executable)

BASE_DIR = "."  # Current directory (i.e., logs/)

def process_nopm(json_files):
    rows = []
    for file in sorted(json_files):
        print(f"Reading nopm file: {file}")
        if os.path.getsize(file) == 0:
            print(f"⚠️ Skipping empty file: {file}")
            continue
        with open(file) as f:
            try:
                data = json.load(f)
                rows.append({
                    "ID": data[0],
                    "Timestamp": data[1],
                    "Users": data[2],
                    "Result": data[3]
                })
            except json.JSONDecodeError as e:
                print(f"Failed to parse {file}: {e}")
    return pd.DataFrame(rows)


def process_times(json_files):
    dfs = []
    for file in sorted(json_files):
        print(f"Reading times file: {file}")
        if os.path.getsize(file) == 0:
            print(f"⚠️ Skipping empty file: {file}")
            continue
        try:
            with open(file) as f:
                data = json.load(f)
                df = pd.DataFrame(data).T  # Transpose to make operations rows
                df.insert(0, "Source File", os.path.basename(file))
                df = df.reset_index().rename(columns={"index": "Operation"})
                dfs.append(df)
        except json.JSONDecodeError as e:
            print(f"Failed to parse {file}: {e}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def process_trx(json_files):
    dfs = []
    for file in sorted(json_files):
        print(f"Reading trx file: {file}")
        if os.path.getsize(file) == 0:
            print(f"⚠️ Skipping empty file: {file}")
            continue
        try:
            with open(file) as f:
                data = json.load(f)
                if not data:
                    print(f"⚠️ No data in {file}")
                    continue
                key = list(data.keys())[0]
                timestamps = list(data[key].keys())
                values = list(data[key].values())
                df = pd.DataFrame({"Timestamp": timestamps, key: values})
                df.insert(0, "Source File", os.path.basename(file))
                dfs.append(df)
        except json.JSONDecodeError as e:
            print(f"Failed to parse {file}: {e}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def process_set(set_path):
    json_dir = os.path.join(set_path, "csv", "jsons")
    excel_dir = os.path.join(set_path, "csv", "excel")
    folder_name = (set_path.split("\\")[-1]).lower()
    os.makedirs(excel_dir, exist_ok=True)

    nopm_files = glob(os.path.join(json_dir, "nopm[1-5].json"))
    times_files = glob(os.path.join(json_dir, "times[1-5].json"))
    trx_files = glob(os.path.join(json_dir, "trx[1-5].json"))

    if nopm_files:
        df_nopm = process_nopm(nopm_files)
        df_nopm.to_csv(os.path.join(excel_dir, f"{folder_name}_nopm.csv"), index=False)

    if times_files:
        df_times = process_times(times_files)
        df_times.to_csv(os.path.join(excel_dir, f"{folder_name}_times.csv"), index=False)

    if trx_files:
        df_trx = process_trx(trx_files)
        df_trx.to_csv(os.path.join(excel_dir, f"{folder_name}_trx.csv"), index=False)

def main():
    for set_dir in sorted(glob(os.path.join(BASE_DIR, "Set*"))):
        if os.path.isdir(set_dir):
            process_set(set_dir)
            

if __name__ == "__main__":
    main()
