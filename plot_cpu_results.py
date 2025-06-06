import re
import pandas as pd
import matplotlib.pyplot as plt

log_path = "C:/Users/guipm/logs/Set1/4vusers/cpu1.log"

# Pattern to match each data line
cpu_line_pattern = re.compile(r'^(\d{2}:\d{2}:\d{2})\s+(\S+)\s+(.*)$')

columns = ['%usr', '%nice', '%sys', '%iowait', '%irq', '%soft', '%steal', '%guest', '%gnice', '%idle']
records = []

with open(log_path, 'r') as file:
    current_time = None
    for line in file:
        match = cpu_line_pattern.match(line)
        if match:
            timestamp, cpu, values_str = match.groups()
            if cpu == "CPU":
                continue  # skip header
            values = list(map(float, values_str.split()))
            record = {'time': timestamp, 'CPU': cpu}
            for col, val in zip(columns, values):
                record[col] = val
            records.append(record)

# Create DataFrame
df = pd.DataFrame(records)
df['second'] = df.groupby('CPU').cumcount()  # Time index per CPU
df_all = df[df['CPU'] == 'all'].reset_index(drop=True)

# Plotting all metrics for the 'all' CPU
for metric in columns:
    plt.figure(figsize=(10, 4))
    plt.plot(df_all['second'], df_all[metric])
    plt.title(f"'all' CPU - {metric} over time")
    plt.xlabel("Seconds")
    plt.ylabel("Percentage")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{metric.replace('%','')}_all_cpu.png")  # Save each plot
    plt.close()

print("Plots saved for each metric (all CPU view).")
