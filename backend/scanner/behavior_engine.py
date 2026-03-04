import os

# -----------------------------------------
# Suspicious behavior patterns by file type
# -----------------------------------------
BEHAVIOR_RULES = {
    ".exe": ["modifying registry", "injecting process", "attempting mass encryption"],
    ".msi": ["creating new services", "auto-startup installation"],
    ".com": ["direct memory access", "self-replication"],

    ".py": ["downloading payload from internet", "executing system commands"],
    ".js": ["browser hijacking", "network beaconing"],

    ".sh": ["modifying system permissions", "remote command execution"],
    ".bat": ["running system-level commands", "registry modification"],

    ".bin": ["low-level device access"],
    ".dll": ["process injection", "export hooking"],

    ".pdf": ["embedded javascript"],
    ".doc": ["macros detected"],
    ".docx": ["macros detected"],
    ".xls": ["auto-macro execution"],
    ".xlsx": ["auto-macro execution"],
    ".ppt": ["macro objects detected"],
    ".pptx": ["macro objects detected"],

    ".jpg": ["embedded steganography"],
    ".jpeg": ["embedded steganography"],
    ".png": ["embedded steganography"],
    ".gif": ["embedded steganography"],

    ".mp3": ["hidden metadata channels"],
    ".wav": ["hidden metadata channels"],
    ".mp4": ["suspicious embedded data"],
    ".avi": ["suspicious embedded data"],
    ".mkv": ["suspicious embedded data"],

    ".zip": ["archive contains executables"],
    ".rar": ["archive contains executables"],
    ".7z": ["archive contains executables"],
    ".tar": ["archive contains scripts"],
    ".gz": ["archive contains scripts"],

    ".apk": ["permissions abuse", "background service creation"],
    ".ipa": ["private API usage"],

    ".iso": ["boot sector modification"],

    ".html": ["inline javascript injection"],
    ".htm": ["inline javascript injection"]
}


def behavior_scan(file_path):
    """
    Simulates a behavior-based scan based on file extension
    and known malicious behavior patterns.
    """

    extension = os.path.splitext(file_path)[1].lower()

    # If extension is recognized, return the expected behavior patterns
    if extension in BEHAVIOR_RULES:
        actions = BEHAVIOR_RULES[extension]

        return {
            "behavior_score": len(actions),  # simple scoring model
            "actions": actions
        }

    # Default fallback for unknown file types
    return {
        "behavior_score": 0,
        "actions": []
    }