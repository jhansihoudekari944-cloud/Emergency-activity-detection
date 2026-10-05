import math
import time

class FallDetector:

    def __init__(self):

        self.previous_angle = 90

        self.fall_start_time = None

        self.angle_threshold = 45

        self.angle_change = 35

    def calculate_angle(self, shoulder, hip):

        dx = shoulder.x - hip.x
        dy = shoulder.y - hip.y

        return abs(math.degrees(math.atan2(dy, dx)))

    def detect_fall(self, pose_results, moving):

        if not pose_results.pose_landmarks:
            return False, 0

        landmarks = pose_results.pose_landmarks.landmark

        ls = landmarks[11]
        rs = landmarks[12]

        lh = landmarks[23]
        rh = landmarks[24]

        sx = (ls.x + rs.x)/2
        sy = (ls.y + rs.y)/2

        hx = (lh.x + rh.x)/2
        hy = (lh.y + rh.y)/2

        class Point:
            pass

        shoulder = Point()
        shoulder.x = sx
        shoulder.y = sy

        hip = Point()
        hip.x = hx
        hip.y = hy

        angle = self.calculate_angle(shoulder, hip)

        sudden_change = abs(angle - self.previous_angle)

        self.previous_angle = angle

        # Possible fall started
        if angle < self.angle_threshold and sudden_change > self.angle_change:

            if self.fall_start_time is None:

                self.fall_start_time = time.time()

        else:

            self.fall_start_time = None

        # Confirm fall only if person stays still
        if self.fall_start_time is not None:

            elapsed = time.time() - self.fall_start_time

            if elapsed > 1 and not moving:

                return True, angle

        return False, angle