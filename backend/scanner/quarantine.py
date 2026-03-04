import os
import shutil
import time

QUARANTINE_DIR = "backend/data/quarantine/"

# Create folder if missing
os.makedirs(QUARANTINE_DIR, exist_ok=True)


def generate_safe_name(file_name):
    """
    Prevent overwrite by adding timestamp if filename already exists.
    Example: malware.exe → malware_1712345678.exe
    """
    base, ext = os.path.splitext(file_name)
    timestamp = str(int(time.time()))
    return f"{base}_{timestamp}{ext}"


def add_to_quarantine(file_path):
    """
    Move infected file to quarantine folder safely.
    Returns: {"success": bool, "new_path": str}
    """
    if not os.path.exists(file_path):
        return {"success": False, "new_path": None}

    file_name = os.path.basename(file_path)
    quarantine_path = os.path.join(QUARANTINE_DIR, file_name)

    # Avoid file overwrite
    if os.path.exists(quarantine_path):
        file_name = generate_safe_name(file_name)
        quarantine_path = os.path.join(QUARANTINE_DIR, file_name)

    try:
        shutil.move(file_path, quarantine_path)
        return {"success": True, "new_path": quarantine_path}
    except Exception as e:
        return {"success": False, "new_path": None}


def get_quarantine_items():
    """
    List all files stored in quarantine with full paths.
    """
    return [
        os.path.join(QUARANTINE_DIR, f)
        for f in os.listdir(QUARANTINE_DIR)
    ]


def restore_from_quarantine(file_name, restore_path):
    """
    Restore a file from quarantine back to its original or user-selected path.
    """
    q_file = os.path.join(QUARANTINE_DIR, file_name)

    if not os.path.exists(q_file):
        return False

    try:
        shutil.move(q_file, restore_path)
        return True
    except Exception:
        return False


def delete_from_quarantine(file_name):
    """
    Permanently delete a quarantined file.
    """
    q_file = os.path.join(QUARANTINE_DIR, file_name)

    if not os.path.exists(q_file):
        return False

    try:
        os.remove(q_file)
        return True
    except Exception:
        return False