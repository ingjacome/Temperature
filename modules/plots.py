import matplotlib.pyplot as plt

def plot_transmitter_range(tn, tmax, span, filename):
    plt.figure()
    plt.bar(["Tn", "Tmax"], [tn, tmax])
    plt.axhline(span, linestyle="--", label="Límite transmisor")
    plt.ylabel("Temperatura °C")
    plt.legend()
    plt.savefig(filename)
    plt.close()


def plot_error(err_sensor, err_tx, err_total, filename):
    plt.figure()
    plt.bar(["Sensor", "Transmisor", "Total"],
            [err_sensor, err_tx, err_total])
    plt.ylabel("Error °C")
    plt.savefig(filename)
    plt.close()


def plot_thermowell(fn, fv, filename):
    plt.figure()
    plt.bar(["fn", "2.2 fv"], [fn, 2.2 * fv])
    plt.ylabel("Frecuencia (Hz)")
    plt.savefig(filename)
    plt.close()
