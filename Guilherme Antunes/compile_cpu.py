import re
import pandas as pd
import os

# Define the base path for log files and output CSV path
log_base_path = "C:/Users/guipm/logs/Set5/"
output_csv_path = os.path.join(log_base_path, "csv/excel/set5_cpu_metrics_combined.csv")

# Pattern to match each data line
cpu_line_pattern = re.compile(r'^(\d{2}:\d{2}:\d{2})\s+(\S+)\s+(.*)$')

columns = ['%usr', '%nice', '%sys', '%iowait', '%irq', '%soft', '%steal', '%guest', '%gnice', '%idle']
all_logs_data = []

# Loop through each log file from cpu1.log to cpu5.log
for i in range(1, 6):
    log_path = os.path.join(log_base_path, f"cpu{i}.log")
    records = []
    with open(log_path, 'r') as file:
        for line in file:
            match = cpu_line_pattern.match(line)
            if match:
                timestamp, cpu, values_str = match.groups()
                if cpu == "CPU":
                    continue  # skip header
                values = list(map(float, values_str.split()))
                record = {'time': timestamp, 'CPU': cpu, 'log_file': f'cpu{i}.log'}
                for col, val in zip(columns, values):
                    record[col] = val
                records.append(record)
    # Add a time counter in seconds for each record
    for idx, rec in enumerate(records):
        rec['second'] = idx
    all_logs_data.extend(records)

# Create DataFrame from all collected data
df = pd.DataFrame(all_logs_data)

# Save all collected data into a single CSV file
df.to_csv(output_csv_path, index=False)

print(f"All CPU metrics compiled and saved to: {output_csv_path}")
