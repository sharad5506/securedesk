import os
import hashlib

# -----------------------------------------
# SUPPORTED FILE TYPES
# -----------------------------------------
SUPPORTED_TYPES = [
    # Executables
    ".exe", ".msi", ".com",

    # Scripts
    ".py", ".js", ".sh", ".bat",

    # System / Binary
    ".bin", ".dll",

    # Documents
    ".pdf", ".doc", ".docx",
    ".xls", ".xlsx",
    ".ppt", ".pptx",

    # Images
    ".jpg", ".jpeg", ".png", ".gif",

    # Audio
    ".mp3", ".wav",

    # Video
    ".mp4", ".avi", ".mkv",

    # Archives
    ".zip", ".rar", ".7z", ".tar", ".gz",

    # Mobile Apps
    ".apk", ".ipa",

    # Disk Images
    ".iso",

    # Web Files
    ".html", ".htm"
]

# -----------------------------------------
# MAGIC SIGNATURES (real file-type headers)
# -----------------------------------------
MAGIC_SIGNATURES = {
    b"MZ": ".exe",  # Windows EXE
    b"\x50\x4B\x03\x04": ".zip",  # ZIP/Office
    b"%PDF": ".pdf",
    b"\xFF\xD8\xFF": ".jpg",
    b"\x89PNG": ".png",
    b"GIF87a": ".gif",
    b"GIF89a": ".gif",
    b"\x52\x61\x72\x21": ".rar",  # RAR
    b"\x1F\x8B": ".gz",
    b"\x00\x00\x01\x00": ".ico",
    b"OggS": ".mp3",
    b"ID3": ".mp3",
    b"RIFF": ".wav",
}

# -----------------------------------------
# KNOWN MALWARE HASHES (fake demo samples)
# -----------------------------------------
KNOWN_BAD_HASHES = {
    "e99a18c428cb38d5f260853678922e03",  # demo MD5
    "44d88612fea8a8f36de82e1278abb02f",  # EICAR test virus
}


def compute_md5(file_path):
    """Compute MD5 hash safely for malware scanning."""
    hasher = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                hasher.update(block)
        return hasher.hexdigest()
    except Exception:
        return None


def detect_magic(file_path):
    """Detect file type using magic-number headers."""
    try:
        with open(file_path, "rb") as f:
            header = f.read(8)

        for sig, ext in MAGIC_SIGNATURES.items():
            if header.startswith(sig):
                return ext

    except:
        pass

    return None


def signature_scan(file_path):
    """
    Main signature-based malware scan.
    Checks:
    ✔ File type by extension
    ✔ Magic number mismatch (fake files)
    ✔ Known malicious signatures (hash match)
    """

    extension = os.path.splitext(file_path)[1].lower()

    # -----------------------------------------
    # 1. Unsupported file type
    # -----------------------------------------
    if extension not in SUPPORTED_TYPES:
        return {
            "status": "unsupported",
            "message": f"File type '{extension}' not supported."
        }

    # -----------------------------------------
    # 2. Magic signature check
    # -----------------------------------------
    detected_magic = detect_magic(file_path)
    if detected_magic and detected_magic != extension:
        return {
            "status": "suspicious",
            "message": "File header does not match extension (possible spoofing)"
        }

    # -----------------------------------------
    # 3. Hash check for known malware
    # -----------------------------------------
    file_hash = compute_md5(file_path)

    if file_hash in KNOWN_BAD_HASHES:
        return {
            "status": "infected",
            "message": "Malicious file signature detected",
            "hash": file_hash
        }

    # -----------------------------------------
    # SAFE RESULT
    # -----------------------------------------
    return {
        "status": "clean",
        "message": "No malicious signature found",
        "hash": file_hash
    }