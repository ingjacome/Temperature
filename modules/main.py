from temperature_calc import *
from thermowell import *
from sensors_db import *
from plots import *

# INPUTS
Tn = 120
Tmax = 150
unit = "C"
flow = 3000
velocity = 4
diameter = 6
length = 180
elastic_modulus = 193
density = 1000

if unit == "F":
    Tn = f_to_c(Tn)
    Tmax = f_to_c(Tmax)

# TRANSMISOR
low, high = select_transmitter_range(Tmax)
span = high - low

# SENSOR
sensor = select_sensor(high)
err_sensor = sensor_error(sensor["type"], "A", Tn)
err_tx = transmitter_error(span)
err_total = total_error(err_sensor, err_tx)

# TERMOPOZO
status, fv, fn = check_thermowell(velocity, diameter, length, elastic_modulus, density)

# PLOTS
plot_transmitter_range(Tn, Tmax, high, "output/range_plot.png")
plot_error(err_sensor, err_tx, err_total, "output/error_plot.png")
plot_thermowell(fn, fv, "output/thermowell_plot.png")

print("RESULTADO FINAL:", status)
print("Sensor seleccionado:", sensor["model"])
print("Error total:", round(err_total, 3), "°C")
