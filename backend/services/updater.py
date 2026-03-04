import requests
import json
import os

UPDATE_URL = "https://securedesk-cloud-api.com/update"
SIGNATURE_FILE = "scanner/signatures.json"
TIMEOUT = 7  # seconds


def check_updates():
    """
    Downloads updated malware signatures from SecureDesk cloud
    and safely writes them to signatures.json.
    """

    try:
        # Request cloud update
        response = requests.get(UPDATE_URL, timeout=TIMEOUT)

        if response.status_code != 200:
            return {
                "updated": False,
                "error": f"Server response: {response.status_code}"
            }

        # Validate JSON
        try:
            data = response.json()
        except json.JSONDecodeError:
            return {
                "updated": False,
                "error": "Invalid JSON from update server"
            }

        # Ensure directory exists
        os.makedirs(os.path.dirname(SIGNATURE_FILE), exist_ok=True)

        # Write new signature file
        with open(SIGNATURE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return {
            "updated": True,
            "message": "Signature database updated successfully"
        }

    except requests.exceptions.Timeout:
        return {
            "updated": False,
            "error": "Update server timeout"
        }

    except requests.exceptions.ConnectionError:
        return {
            "updated": False,
            "error": "Unable to connect to update server"
        }

    except Exception as e:
        return {
            "updated": False,
            "error": str(e)
        }
    
    