import sqlite3


class EmergencyDatabase:

    def __init__(self):

        self.conn = sqlite3.connect(
            "emergency.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            date_time TEXT,

            latitude REAL,

            longitude REAL,

            screenshot TEXT,

            emergency_type TEXT,

            score INTEGER
        )
        """)

        self.conn.commit()

    # ==========================================
    # SAVE EMERGENCY ALERT
    # ==========================================

    def save_alert(
        self,
        date_time,
        latitude,
        longitude,
        screenshot,
        emergency_type,
        score
    ):

        self.cursor.execute(
            """
            INSERT INTO alerts
            (
                date_time,
                latitude,
                longitude,
                screenshot,
                emergency_type,
                score
            )

            VALUES
            (?, ?, ?, ?, ?, ?)
            """,

            (
                date_time,
                latitude,
                longitude,
                screenshot,
                emergency_type,
                score
            )
        )

        self.conn.commit()

    # ==========================================
    # GET ALL EMERGENCY ALERTS
    # ==========================================

    def get_alerts(self):

        self.cursor.execute("""
            SELECT
                id,
                date_time,
                latitude,
                longitude,
                screenshot,
                emergency_type,
                score
            FROM alerts
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()
    def close(self):
        self.conn.close()