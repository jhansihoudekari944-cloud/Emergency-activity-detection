import streamlit as st
import cv2
import os
from datetime import datetime

from utils.location import get_live_location
from utils.database import EmergencyDatabase
from utils.screenshot import save_alert
from utils.alarm import play_alarm

from modules.person_detector import PersonDetector
from modules.pose_detector import PoseDetector
from modules.motion_detector import MotionDetector
from modules.fall_detector import FallDetector
from modules.hand_gesture import HandGestureDetector
from modules.decision_engine import DecisionEngine


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Emergency Detection",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 AI Emergency Activity Detection System")


# =========================================================
# DATABASE
# =========================================================

database = EmergencyDatabase()


# =========================================================
# SESSION STATE
# =========================================================

if "monitoring" not in st.session_state:
    st.session_state.monitoring = False

if "alert_saved" not in st.session_state:
    st.session_state.alert_saved = False

if "latitude" not in st.session_state:
    st.session_state.latitude = None

if "longitude" not in st.session_state:
    st.session_state.longitude = None

if "camera" not in st.session_state:
    st.session_state.camera = None


# =========================================================
# LOCATION
# =========================================================

st.subheader("📍 Live Location")

location_col1, location_col2 = st.columns(2)


# ---------------------------------------------------------
# GET LOCATION BUTTON
# ---------------------------------------------------------

with location_col1:

    if st.button(
        "📍 Get Current Location",
        key="get_location_button",
        width="stretch"
    ):

        location = get_live_location()

        if location:

            st.session_state.latitude = location[0]
            st.session_state.longitude = location[1]

            st.success("✅ Location Found")

        else:

            st.session_state.latitude = None
            st.session_state.longitude = None

            st.error(
                "❌ Location permission denied "
                "or location unavailable."
            )


# ---------------------------------------------------------
# SHOW LOCATION
# ---------------------------------------------------------

with location_col2:

    lat = st.session_state.latitude
    lon = st.session_state.longitude

    if lat is not None and lon is not None:

        st.write(f"**Latitude:** {lat}")
        st.write(f"**Longitude:** {lon}")

        st.markdown(
            f"[📍 Open Location in Google Maps]"
            f"(https://www.google.com/maps?q={lat},{lon})"
        )

    else:

        st.info("📍 Location not available yet.")


st.divider()


# =========================================================
# MONITORING CONTROLS
# =========================================================

st.subheader("🎥 Emergency Monitoring")

control_col1, control_col2 = st.columns(2)


# =========================================================
# START MONITORING
# =========================================================

with control_col1:

    if st.button(
        "▶️ START MONITORING",
        key="start_monitoring_button",
        width="stretch"
    ):

        # ---------------------------------------------
        # Get location
        # ---------------------------------------------

        location = get_live_location()

        if location:

            st.session_state.latitude = location[0]
            st.session_state.longitude = location[1]

        else:

            st.session_state.latitude = None
            st.session_state.longitude = None


        # ---------------------------------------------
        # Open camera
        # ---------------------------------------------

        camera = cv2.VideoCapture(0)

        if camera.isOpened():

            st.session_state.camera = camera
            st.session_state.monitoring = True
            st.session_state.alert_saved = False

            st.rerun()

        else:

            camera.release()

            st.error(
                "❌ Could not open camera."
            )


# =========================================================
# STOP MONITORING
# =========================================================

with control_col2:

    if st.button(
        "⏹️ STOP MONITORING",
        key="stop_monitoring_button",
        width="stretch"
    ):

        st.session_state.monitoring = False
        st.session_state.alert_saved = False

        if st.session_state.camera is not None:

            st.session_state.camera.release()

            st.session_state.camera = None

        st.success(
            "🛑 Monitoring stopped."
        )

        st.rerun()


st.divider()


# =========================================================
# DASHBOARD
# =========================================================

st.subheader("📊 Emergency Monitoring Dashboard")

status_box = st.empty()

frame_placeholder = st.empty()


# =========================================================
# METRICS
# =========================================================

metric_col1, metric_col2, metric_col3, metric_col4 = (
    st.columns(4)
)

people_box = metric_col1.empty()
fall_box = metric_col2.empty()
motion_box = metric_col3.empty()
sos_box = metric_col4.empty()

score_box = st.empty()


# =========================================================
# LOAD AI MODELS ONCE
# =========================================================

@st.cache_resource
def load_models():

    person_detector = PersonDetector()

    pose_detector = PoseDetector()

    motion_detector = MotionDetector()

    fall_detector = FallDetector()

    hand_detector = HandGestureDetector()

    decision = DecisionEngine()

    return (
        person_detector,
        pose_detector,
        motion_detector,
        fall_detector,
        hand_detector,
        decision
    )


# =========================================================
# MONITORING FUNCTION
# =========================================================

