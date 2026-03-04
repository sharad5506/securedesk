import psutil
import time
from utils.log_utils import log_event

SAFE_PROCESSES = [
    "python.exe",
    "pythonw.exe",
    "cmd.exe",
    "powershell.exe",
    "code.exe",
    "conhost.exe",
    "system idle process",
    "system"
]

def watchdog():
    """
    Continuously monitors running processes and blocks
    suspicious process-killing tools.
    """

    while True:
        try:
            for proc in psutil.process_iter(["pid", "name"]):
                name = proc.info.get("name")

                if not name:
                    continue

                name = name.lower()

                # Ignore safe processes
                if name in SAFE_PROCESSES:
                    continue

                # Detect suspicious kill tools
                if (
                    "taskkill" in name or
                    "processhacker" in name or
                    "killer" in name
                ):
                    log_event(f"Attempt to kill SecureDesk detected: {name}")

                    try:
                        proc.kill()
                    except (psutil.NoSuchProcess,
                            psutil.AccessDenied,
                            psutil.ZombieProcess):
                        pass

        except Exception as e:
            # Prevent watchdog crash
            print("Watchdog error:", e)

        # Reduce CPU usage
        time.sleep(2)
