import requests
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIGNATURE_FILE = os.path.join(BASE_DIR, "scanner/signatures.json")
VERSION_FILE = os.path.join(BASE_DIR, "scanner/version.json")

# 🔹 Replace with your GitHub raw URLs
CLOUD_SIGNATURE_URL = "https://raw.githubusercontent.com/YOUR_REPO/signatures.json"
CLOUD_VERSION_URL = "https://raw.githubusercontent.com/YOUR_REPO/version.json"


def get_local_version():
    if not os.path.exists(VERSION_FILE):
        return "0.0"

    with open(VERSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("version", "0.0")


def update_signatures():
    try:
        local_version = get_local_version()

        cloud_version_data = requests.get(CLOUD_VERSION_URL).json()
        cloud_version = cloud_version_data.get("version", "0.0")

        if cloud_version > local_version:
            # Download new signatures
            new_signatures = requests.get(CLOUD_SIGNATURE_URL).text

            with open(SIGNATURE_FILE, "w", encoding="utf-8") as f:
                f.write(new_signatures)

            # Update version file
            with open(VERSION_FILE, "w") as f:
                json.dump({"version": cloud_version}, f)

            return {
                "status": "updated",
                "new_version": cloud_version
            }

        return {
            "status": "already_latest",
            "version": local_version
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
