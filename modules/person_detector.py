from ultralytics import YOLO

class PersonDetector:

    def __init__(self):

        # Load YOLO model
        self.model = YOLO("yolo11n.pt")

    def detect(self, frame):

        results = self.model(frame, verbose=False)

        detections = []

        for result in results:

            for box in result.boxes:

                cls = int(box.cls[0])

                confidence = float(box.conf[0])

                # Person class in COCO dataset = 0
                if cls == 0 and confidence > 0.5:

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    detections.append({

                        "bbox": (x1, y1, x2, y2),
                        "confidence": confidence

                    })

        return detections