# app.py
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import pandas as pd
import shap
import joblib
import smtplib
from email.mime.text import MIMEText
from fpdf import FPDF
import os

app = Flask(__name__)
CORS(app)

# Load pre-trained model and explainer (mocked here)
model = joblib.load("model.pkl")
explainer = joblib.load("explainer.pkl")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data["email"] == "admin@example.com" and data["password"] == "admin123":
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"}), 401

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    df = pd.read_csv(file)
    preds = model.predict(df)
    shap_values = explainer.shap_values(df)

    alerts = []
    for i, row in df.iterrows():
        if preds[i] == 1:
            alerts.append({
                "timestamp": row["timestamp"],
                "status": "UNSAFE",
                "shap": shap_values[i].tolist(),
                "data": row.to_dict()
            })
    return jsonify(alerts)

@app.route("/send-alert", methods=["POST"])
def send_alert():
    data = request.get_json()
    recipient = data["email"]
    message = f"Alert: anomaly detected at {data['timestamp']} with values {data['data']}"
    try:
        msg = MIMEText(message)
        msg["Subject"] = "Sensor Anomaly Alert"
        msg["From"] = "yourapp@example.com"
        msg["To"] = recipient

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("yourapp@example.com", "yourpassword")
            server.send_message(msg)
        return jsonify({"status": "sent"})
    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)})

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.get_json()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Sensor Anomaly Report", ln=True)
    for alert in data["alerts"]:
        pdf.multi_cell(0, 10, txt=str(alert))
    pdf_path = "report.pdf"
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
