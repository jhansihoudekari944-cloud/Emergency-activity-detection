import cv2
from utils.screenshot import save_alert


cap = cv2.VideoCapture(0)

ret, frame = cap.read()

if ret:

    filename = save_alert(frame)

    print("Returned path:")
    print(filename)

else:

    print("Could not read camera frame")

cap.release()