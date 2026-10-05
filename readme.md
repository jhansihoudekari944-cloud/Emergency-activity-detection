# 🚨 AI Emergency Activity Detection System

An AI-powered real-time emergency activity detection system that uses computer vision and machine learning techniques to identify potentially dangerous situations and generate alerts automatically.

## 📌 Overview

The **AI Emergency Activity Detection System** is designed to monitor video/camera input and detect abnormal or emergency activities.

The system combines multiple computer vision modules such as:

* 👤 Person Detection
* 🧍 Pose Detection
* 🏃 Motion Detection
* 🤕 Fall Detection
* ✋ Hand Gesture Detection
* 🧠 Decision Engine
* 📸 Evidence/Screenshot Capture
* 🔔 Emergency Alerts
* 🗄️ Alert Database Logging

The detected activities are processed by a decision engine to determine whether an emergency situation has occurred.

---

## ✨ Features

### 👤 Person Detection

Detects people appearing in the camera/video stream.

### 🧍 Pose Detection

Analyzes human body posture to understand the person's activity.

### 🏃 Motion Detection

Detects significant movement and changes between video frames.

### 🤕 Fall Detection

Identifies patterns that may indicate a person has fallen.

### ✋ Hand Gesture Detection

Detects predefined hand gestures that can be used as emergency signals.

### 🧠 Decision Engine

Combines information from different detection modules and determines whether an emergency should be triggered.

### 📸 Evidence Capture

Captures screenshots when an emergency event is detected.

### 🔔 Emergency Alert

Generates an alert when the system determines that an emergency situation has occurred.

### 🗄️ Database Logging

Stores detected emergency events and relevant information for later review.

---

## 🏗️ Project Structure

```text
AI_Emergency_Detection/
│
├── alerts/
│
├── assets/
│
├── database/
│
├── emergency_screenshots/
│
├── evidence/
│
├── modules/
│   ├── decision_engine.py
│   ├── fall_detector.py
│   ├── hand_gesture.py
│   ├── motion_detector.py
│   ├── person_detection.py
│   └── pose_detection.py
│
├── utils/
│
├── app.py
├── config.py
├── dashboard.py
├── emergency.py
├── emergencyactivityapp.py
│
├── requirements.txt
│
├── test_alarm.py
├── test_database.py
└── test_screenshot.py
```

---

## 🔄 System Workflow

```text
Camera / Video Input
        │
        ▼
   Person Detection
        │
        ▼
    Pose Detection
        │
        ├──────────────┐
        ▼              ▼
 Motion Detection   Fall Detection
        │              │
        └──────┬───────┘
               ▼
       Hand Gesture Detection
               │
               ▼
        Decision Engine
               │
        ┌──────┴──────┐
        ▼             ▼
   Normal Event   Emergency Event
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
           Alert   Screenshot  Database
```

---

## 🛠️ Technologies Used

* **Python**
* **OpenCV**
* **Computer Vision**
* **Machine Learning**
* **Pose Estimation**
* **Object Detection**
* **Motion Analysis**
* **Database Management**

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/jhansihoudekari944-cloud/Emergency-activity-detection.git
```

### 2. Navigate to the project

```bash
cd Emergency-activity-detection
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

After installing the required dependencies, run the main application:

```bash
python emergencyactivityapp.py
```

> The exact entry point may depend on the configuration of your local project.

---

## 🧪 Testing

The project contains separate test files for important components:

```bash
python test_alarm.py
python test_database.py
python test_screenshot.py
```

---

## 📸 Evidence and Alerts

When an emergency activity is detected, the system can:

1. Identify the emergency activity.
2. Trigger an alert.
3. Capture supporting evidence.
4. Store the event information.
5. Allow the event to be reviewed later.

---

## 🎯 Project Goals

The main goals of this project are:

* Automate emergency activity detection.
* Reduce the need for continuous manual monitoring.
* Detect potentially dangerous activities in real time.
* Generate alerts automatically.
* Preserve evidence of detected events.
* Provide a foundation for intelligent safety-monitoring systems.

---

## 🚀 Future Improvements

Possible future enhancements include:

* Real-time notification through mobile applications.
* SMS/email emergency notifications.
* Cloud-based monitoring.
* Improved detection accuracy.
* Multi-camera support.
* Advanced activity recognition.
* Web-based monitoring dashboard.
* Deployment on edge devices.

---

## 👩‍💻 Author

**Jhansi Houdekari**

AI / Computer Vision Project

---

## 📄 License

This project is intended for educational and project-development purposes.
