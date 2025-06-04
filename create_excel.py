import json
import pandas as pd
import os
from datetime import datetime

def append_json_to_excel(json_path, excel_path, batch_name=None):
    # Load JSON data
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Create a list of rows from the JSON data
    rows = []
    timestamp = datetime.now().isoformat(timespec='seconds')
    batch = batch_name or timestamp
    
    for txn_type, stats in data.items():
        row = {
            "batch": batch,
            "txn_type": txn_type,
            **{k: float(v) for k, v in stats.items()}
        }
        rows.append(row)
    
    # Convert to DataFrame
    df_new = pd.DataFrame(rows)

    # If file exists, append
    if os.path.exists(excel_path):
        df_existing = pd.read_excel(excel_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    # Write back to Excel
    df_combined.to_excel(excel_path, index=False)
    print(f"Data from '{json_path}' added to '{excel_path}' successfully.")

# Example usage:
# The name of the excel file is results_vusers-warehouses-rampup-duration
append_json_to_excel("./gpantunes/data1.json", "./gpantunes/timing_data_8-8-2-5.xlsx", batch_name="test_run_2")
