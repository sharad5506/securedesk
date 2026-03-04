import json
import os
from datetime import datetime

LOG_FILE = "logs/threat_logs.json"


def _ensure_log_directory():
    """Ensures the logs/ directory exists."""
    log_dir = os.path.dirname(LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)


def _load_existing_logs():
    """Loads existing logs safely, even if file is corrupted or empty."""
    if not os.path.exists(LOG_FILE):
        return []

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        # Corrupted or empty file → reset
        return []


def _write_logs(data):
    """Safely writes logs to JSON file."""
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def log_event(event):
    """
    Safely logs a security event with timestamp.
    Creates file/folder if missing, fixes corrupted logs.
    """

    _ensure_log_directory()

    logs = _load_existing_logs()

    entry = {
        "event": event,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    logs.append(entry)

    _write_logs(logs)

    return True  # confirms logging