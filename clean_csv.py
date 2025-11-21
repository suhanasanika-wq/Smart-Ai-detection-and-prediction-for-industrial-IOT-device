import pandas as pd

input_path = "sensor_readings.csv"
output_path = "sensor_readings_clean.csv"

with open(input_path, 'r') as file:
    lines = [line for line in file if len(line.strip().split(',')) == 5]

with open(output_path, 'w') as out:
    out.writelines(lines)

print(f"✅ Cleaned file saved to: {output_path}")
