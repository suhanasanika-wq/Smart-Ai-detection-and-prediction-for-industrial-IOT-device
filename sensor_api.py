from flask import Flask, jsonify, send_file
from flask_cors import CORS
import pandas as pd
from datetime import datetime, timedelta
import os
import smtplib
from email.message import EmailMessage
import pdfkit

app = Flask(__name__)
CORS(app)

CSV_FILE = "sensor_readings.csv"
EMAIL_USER = "your-gmail@gmail.com"
EMAIL_PASS = "your-16-digit-app-password"
EMAIL_TO = "your-gmail@gmail.com"
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

def send_email_alert(voltage, timestamp):
    subject = "⚠️ Voltage Anomaly Detected"
    body = f"Abnormal voltage detected: {voltage}V at {timestamp}"
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
            print("✅ Email sent.")
    except Exception as e:
        print("❌ Email error:", e)

@app.route("/api/sensor-data", methods=["GET"])
def get_latest_sensor_data():
    if not os.path.exists(CSV_FILE):
        return jsonify({"error": "CSV not found"}), 404
    try:
        df = pd.read_csv(CSV_FILE)
        latest = df.iloc[-1]
        voltage = float(latest["voltage"])
        timestamp = str(latest["timestamp"])
        email_sent = False

        if voltage < 220 or voltage > 270:
            send_email_alert(voltage, timestamp)
            email_sent = True

        return jsonify({
            "timestamp": timestamp,
            "voltage": f"{voltage} V",
            "temperature": f"{latest['temperature']} °C",
            "vibration": f"{latest['vibration']} Hz",
            "pressure": f"{latest['pressure']} psi",
            "email_sent": email_sent
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sensor-history/<sensor>", methods=["GET"])
def get_sensor_history(sensor):
    try:
        df = pd.read_csv(CSV_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
        df = df.dropna(subset=["timestamp"])  # remove bad rows

        now = datetime.now()
        recent = df[df["timestamp"] >= now - timedelta(minutes=5)]
        data = [
            {"value": row[sensor], "time": row["timestamp"].strftime("%H:%M:%S")}
            for _, row in recent.iterrows()
        ]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/report", methods=["GET"])
def download_report():
    try:
        df = pd.read_csv(CSV_FILE)
        html = f"""
        <html><head><style>
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
        th {{ background-color: #f2f2f2; }}
        </style></head><body>
        <h2>Sensor Report</h2>
        {df.to_html(index=False)}
        </body></html>
        """
        pdfkit.from_string(html, "sensor_report.pdf", configuration=PDFKIT_CONFIG)
        return send_file("sensor_report.pdf", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

