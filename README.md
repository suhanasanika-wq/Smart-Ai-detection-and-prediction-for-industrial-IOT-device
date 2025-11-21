setup+code run instructions



🔧 Industrial Sensor Monitoring Dashboard

A modern AI-powered dashboard to monitor IoT sensor data in real-time, detect anomalies, send alerts via email, generate downloadable reports in PDF format, and assess system safety using hazard prediction.

🚀 Features

📊 Live Monitoring of Voltage, Temperature, Vibration, and Pressure

⚠ Anomaly Detection and real-time alert system

📧 Email Notifications for flagged irregularities

🤖 AI Hazard Risk Assessment with visual risk bar

🕒 Sensor History viewer for last 5 minutes

📄 PDF Report Export for sensor logs

🖥 Modern UI with gradient-based visual design

🛠 Tech Stack

Frontend: HTML, CSS, JavaScript

Backend: Flask (Python), Pandas

Email Service: SMTP with Gmail App Password

PDF Generator: pdfkit + wkhtmltopdf

Deployment: Localhost (Flask dev server) / Optional: Render, Replit, or Railway

📦 Installation

Clone the repository:

git clone https://github.com/your-username/sensor-dashboard.git
cd sensor-dashboard


Install dependencies:

pip install -r requirements.txt


Install wkhtmltopdf:

Download: https://wkhtmltopdf.org/downloads.html

Add its path to sensor_api.py like:

PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")


Create .env file or replace in code:

EMAIL_USER=your-gmail@gmail.com
EMAIL_PASS=your-16-digit-app-password
EMAIL_TO=receiver-email@gmail.com

🚦 Run Locally
python sensor_api.py


Then open index.html in a browser and start interacting with the dashboard.

📎 File Structure

index.html – Main frontend UI

sensor_api.py – Flask backend API

sensor_readings.csv – Live sensor data source (simulated)

csv_simulation.py – Generates and appends new sensor data

📌 Notes

Use app-specific passwords for Gmail (enable 2FA).

Email alerts are sent when voltage goes beyond normal range (220–270V).

Make sure wkhtmltopdf is installed and reachable via PATH.
