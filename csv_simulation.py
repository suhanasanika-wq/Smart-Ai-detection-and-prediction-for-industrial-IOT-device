import csv, random, datetime, time

file = "sensor_readings.csv"

def append_row():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    voltage = round(random.uniform(220, 400), 2)
    temperature = round(random.uniform(55, 90), 1)
    vibration = round(random.uniform(0.1, 1.0), 3)
    pressure = round(random.uniform(0.8, 1.5), 2)

    with open(file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now, voltage, temperature, vibration, pressure])
    print(f"Row added at {now}")


try:
    with open(file, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "voltage", "temperature", "vibration", "pressure"])
except FileExistsError:
    pass


while True:
    append_row()
    time.sleep(60)
