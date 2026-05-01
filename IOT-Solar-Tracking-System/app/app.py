from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = "solar_secret_key"
DB_NAME = "solar.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS solar_data (
            timestamp TEXT,
            mode TEXT,
            sun_angle REAL,
            panel_angle REAL,
            voltage REAL,
            current REAL,
            power REAL,
            energy REAL
        )
    """)
    conn.commit()
    conn.close()


def get_latest_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(
        "SELECT * FROM solar_data ORDER BY timestamp DESC LIMIT 1", conn
    )
    conn.close()

    if df.empty:
        return None

    return df.iloc[0].to_dict()


def get_logs(limit=10):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(
        f"SELECT * FROM solar_data ORDER BY timestamp DESC LIMIT {limit}", conn
    )
    conn.close()

    return df.to_dict(orient="records")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form.get("username")
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    latest = get_latest_data()
    logs = get_logs()

    if latest is None:
        latest = {
            "timestamp": "N/A",
            "mode": "N/A",
            "sun_angle": 0,
            "panel_angle": 0,
            "voltage": 0,
            "current": 0,
            "power": 0,
            "energy": 0
        }

    predicted_energy = round(latest["energy"] * 1.1, 3)

    return render_template(
        "dashboard.html",
        data=latest,
        logs=logs,
        predicted_energy=predicted_energy
    )


@app.route("/api", methods=["POST"])
def api():
    data = request.json

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO solar_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["mode"],
        data["sun_angle"],
        data["panel_angle"],
        data["voltage"],
        data["current"],
        data["power"],
        data["energy"]
    ))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
