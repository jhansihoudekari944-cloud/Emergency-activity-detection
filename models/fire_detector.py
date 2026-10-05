from ultralytics import YOLO

class FireDetector:

    def __init__(self):
        self.model = YOLO("models/fire.pt")

    def detect(self, frame):

        results = self.model(frame, verbose=False)

        fire = False

        for result in results:

            for box in result.boxes:

                conf = float(box.conf[0])

                if conf > 0.50:

                    fire = True

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    return fire, (x1, y1, x2, y2)

        return fire, None