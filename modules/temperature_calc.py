import math

def f_to_c(temp_f):
    return (temp_f - 32) * 5 / 9


def select_transmitter_range(tmax_c):
    tmax_design = tmax_c * 1.10
    range_sup = math.ceil(tmax_design / 10) * 10
    return 0, range_sup


def sensor_error(sensor_type, sensor_class, temp_c):
    if sensor_type == "RTD":
        if sensor_class == "A":
            return 0.15 + 0.002 * abs(temp_c)
        elif sensor_class == "B":
            return 0.3 + 0.005 * abs(temp_c)
    elif sensor_type == "TC":
        return 2.2
    raise ValueError("Sensor no válido")


def transmitter_error(span):
    return 0.001 * span   # 0.1 % span


def total_error(err_sensor, err_tx):
    return math.sqrt(err_sensor**2 + err_tx**2)
