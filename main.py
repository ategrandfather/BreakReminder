from plyer import notification
import psutil
import threading
import time

NOTIFICATION_TIME = 45 * 60  # minutes
TITLE = "45 minutes past."
MESSAGE = "Go move for a bit."
TIMEOUT = 3  # seconds of  notification appearance

# global variable so timer can be stopped if apps are closed but {NOTIFICATION_TIME} is still not done
timer = None
process_name = ""

# Linux doesn't use .exe for the run files.
# On Windows, just add .exe e.g. 'steam.exe'
TARGET_PROCESSES = [
    "steam",
    "chrome",
    "google-chrome",
    "chromium",
    "firefox-bin",
    "brave",
    "opera",
    "microsoft-edge",
]


def is_target_running() -> bool:
    """Check if any target runs"""
    global process_name
    for proc in psutil.process_iter(["name"]):
        name = proc.info["name"]
        process_name = name
        if name and name.lower() in TARGET_PROCESSES:
            return True
    return False


def notification_call():
    """Send Notification"""
    assert notification.notify is not None
    notification.notify(
        title=TITLE,
        message=MESSAGE,
        timeout=TIMEOUT,
    )


def timer_finished():
    global timer
    print(f"{NOTIFICATION_TIME} minutes passed. Sending notification.")
    notification_call()
    timer = None  # reset timer


def main():
    """Main loop that monitors processes and controlling timer."""
    global timer
    global process_name

    print("Monitoring if any targeted app is working...")

    while True:
        if is_target_running():
            if timer is None:
                print(f"Detected targeted app {process_name}. Timer has started.")
                timer = threading.Timer(NOTIFICATION_TIME, timer_finished)
                timer.start()

        else:
            if timer is not None:
                print("All apps currently closed. Timer stopped.")
                timer.cancel()
                timer = None

        time.sleep(3)


if __name__ == "__main__":
    main()
