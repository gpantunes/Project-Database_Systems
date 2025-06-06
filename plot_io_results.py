import matplotlib.pyplot as plt
import pandas as pd
import re
import os

# Define log file and output path
log_file = 'C:/Users/guipm/logs/Set1/4vusers/io1.log'
output_dir = r'C:/Users/guipm/logs/Set1/4vusers/plots'

# Extract base name without extension for naming plots
log_basename = os.path.splitext(os.path.basename(log_file))[0]

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read and parse the log
with open(log_file, 'r') as file:
    lines = file.readlines()

headers = []
data_blocks = []
current_block = []

for line in lines:
    if line.startswith("Device"):
        header_line = re.sub(r'\s+', ',', line.strip())
        headers = header_line.split(',')[1:]  # skip 'Device'
        continue
    elif line.strip() == "":
        if current_block:
            data_blocks.append(current_block)
            current_block = []
    elif not line.startswith("Linux"):
        current_block.append(line.strip())

if current_block:
    data_blocks.append(current_block)

# Parse device data
devices = {}
for block in data_blocks:
    for line in block:
        if line:
            parts = re.split(r'\s+', line)
            dev = parts[0]
            if dev not in devices:
                devices[dev] = {key: [] for key in headers}
            for i, key in enumerate(headers):
                try:
                    devices[dev][key].append(float(parts[i + 1]))
                except ValueError:
                    devices[dev][key].append(0.0)

# Plot and save each metric
for dev, metrics in devices.items():
    df = pd.DataFrame(metrics)
    time = list(range(len(df)))
    for column in df.columns:
        plt.figure(figsize=(10, 4))
        plt.plot(time, df[column], label=column)
        plt.title(f"{column} over Time for {dev}")
        plt.xlabel("Time (s)")
        plt.ylabel(column)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        filename = f"{log_basename}_{dev}_{column.replace('/', '_')}.png"
        plt.savefig(os.path.join(output_dir, filename))
        plt.close()

print(f"All plots saved to: {output_dir}")
