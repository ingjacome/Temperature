def vortex_frequency(velocity, diameter_mm):
    st = 0.2
    d = diameter_mm / 1000
    return st * velocity / d


def natural_frequency(diameter_mm, length_mm, elastic_modulus_gpa, density):
    d = diameter_mm / 1000
    l = length_mm / 1000
    e = elastic_modulus_gpa * 1e9
    return 0.56 * (d / l**2) * ((e / density) ** 0.5)


def check_thermowell(velocity, diameter_mm, length_mm, elastic_modulus_gpa, density):
    fv = vortex_frequency(velocity, diameter_mm)
    fn = natural_frequency(diameter_mm, length_mm, elastic_modulus_gpa, density)

    if fn >= 2.2 * fv:
        return "APROBADO", fv, fn
    else:
        return "NO CUMPLE – Resonancia", fv, fn
