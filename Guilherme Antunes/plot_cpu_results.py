import re
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the base path for log files and output directory
log_base_path = "C:/Users/guipm/logs/Set5.1/"
output_dir = r'C:/Users/guipm/logs/Set5.1/plots/cpu'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

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
    all_logs_data.extend(records)

# Create DataFrame from all collected data
df = pd.DataFrame(all_logs_data)

# Filter for 'all' CPU data
df_all = df[df['CPU'] == 'all']

# Plotting all metrics for the 'all' CPU, comparing across log files
for metric in columns:
    plt.figure(figsize=(12, 6))
    for log_file in df_all['log_file'].unique():
        df_filtered = df_all[df_all['log_file'] == log_file].copy()
        df_filtered['second'] = df_filtered.groupby('log_file').cumcount()
        plt.plot(df_filtered['second'], df_filtered[metric], label=log_file)

    plt.title(f"'all' CPU - {metric} over time (Comparison)")
    plt.xlabel("Seconds")
    plt.ylabel("Percentage")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{metric.replace('%','')}_cpu_comparison.png"))  # Save each plot
    plt.close()

print(f"Comparison plots saved for each metric in {output_dir}.")