import os
import time

HONEYPOT_DIR = "backend/data/honeypot/"

# Ensure directory exists
os.makedirs(HONEYPOT_DIR, exist_ok=True)

def initialize_honeypot():
    """
    Creates several honeypot files that ransomware will try to encrypt/delete.
    These files should remain untouched.
    """
    sample_files = [
        "hp_doc1.txt",
        "hp_img1.jpg",
        "hp_data1.bin"
    ]

    for fname in sample_files:
        path = os.path.join(HONEYPOT_DIR, fname)

        # Create file if missing
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("Honeypot file - do not modify")

    return True


def check_honeypot():
    """
    Checks if honeypot files were modified, deleted, encrypted, or resized.
    If yes → ransomware activity suspected.
    """

    for file in os.listdir(HONEYPOT_DIR):

        path = os.path.join(HONEYPOT_DIR, file)

        # FILE DELETED → ransomware likely
        if not os.path.exists(path):
            return {
                "alert": True,
                "message": f"Ransomware attempt: Honeypot file missing → {file}"
            }

        # FILE SIZE ZERO → ransomware overwrote/encrypted file
        if os.path.getsize(path) == 0:
            return {
                "alert": True,
                "message": f"Ransomware attempt: Honeypot file tampered → {file}"
            }

        # LAST-MODIFIED CHECK — ransomware often edits all files quickly
        last_modified = os.path.getmtime(path)
        if time.time() - last_modified < 3:  # changed in last 3 seconds
            return {
                "alert": True,
                "message": f"Ransomware modification detected → {file}"
            }

    return {"alert": False, "message": "No ransomware behavior detected"}