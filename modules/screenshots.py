import cv2
import os
from datetime import datetime


# -------------------------------------------------
# Folder where emergency screenshots are stored
# -------------------------------------------------

ALERT_FOLDER = "alerts"

os.makedirs(ALERT_FOLDER, exist_ok=True)


# -------------------------------------------------
# Save emergency screenshot
# -------------------------------------------------

def save_alert(frame):
    """
    Save the current video frame as an emergency screenshot.

    Returns:
        filename: path of the saved screenshot
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = os.path.join(
        ALERT_FOLDER,
        f"emergency_{timestamp}.jpg"
    )

    success = cv2.imwrite(filename, frame)

    if success:
        print(f"Emergency screenshot saved: {filename}")
        return filename

    print("ERROR: Could not save emergency screenshot")
    return None


# -------------------------------------------------
# Screenshot Logger
# -------------------------------------------------

class ScreenshotLogger:

    def __init__(self, folder=ALERT_FOLDER):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)

    def save(self, frame):
        """
        Save a screenshot using the logger.
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = os.path.join(
            self.folder,
            f"emergency_{timestamp}.jpg"
        )

        success = cv2.imwrite(filename, frame)

        if success:
            print(f"Screenshot saved: {filename}")
            return filename

        print("ERROR: Could not save screenshot")
        return None