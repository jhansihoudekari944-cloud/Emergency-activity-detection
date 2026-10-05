from utils.database import EmergencyDatabase

database = EmergencyDatabase()

alerts = database.get_alerts()

print("\n========== EMERGENCY ALERTS ==========\n")

for alert in alerts:

    print("ID          :", alert[0])
    print("Date/Time   :", alert[1])
    print("Latitude    :", alert[2])
    print("Longitude   :", alert[3])
    print("Screenshot  :", alert[4])
    print("Type        :", alert[5])
    print("Score       :", alert[6])

    print("--------------------------------------")