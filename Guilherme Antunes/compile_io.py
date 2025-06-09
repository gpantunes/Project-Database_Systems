import pandas as pd
import re
import os

# Define the base path for log files and output CSV path
log_base_path = "C:/Users/guipm/logs/Set5/"
output_csv_path = os.path.join(log_base_path, "csv/excel/set5_io_metrics_combined.csv")

all_logs_data = []

# Loop through each log file from io1.log to io5.log
for i in range(1, 6):
    log_file = os.path.join(log_base_path, f"io{i}.log")
    log_filename = f"io{i}.log"

    # Read and parse the log
    with open(log_file, 'r') as file:
        lines = file.readlines()

    headers = []
    data_blocks = []
    current_block = []

    for line in lines:
        if line.startswith("Device"):
            header_line = re.sub(r'\s+', ',', line.strip())
            headers = header_line.split(',')[1:]
            continue
        elif line.strip() == "":
            if current_block:
                data_blocks.append(current_block)
                current_block = []
        elif not line.startswith("Linux"):
            current_block.append(line.strip())

    if current_block:
        data_blocks.append(current_block)

    # Parse and collect data
    for block in data_blocks:
        for idx, line in enumerate(block):
            if line:
                parts = re.split(r'\s+', line)
                dev = parts[0]
                record = {
                    'log_file': log_filename,
                    'Device': dev,
                    'second': idx  # index within the block becomes the "second"
                }
                for j, key in enumerate(headers):
                    try:
                        record[key] = float(parts[j + 1])
                    except ValueError:
                        record[key] = 0.0
                all_logs_data.append(record)

# Convert to DataFrame
df_all = pd.DataFrame(all_logs_data)

# Save to CSV
df_all.to_csv(output_csv_path, index=False)

print(f"All I/O metrics compiled and saved to: {output_csv_path}")
