import requests, math
from datetime import datetime, timedelta

t = datetime(2026, 1, 12, 6, 0)

for i in range(50):
    sun_angle = i * 3.6

    for mode in ["fixed", "tracking"]:
        panel_angle = 90 if mode == "fixed" else sun_angle
        
        if mode == "fixed":
           energy = abs(math.cos(math.radians(sun_angle - panel_angle))) * 0.6
        else:
            energy = abs(math.cos(math.radians(sun_angle - panel_angle))) * 0.9


        payload = {
            "timestamp": t.isoformat(),
            "mode": mode,
            "sun_angle": sun_angle,
            "panel_angle": panel_angle,
            "voltage": 18,
            "current": energy,
            "power": 18 * energy,
            "energy": energy
        }

        requests.post("http://127.0.0.1:5000/api", json=payload)

    t += timedelta(minutes=5)

print("done")
