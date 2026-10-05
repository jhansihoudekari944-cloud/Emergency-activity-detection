from utils.database import EmergencyDatabase
from datetime import datetime
import cv2
from modules.screenshots import save_alert
from modules.screenshots import ScreenshotLogger
import config
from utils.logger import save_alert
from utils.alarm import play_alarm
from modules.person_detector import PersonDetector
from modules.pose_detector import PoseDetector
from modules.motion_detector import MotionDetector
from modules.fall_detector import FallDetector
from modules.hand_gesture import HandGestureDetector
from modules.decision_engine import DecisionEngine

# Uncomment ONLY if you have models/fire.pt
# from modules.fire_detector import FireDetector


# -------------------------
# Initialize Modules
# -------------------------

detector = PersonDetector()
pose_detector = PoseDetector()
motion_detector = MotionDetector()
fall_detector = FallDetector()
hand_detector = HandGestureDetector()
decision = DecisionEngine()
alert_saved = False
decision = DecisionEngine()
screenshot = ScreenshotLogger()
database = EmergencyDatabase()


# Uncomment ONLY if fire model exists
# fire_detector = FireDetector()


# -------------------------
# Camera
# -------------------------

cap = cv2.VideoCapture(config.CAMERA_INDEX)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
import time
last_saved = 0
alert_saved = False


while True:

    ret, frame = cap.read()

    if not ret:
        break

    # ==========================
    # Person Detection
    # ==========================

    detections = detector.detect(frame)

    # ==========================
    # Pose Detection
    # ==========================

    pose_results = pose_detector.detect_pose(frame)
    frame = pose_detector.draw_pose(frame, pose_results)

    # ==========================
    # Motion Detection
    # ==========================

    moving, no_motion_time = motion_detector.detect_motion(frame)

    # ==========================
    # Fall Detection
    # ==========================

    fall_detected, angle = fall_detector.detect_fall(
        pose_results,
        moving
    )

    # ==========================
    # Hand Gesture
    # ==========================

    hand_results = hand_detector.detect(frame)
    frame = hand_detector.draw(frame, hand_results)
    

    hand_detected = hand_detector.is_sos_gesture(hand_results)
    print("SOS:", hand_detected)
    print("Hand:", hand_detected)


    # ==========================
    # Fire Detection (Optional)
    # ==========================

    fire_detected = False

    # Uncomment if fire model exists

    """
    fire_detected, fire_box = fire_detector.detect(frame)

    if fire_detected:

        x1, y1, x2, y2 = fire_box

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 0, 255),
            3
        )

        cv2.putText(
            frame,
            "FIRE",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
    """

    # ==========================
    # Decision Engine
    # ==========================

    emergency = hand_detected
    score = 100 if emergency else 0
    print("---------------------")
    print("Fall:", fall_detected)
    print("Moving:", moving)
    print("Hand:", hand_detected)
    print("Emergency:", emergency)
    print("Score:", score)

    # ==========================
    # Draw Person Boxes
    # ==========================

    for person in detections:

        x1, y1, x2, y2 = person["bbox"]
        confidence = person["confidence"]

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Person {confidence:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # ==========================
    # Information Panel
    # ==========================

    cv2.putText(
        frame,
        f"People : {len(detections)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 0, 0),
        2
    )

    cv2.putText(
        frame,
        f"Body Angle : {angle:.1f}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # Fall Status

    status = "EMERGENCY FAIL" if fall_detected else "NORMAL"

    color = (0, 0, 255) if fall_detected else (0, 255, 0)

    cv2.putText(
        frame,
        status,
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3
    )

    # Motion

    motion_status = "MOVING" if moving else "NO MOVEMENT"

    motion_color = (0, 255, 0) if moving else (0, 0, 255)

    cv2.putText(
        frame,
        motion_status,
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        motion_color,
        2
    )

    cv2.putText(
        frame,
        f"No Motion : {no_motion_time:.1f}s",
        (20, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # Hand

    gesture_status = "SOS:YES" if hand_detected else "SOS:NO"
    gesture_color = (
    (0, 0, 255)
    if hand_detected
    else (0, 255, 0)
    )

    gesture_color = (0, 255, 0) if hand_detected else (0, 0, 255)

    # Final Status

    if emergency:
        play_alarm()

        if not alert_saved:
            filename = save_alert(frame)
            current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
            )

            # Temporary location
            lat = 17.562682
            lon = 78.451521

            database.save_alert(
                current_time,
                lat,
                lon,
                filename,
                "SOS",
                score
            )

            print("Saved to Database")

            alert_saved = True

        cv2.putText(
            frame,
            "EMERGENCY DETECTED",
            (20, 330),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        cv2.putText(
            frame,
            "SCREENSHOT SAVED",
            (20, 370),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 255),
            2
        )

    else:
        # Ready for the next emergency
        alert_saved = False

        cv2.putText(
        frame,
        "SAFE",
        (20, 330),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        3
        )

   

    # ==========================
    # Show Frame
    # ==========================
    cv2.imshow("AI Emergency Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()