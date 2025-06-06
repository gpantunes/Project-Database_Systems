import matplotlib.pyplot as plt
import pandas as pd
import re
import os

# Define the base path for log files and output directory
log_base_path = "C:/Users/guipm/logs/Set1/4vusers/"
output_dir = r'C:/Users/guipm/logs/Set1/4vusers/plots/io'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

all_logs_data = []

# Loop through each log file from io1.log to io5.log
for i in range(1, 6):
    log_file = os.path.join(log_base_path, f"io{i}.log")
    log_filename = f"io{i}.log" # Identifier for the current log file

    # Read and parse the log
    with open(log_file, 'r') as file:
        lines = file.readlines()

    headers = []
    data_blocks = []
    current_block = []

    for line in lines:
        if line.startswith("Device"):
            # Clean and split header line, skip 'Device'
            header_line = re.sub(r'\s+', ',', line.strip())
            headers = header_line.split(',')[1:]
            continue
        elif line.strip() == "":
            if current_block:
                data_blocks.append(current_block)
                current_block = []
        elif not line.startswith("Linux"): # Skip lines that start with "Linux" (system info)
            current_block.append(line.strip())

    if current_block: # Add any remaining block
        data_blocks.append(current_block)

    # Parse device data from collected blocks
    for block in data_blocks:
        for line in block:
            if line:
                parts = re.split(r'\s+', line)
                dev = parts[0] # Device name is the first part
                record = {'log_file': log_filename, 'Device': dev}
                for j, key in enumerate(headers):
                    try:
                        # Convert value to float, handling potential errors
                        record[key] = float(parts[j + 1])
                    except ValueError:
                        record[key] = 0.0 # Default to 0.0 if conversion fails (e.g., non-numeric data)
                all_logs_data.append(record)

# Create a single DataFrame from all collected data
df_all = pd.DataFrame(all_logs_data)

# Get unique devices found across all log files
unique_devices = df_all['Device'].unique()
# Determine metric columns dynamically by excluding 'log_file' and 'Device'
metric_columns = [col for col in df_all.columns if col not in ['log_file', 'Device']]

# Plotting each metric for each device, comparing across log files
for dev in unique_devices:
    # Filter DataFrame for the current device
    df_dev = df_all[df_all['Device'] == dev].copy()
    for metric in metric_columns:
        plt.figure(figsize=(12, 6)) # Larger figure size for comparison plots
        
        # Plot data for each log file on the same graph
        for log_file_identifier in df_dev['log_file'].unique():
            df_filtered = df_dev[df_dev['log_file'] == log_file_identifier].copy()
            # Create a time index (seconds) for each log file independently
            df_filtered['time_idx'] = df_filtered.groupby('log_file').cumcount()
            plt.plot(df_filtered['time_idx'], df_filtered[metric], label=log_file_identifier)

        plt.title(f"{metric} over Time for {dev} (Comparison)")
        plt.xlabel("Time (s)")
        plt.ylabel(metric)
        plt.grid(True)
        plt.legend(title="Log File") # Add a legend to distinguish lines
        plt.tight_layout() # Adjust layout to prevent labels from overlapping
        
        # Define filename for the comparison plot
        filename = f"{dev}_{metric.replace('/', '_')}_comparison.png"
        plt.savefig(os.path.join(output_dir, filename))
        plt.close() # Close the plot to free up memory

print(f"Comparison plots saved for each metric and device in: {output_dir}")