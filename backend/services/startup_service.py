import os
import shutil


def get_startup_path():
    """
    Returns the full path where SecureDesk should be placed
    inside Windows Startup folder.
    """
    appdata = os.getenv("APPDATA")

    if not appdata:
        raise EnvironmentError("APPDATA not found. Not a Windows system?")

    startup_folder = os.path.join(
        appdata,
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup"
    )

    # Ensure folder exists
    os.makedirs(startup_folder, exist_ok=True)

    return os.path.join(startup_folder, "SecureDesk.exe")


def enable_startup(source_exe="securedesk.exe"):
    """
    Copies SecureDesk executable to Windows Startup folder.
    """
    target = get_startup_path()

    if not os.path.exists(source_exe):
        raise FileNotFoundError(f"Source executable not found: {source_exe}")

    shutil.copy(source_exe, target)

    return f"SecureDesk added to startup: {target}"


def disable_startup():
    """
    Removes SecureDesk from Windows Startup.
    """
    target = get_startup_path()

    if os.path.exists(target):
        os.remove(target)
        return "SecureDesk removed from startup."

    return "SecureDesk was not in startup."