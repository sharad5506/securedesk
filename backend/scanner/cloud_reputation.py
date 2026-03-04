import os
import random

# -----------------------------------------
# Cloud Reputation Database (Simulated)
# -----------------------------------------
CLOUD_REPUTATION_DB = {
    ".exe": {"risk": "High", "score_range": (70, 95)},
    ".msi": {"risk": "Medium", "score_range": (40, 70)},
    ".com": {"risk": "High", "score_range": (65, 90)},

    ".py": {"risk": "Medium", "score_range": (40, 65)},
    ".js": {"risk": "Medium", "score_range": (35, 60)},

    ".sh": {"risk": "High", "score_range": (60, 85)},
    ".bat": {"risk": "High", "score_range": (60, 90)},

    ".bin": {"risk": "Medium", "score_range": (30, 55)},
    ".dll": {"risk": "High", "score_range": (70, 95)},

    ".pdf": {"risk": "Low", "score_range": (5, 20)},
    ".doc": {"risk": "Medium", "score_range": (20, 45)},
    ".docx": {"risk": "Medium", "score_range": (20, 45)},
    ".xls": {"risk": "Medium", "score_range": (20, 45)},
    ".xlsx": {"risk": "Medium", "score_range": (20, 45)},
    ".ppt": {"risk": "Low", "score_range": (5, 25)},
    ".pptx": {"risk": "Low", "score_range": (5, 25)},

    ".jpg": {"risk": "Low", "score_range": (1, 10)},
    ".jpeg": {"risk": "Low", "score_range": (1, 10)},
    ".png": {"risk": "Low", "score_range": (1, 10)},
    ".gif": {"risk": "Low", "score_range": (1, 10)},

    ".mp3": {"risk": "Low", "score_range": (1, 10)},
    ".wav": {"risk": "Low", "score_range": (1, 10)},
    ".mp4": {"risk": "Low", "score_range": (1, 10)},
    ".avi": {"risk": "Low", "score_range": (1, 10)},
    ".mkv": {"risk": "Low", "score_range": (1, 10)},

    ".zip": {"risk": "Medium", "score_range": (30, 60)},
    ".rar": {"risk": "Medium", "score_range": (30, 60)},
    ".7z": {"risk": "Medium", "score_range": (30, 60)},
    ".tar": {"risk": "Medium", "score_range": (25, 55)},
    ".gz": {"risk": "Medium", "score_range": (25, 55)},

    ".apk": {"risk": "High", "score_range": (60, 90)},
    ".ipa": {"risk": "High", "score_range": (60, 90)},

    ".iso": {"risk": "High", "score_range": (60, 95)},

    ".html": {"risk": "Medium", "score_range": (25, 50)},
    ".htm": {"risk": "Medium", "score_range": (25, 50)},
}


def cloud_reputation_check(file_path):
    """
    Simulates cloud reputation score like VirusTotal, Hybrid Analysis,
    based on known threat intelligence patterns.
    """

    extension = os.path.splitext(file_path)[1].lower()

    # If extension exists in cloud DB, generate a realistic score
    if extension in CLOUD_REPUTATION_DB:
        info = CLOUD_REPUTATION_DB[extension]
        score_low, score_high = info["score_range"]

        score = random.randint(score_low, score_high)
        risk = info["risk"]

        return {
            "cloud_score": score,
            "risk_level": risk,
            "trusted": score < 30,       # Below 30 = safe
            "unknown": False
        }

    # Unknown file type → mark suspicious
    return {
        "cloud_score": random.randint(20, 50),
        "risk_level": "Unknown",
        "trusted": False,
        "unknown": True
    }