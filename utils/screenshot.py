import cv2
import os
from datetime import datetime


class ScreenshotLogger:

    def __init__(self):

        # Project root folder
        project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.folder = os.path.join(
            project_root,
            "evidence"
        )

        os.makedirs(
            self.folder,
            exist_ok=True
        )

    def save(self, frame):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        filename = f"emergency_{timestamp}.jpg"

        path = os.path.join(
            self.folder,
            filename
        )

        success = cv2.imwrite(
            path,
            frame
        )

        print("================================")
        print("Screenshot Save")
        print("Success:", success)
        print("Path:", path)
        print("Exists:", os.path.exists(path))
        print("================================")

        if success:

            return path

        return None


def save_alert(frame):

    logger = ScreenshotLogger()

    return logger.save(frame)