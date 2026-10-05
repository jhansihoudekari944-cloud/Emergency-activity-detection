import cv2
import os
from datetime import datetime

os.makedirs("alerts", exist_ok=True)

def save_alert(frame):

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"alerts/alert_{now}.jpg"

    cv2.imwrite(filename, frame)

    return filename