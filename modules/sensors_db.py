# modules/sensors_db.py

SENSORS = [
    {"model": "Rosemount 214C", "type": "RTD", "tmin": -200, "tmax": 600, "error": 0.15},
    {"model": "Endress TR10", "type": "RTD", "tmin": -50, "tmax": 400, "error": 0.20},
    {"model": "Yokogawa YTA110", "type": "TC", "tmin": -200, "tmax": 1100, "error": 2.0},
]

def select_sensor(tmax_design):
    """
    Selecciona el sensor más preciso que cubra la temperatura de diseño.
    """
    candidates = [s for s in SENSORS if s["tmax"] >= tmax_design]
    candidates.sort(key=lambda x: x["error"])
    return candidates[0] if candidates else None
