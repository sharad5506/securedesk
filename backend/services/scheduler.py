import threading
import time
import os

from scanner.signature_scanner import signature_scan
from scanner.heuristic_engine import heuristic_scan
from scanner.behavior_engine import behavior_scan
from utils.log_utils import log_event


def scheduled_scan(paths, interval=3600):
    """
    Runs scheduled scans repeatedly.
    - paths (list): List of critical files/folders to monitor
    - interval: Time gap between scans (default 1 hour)
    """

    if isinstance(paths, str):
        # If user passes a single string, convert to list
        paths = [paths]

    log_event(f"Scheduled scan started. Scanning every {interval} seconds.")

    while True:

        for path in paths:

            if not os.path.exists(path):
                log_event(f"Scheduled scan skipped missing file: {path}")
                continue

            # -----------------------------
            # 1. Signature Scan
            # -----------------------------
            sig = signature_scan(path)

            if sig.get("infected"):
                log_event(f"[Scheduled] Signature threat detected: {path}")
                continue

            # -----------------------------
            # 2. Heuristic Scan
            # -----------------------------
            heu = heuristic_scan(path)

            if heu.get("suspicious"):
                log_event(f"[Scheduled] Heuristic alert: {path} → {heu['reasons']}")
                continue

            # -----------------------------
            # 3. Behavior Scan
            # -----------------------------
            beh = behavior_scan(path)

            if beh.get("behavior_score", 0) > 0:
                log_event(f"[Scheduled] Behavior threat detected: {path}")
                continue

            # If clean
            log_event(f"[Scheduled] {path} → Clean")

        time.sleep(interval)


def start_scheduled_scan(paths, interval=3600):
    """
    Runs scheduled scanning in a background thread.
    """
    thread = threading.Thread(
        target=scheduled_scan,
        args=(paths, interval),
        daemon=True
    )
    thread.start()
    return thread