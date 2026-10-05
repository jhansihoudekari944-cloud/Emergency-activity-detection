import cv2
import time

class MotionDetector:
    def __init__(self):
        self.previous_gray = None
        self.no_motion_start = None

    def detect_motion(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.previous_gray is None:
            self.previous_gray = gray
            return True, 0

        frame_diff = cv2.absdiff(self.previous_gray, gray)

        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

        motion_pixels = cv2.countNonZero(thresh)

        self.previous_gray = gray

        if motion_pixels > 5000:

            self.no_motion_start = None

            return True, 0

        else:

            if self.no_motion_start is None:
                self.no_motion_start = time.time()

            elapsed = time.time() - self.no_motion_start

            return False, elapsed