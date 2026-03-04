import psutil
import time
from utils.log_utils import log_event


def monitor_behavior():
    """
    Real-time process behavior monitoring:
    ✔ Detects CPU spikes
    ✔ Detects abnormal disk activity
    ✔ Detects suspicious process names
    ✔ Safe, crash-proof scanning
    """

    SUSPICIOUS_KEYWORDS = [
        "encrypt", "crypto", "locker", "ransom", "pythonw",
        "powershell", "cmd.exe", "wscript", "cscript"
    ]

    while True:
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'io_counters']):
                name = proc.info.get("name", "").lower()

                # -------------------------------
                # 1. CPU spike detection
                # -------------------------------
                if proc.info.get("cpu_percent", 0) > 80:
                    log_event(f"High CPU usage detected → {name}")

                # -------------------------------
                # 2. Suspicious process naming
                # -------------------------------
                for keyword in SUSPICIOUS_KEYWORDS:
                    if keyword in name:
                        log_event(f"Suspicious process detected → {name}")
                        break

                # -------------------------------
                # 3. Abnormal disk activity (possible ransomware)
                # -------------------------------
                io = proc.info.get("io_counters")
                if io:
                    # Write-heavy process → ransomware often writes rapidly
                    if io.write_bytes > 5 * 1024 * 1024:  # >5MB writes instantly
                        log_event(f"Heavy disk write activity detected → {name}")

        except Exception as e:
            log_event(f"Monitor error: {str(e)}")

        time.sleep(3)