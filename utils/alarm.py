import os
import threading
import winsound

is_playing = False


def play_alarm():

    global is_playing

    if is_playing:
        return

    is_playing = True

    threading.Thread(
        target=_play,
        daemon=True
    ).start()


def _play():

    global is_playing

    try:

        alarm_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "assets",
                "alarm.wav"
            )
        )

        print("Alarm file:", alarm_path)
        print("Alarm exists:", os.path.exists(alarm_path))

        if not os.path.exists(alarm_path):

            print("❌ Alarm file not found!")

            return

        # Play alarm
        winsound.PlaySound(
            alarm_path,
            winsound.SND_FILENAME
        )

    except Exception as e:

        print("❌ Alarm Error:", e)

    finally:

        is_playing = False