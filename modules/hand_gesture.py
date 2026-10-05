import cv2
import mediapipe as mp


class HandGestureDetector:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.drawer = mp.solutions.drawing_utils

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return self.hands.process(rgb)

    def draw(self, frame, results):

        if results.multi_hand_landmarks:

            for hand in results.multi_hand_landmarks:

                self.drawer.draw_landmarks(
                    frame,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return frame

    def is_sos_gesture(self, results):
        if not results.multi_hand_landmarks:
            return False

        hand = results.multi_hand_landmarks[0]

        lm = hand.landmark

        # Index
        index = lm[8].y < lm[6].y

        # Middle
        middle = lm[12].y < lm[10].y

        # Ring
        ring = lm[16].y < lm[14].y

        # Little
        little = lm[20].y < lm[18].y

        # If 4 fingers are open, treat as SOS
        if index and middle and ring and little:
            return True

        return False