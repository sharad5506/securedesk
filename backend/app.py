from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
import os
import threading
import psutil

from scanner.signature_scanner import signature_scan
from scanner.behavior_engine import behavior_scan
from scanner.heuristic_engine import heuristic_scan
from scanner.ransomware_trap import check_honeypot
from scanner.quarantine import add_to_quarantine, get_quarantine_items
from utils.log_utils import log_event
from scanner.real_time_monitor import monitor_behavior
from scanner.watchdog import watchdog
from scanner.cloud_updater import update_signatures


# ==========================================================
# BASE PATH CONFIGURATION
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
LOGS_PATH = os.path.join(BASE_DIR, "logs/threat_logs.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)


# ==========================================================
# SERVE FRONTEND (Safe Routing)
# ==========================================================
@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    if path.startswith("api/"):
        return jsonify({"error": "Invalid endpoint"}), 404
    return send_from_directory(FRONTEND_DIR, path)


# ==========================================================
# API: ENGINE STATUS
# ==========================================================
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "engine": "SecureDesk Engine",
        "status": "running",
        "quarantined": len(get_quarantine_items())
    })


# ==========================================================
# API: SCAN FILE
# ==========================================================
@app.route("/api/scan", methods=["POST"])
def scan_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_DIR, filename)
        file.save(file_path)

        result = {"file": filename}

        # ---------- Signature Scan ----------
        sig = signature_scan(file_path)
        result["signature"] = sig

        if sig.get("infected"):
            add_to_quarantine(file_path)
            log_event(f"Signature detection: {filename}")
            return jsonify(result)

        # ---------- Heuristic Scan ----------
        heu = heuristic_scan(file_path)
        result["heuristic"] = heu

        if heu.get("suspicious"):
            add_to_quarantine(file_path)
            log_event(f"Heuristic detection: {filename}")
            return jsonify(result)

        # ---------- Behavior Scan ----------
        beh = behavior_scan(file_path)
        result["behavior"] = beh

        # ---------- Honeypot Check ----------
        try:
            result["honeypot"] = check_honeypot()
        except FileNotFoundError:
            honeypot_dir = os.path.join(BASE_DIR, "data/honeypot")
            os.makedirs(honeypot_dir, exist_ok=True)
            result["honeypot"] = {"info": "honeypot folder created"}

        return jsonify(result)

    except Exception as e:
        log_event(f"Scan error: {str(e)}")
        return jsonify({"error": "Scan failed"}), 500


# ==========================================================
# API: QUARANTINE
# ==========================================================
@app.route("/api/quarantine", methods=["GET"])
def quarantine_list():
    return jsonify(get_quarantine_items())


# ==========================================================
# API: LOGS
# ==========================================================
@app.route("/api/logs", methods=["GET"])
def get_logs():
    if not os.path.exists(LOGS_PATH):
        return jsonify([])

    try:
        with open(LOGS_PATH, "r") as f:
            return jsonify(json.load(f))
    except json.JSONDecodeError:
        return jsonify([])
    except Exception:
        return jsonify([])


# ==========================================================
# API: REAL-TIME PROCESS MONITOR
# ==========================================================
@app.route("/api/processes", methods=["GET"])
def get_processes():
    processes = []

    for p in psutil.process_iter(["name", "cpu_percent"]):
        try:
            cpu = p.cpu_percent(interval=0.1)
            processes.append({
                "name": p.info["name"],
                "cpu": cpu
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort by highest CPU usage
    processes.sort(key=lambda x: x["cpu"], reverse=True)

    # Return top 15 processes only
    return jsonify(processes[:15])


# ==========================================================
# SAFE BACKGROUND THREAD WRAPPERS
# ==========================================================
def safe_monitor():
    try:
        monitor_behavior()
    except Exception as e:
        print("Monitor thread crashed:", e)


def safe_watchdog():
    try:
        watchdog()
    except Exception as e:
        print("Watchdog thread crashed:", e)


# ==========================================================
# API: UPDATE SIGNATURES
# ==========================================================
@app.route("/api/update", methods=["GET"])
def update():
    result = update_signatures()
    return jsonify(result)


# ==========================================================
# RUN APP
# ==========================================================
if __name__ == "__main__":
    # Start background protection threads
    threading.Thread(target=safe_monitor, daemon=True).start()
    threading.Thread(target=safe_watchdog, daemon=True).start()

    # Run Flask
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