@st.fragment(run_every=0.1)
def monitoring_area():

    # -----------------------------------------------------
    # CHECK MONITORING
    # -----------------------------------------------------

    if not st.session_state.monitoring:

        status_box.info(
            "⏹️ Monitoring is stopped. "
            "Press START MONITORING to begin."
        )

        return


    # -----------------------------------------------------
    # CAMERA
    # -----------------------------------------------------

    camera = st.session_state.camera

    if camera is None:

        status_box.error(
            "❌ Camera is not available."
        )

        st.session_state.monitoring = False

        return


    if not camera.isOpened():

        status_box.error(
            "❌ Camera is not opened."
        )

        st.session_state.monitoring = False

        return


    # -----------------------------------------------------
    # LOAD AI MODELS
    # -----------------------------------------------------

    (
        person_detector,
        pose_detector,
        motion_detector,
        fall_detector,
        hand_detector,
        decision
    ) = load_models()


    # -----------------------------------------------------
    # READ FRAME
    # -----------------------------------------------------

    ret, frame = camera.read()

    if not ret:

        status_box.error(
            "❌ Could not read camera frame."
        )

        return


    # =====================================================
    # PERSON DETECTION
    # =====================================================

    detections = person_detector.detect(
        frame
    )


    # =====================================================
    # POSE DETECTION
    # =====================================================

    pose_results = pose_detector.detect_pose(
        frame
    )

    frame = pose_detector.draw_pose(
        frame,
        pose_results
    )


    # =====================================================
    # MOTION DETECTION
    # =====================================================

    moving, no_motion = (
        motion_detector.detect_motion(
            frame
        )
    )


    # =====================================================
    # FALL DETECTION
    # =====================================================

    fall, angle = (
        fall_detector.detect_fall(
            pose_results,
            moving
        )
    )


    # =====================================================
    # HAND GESTURE DETECTION
    # =====================================================

    hand_results = hand_detector.detect(
        frame
    )

    frame = hand_detector.draw(
        frame,
        hand_results
    )

    sos = hand_detector.is_sos_gesture(
        hand_results
    )


    # =====================================================
    # DECISION ENGINE
    # =====================================================

    emergency, score = decision.evaluate(
        fall,
        moving,
        sos,
        False
    )


    # =====================================================
    # UPDATE METRICS
    # =====================================================

    people_box.metric(
        "👤 People",
        len(detections)
    )

    fall_box.metric(
        "🤕 Fall",
        str(fall)
    )

    motion_box.metric(
        "🏃 Moving",
        str(moving)
    )

    sos_box.metric(
        "✋ SOS",
        str(sos)
    )

    score_box.metric(
        "🚨 Emergency Score",
        score
    )


    # =====================================================
    # EMERGENCY DETECTED
    # =====================================================

    if emergency:

        status_box.error(
            "🚨 EMERGENCY DETECTED"
        )


        # -------------------------------------------------
        # PLAY ALARM
        # -------------------------------------------------

        play_alarm()


        # -------------------------------------------------
        # SAVE EMERGENCY ONLY ONCE
        # -------------------------------------------------

        if not st.session_state.alert_saved:

            # ---------------------------------------------
            # SAVE SCREENSHOT
            # ---------------------------------------------

            screenshot = save_alert(
                frame
            )

            screenshot = os.path.abspath(
                screenshot
            )

            print(
                "📸 Screenshot saved:",
                screenshot
            )


            # ---------------------------------------------
            # GET LOCATION
            # ---------------------------------------------

            lat = st.session_state.latitude
            lon = st.session_state.longitude


            # ---------------------------------------------
            # CURRENT TIME
            # ---------------------------------------------

            current_time = (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )


            # ---------------------------------------------
            # SAVE DATABASE
            # ---------------------------------------------

            database.save_alert(
                current_time,
                lat,
                lon,
                screenshot,
                "SOS",
                score
            )


            print(
                "🚨 Emergency saved to database"
            )


            # ---------------------------------------------
            # PREVENT DUPLICATE ALERTS
            # ---------------------------------------------

            st.session_state.alert_saved = True


    # =====================================================
    # SAFE
    # =====================================================

    else:

        status_box.success(
            "✅ SAFE"
        )

        # Ready for next emergency
        st.session_state.alert_saved = False


    # =====================================================
    # DISPLAY CAMERA
    # =====================================================

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    frame_placeholder.image(
        rgb,
        channels="RGB",
        width="stretch"
    )


# =========================================================
# START MONITORING AREA
# =========================================================

monitoring_area()


# =========================================================
# EMERGENCY HISTORY
# =========================================================

st.divider()

st.subheader("🚨 Emergency History")


alerts = database.get_alerts()


if alerts:

    for alert in alerts:

        alert_id = alert[0]
        date_time = alert[1]
        latitude = alert[2]
        longitude = alert[3]
        screenshot = alert[4]
        emergency_type = alert[5]
        score = alert[6]


        # -------------------------------------------------
        # ALERT EXPANDER
        # -------------------------------------------------

        with st.expander(
            f"🚨 Alert #{alert_id} | "
            f"{emergency_type} | "
            f"{date_time}"
        ):

            history_col1, history_col2 = (
                st.columns(2)
            )


            # =================================================
            # ALERT DETAILS
            # =================================================

            with history_col1:

                st.write(
                    "**Emergency Type:**",
                    emergency_type
                )

                st.write(
                    "**Score:**",
                    score
                )

                st.write(
                    "**Date & Time:**",
                    date_time
                )

                st.write(
                    "**Location:**",
                    latitude,
                    longitude
                )


                # ---------------------------------------------
                # GOOGLE MAPS
                # ---------------------------------------------

                if (
                    latitude is not None
                    and longitude is not None
                ):

                    st.markdown(
                        f"[📍 Open Location in Google Maps]"
                        f"(https://www.google.com/maps?"
                        f"q={latitude},{longitude})"
                    )

                else:

                    st.warning(
                        "📍 Location was not available."
                    )


            # =================================================
            # SCREENSHOT
            # =================================================

            with history_col2:

                if screenshot:

                    screenshot_path = os.path.abspath(
                        screenshot
                    )


                    if os.path.exists(
                        screenshot_path
                    ):

                        st.image(
                            screenshot_path,
                            caption="📸 Emergency Screenshot",
                            width="stretch"
                        )

                    else:

                        st.error(
                            "❌ Screenshot file not found."
                        )

                        st.code(
                            screenshot_path
                        )

                else:

                    st.warning(
                        "⚠️ No screenshot stored."
                    )


else:

    st.info(
        "No emergency alerts recorded yet."
    )