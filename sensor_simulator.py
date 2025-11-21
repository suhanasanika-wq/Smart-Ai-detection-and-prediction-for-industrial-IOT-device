import csv
import random
import datetime
import time
import os

CSV_FILE = "sensor_readings.csv"


if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "voltage", "temperature", "vibration", "pressure"])

def generate_mock_row():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    voltage = round(random.uniform(220, 400), 2)         # V
    temperature = round(random.uniform(55, 90), 1)        # °C
    vibration = round(random.uniform(0.1, 1.0), 3)        # Hz
    pressure = round(random.uniform(0.8, 1.5), 2)         # psi
    return [now, voltage, temperature, vibration, pressure]


while True:
    row = generate_mock_row()
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)
    print(f"[{row[0]}] Data added: {row[1:]}")

    time.sleep(60)
