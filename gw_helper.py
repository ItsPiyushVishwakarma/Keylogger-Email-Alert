import pygetwindow as gw

def get_active_window():
    try:
        window = gw.getActiveWindow()
        return window.title if window else "Unknown"
    except Exception:
        return "Unknown"