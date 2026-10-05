# config.py

# Camera
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Detection Thresholds
PERSON_CONFIDENCE = 0.50
FIRE_CONFIDENCE = 0.60

# Fall Detection
FALL_TIME_THRESHOLD = 10      # seconds
MOTION_THRESHOLD = 20

# Fire Detection
FIRE_AREA_THRESHOLD = 0.02    # 2% of image area

# Screenshot Folder
SCREENSHOT_FOLDER = "screenshots"

# Database
DATABASE_NAME = "database/emergency.db"

# Alarm
ALARM_SOUND = "assets/alarm.wav"