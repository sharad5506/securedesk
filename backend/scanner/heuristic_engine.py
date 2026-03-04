import os

def heuristic_scan(file_path):
    size = os.path.getsize(file_path)
    ext = os.path.splitext(file_path)[1].lower()

    suspicion = []

    # ---------------------------------------------------------
    # 1. EXECUTABLES (.exe, .dll, .bin, .msi, etc.)
    # ---------------------------------------------------------
    executable_ext = [".exe", ".msi", ".com", ".dll", ".bin"]
    if ext in executable_ext:
        if size > 30 * 1024 * 1024:
            suspicion.append("Large executable (possible packed malware)")

        # PE HEADER CHECK
        with open(file_path, "rb") as f:
            header = f.read(2)
            if header != b"MZ":
                suspicion.append("Executable missing MZ header (tampered or packed)")

    # ---------------------------------------------------------
    # 2. OFFICE DOCUMENTS (.docx, .pptx, .xlsx)
    # ---------------------------------------------------------
    office_ext = [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"]
    if ext in office_ext:
        if size > 5 * 1024 * 1024:
            suspicion.append("Large Office document (possible macro virus)")

    # ---------------------------------------------------------
    # 3. SCRIPTS (.js, .py, .sh, .bat)
    # ---------------------------------------------------------
    script_ext = [".js", ".py", ".sh", ".bat"]
    if ext in script_ext:
        try:
            with open(file_path, "r", errors="ignore") as f:
                content = f.read()

                dangerous_keywords = ["eval(", "exec(", "base64", "import os", "subprocess", "cmd.exe"]
                for kw in dangerous_keywords:
                    if kw in content:
                        suspicion.append(f"Script contains dangerous keyword: {kw}")
        except:
            suspicion.append("Script unreadable — possible obfuscation")

    # ---------------------------------------------------------
    # 4. HTML / HTM (WEB FILES)
    # ---------------------------------------------------------
    if ext in [".html", ".htm"]:
        with open(file_path, "r", errors="ignore") as f:
            html = f.read()
            if "<script>" in html or "javascript:" in html:
                suspicion.append("HTML contains embedded JavaScript (possible XSS payload)")
            if "onerror=" in html or "onload=" in html:
                suspicion.append("HTML contains suspicious event handlers")

    # ---------------------------------------------------------
    # 5. PDF FILES
    # ---------------------------------------------------------
    if ext == ".pdf":
        with open(file_path, "rb") as f:
            pdf = f.read()
            if b"/JS" in pdf or b"/JavaScript" in pdf:
                suspicion.append("PDF contains JavaScript (possible exploit)")
            if b"/OpenAction" in pdf:
                suspicion.append("PDF auto-execute trigger detected")

    # ---------------------------------------------------------
    # 6. IMAGES (JPG/PNG) — MALICIOUS EXIF
    # ---------------------------------------------------------
    if ext in [".jpg", ".jpeg", ".png", ".gif"]:
        if size > 15 * 1024 * 1024:
            suspicion.append("Suspiciously large image file (possible steganography)")

    # ---------------------------------------------------------
    # 7. AUDIO/VIDEO — CHECK SIZE
    # ---------------------------------------------------------
    if ext in [".mp3", ".wav", ".mp4", ".avi", ".mkv"]:
        if size > 500 * 1024 * 1024:
            suspicion.append("Very large media file (possible hidden data)")

    # ---------------------------------------------------------
    # 8. ARCHIVES (.zip, .rar, .7z, .tar, .gz) — ARCHIVE BOMB
    # ---------------------------------------------------------
    archive_ext = [".zip", ".rar", ".7z", ".tar", ".gz"]
    if ext in archive_ext:
        if size > 200 * 1024 * 1024:
            suspicion.append("Large compressed archive (possible zip bomb)")

    # ---------------------------------------------------------
    # 9. MOBILE APPS (.apk, .ipa)
    # ---------------------------------------------------------
    if ext == ".apk":
        if size > 30 * 1024 * 1024:
            suspicion.append("Large APK (possible injected payload)")

    if ext == ".ipa":
        if size > 40 * 1024 * 1024:
            suspicion.append("Large iOS app (possible unsafe content)")

    # ---------------------------------------------------------
    # 10. ISO / DISK IMAGES
    # ---------------------------------------------------------
    if ext == ".iso":
        if size > 1 * 1024 * 1024 * 1024:
            suspicion.append("Suspiciously large ISO image")

    # ---------------------------------------------------------
    # FINAL OUTPUT
    # ---------------------------------------------------------
    return {
        "suspicious": len(suspicion) > 0,
        "reasons": suspicion
    }