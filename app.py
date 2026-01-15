import streamlit as st
from temperature_calc import *
from thermowell import *
from sensors_db import *
from plots import *
import os

st.set_page_config(page_title="Temperature EPC Tool", layout="wide")

st.title("🌡️ Temperature Calculation – EPC Engineering")

# =====================
# INPUTS
# =====================
st.sidebar.header("Inputs de Proceso")

Tn = st.sidebar.number_input("Temperatura normal", value=120.0)
Tmax = st.sidebar.number_input("Temperatura máxima", value=150.0)
unit = st.sidebar.selectbox("Unidad", ["°C", "°F"])

velocity = st.sidebar.number_input("Velocidad fluido (m/s)", value=15.0)

st.sidebar.header("Termopozo")
diameter = st.sidebar.number_input("Diámetro termopozo (mm)", value=18.0)
length = st.sidebar.number_input("Longitud inserción (mm)", value=180.0)
elastic_modulus = st.sidebar.number_input("Módulo elasticidad (GPa)", value=193.0)
density = st.sidebar.number_input("Densidad fluido (kg/m³)", value=1000.0)

# =====================
# BOTÓN
# =====================
if st.sidebar.button("Calcular temperatura"):

    if unit == "°F":
        Tn = f_to_c(Tn)
        Tmax = f_to_c(Tmax)

    # -----------------
    # TRANSMISOR
    # -----------------
    low, high = select_transmitter_range(Tmax)
    span = high - low

    # -----------------
    # SENSOR
    # -----------------
    sensor = select_sensor(high)
    err_sensor = sensor_error(sensor["type"], "A", Tn)
    err_tx = transmitter_error(span)
    err_total = total_error(err_sensor, err_tx)

    # -----------------
    # TERMOPOZO
    # -----------------
    status, fv, fn = check_thermowell(
        velocity, diameter, length, elastic_modulus, density
    )

    os.makedirs("output", exist_ok=True)

    plot_transmitter_range(Tn, Tmax, high, "output/range_plot.png")
    plot_error(err_sensor, err_tx, err_total, "output/error_plot.png")
    plot_thermowell(fn, fv, "output/thermowell_plot.png")

    # =====================
    # RESULTADOS
    # =====================
    st.subheader("📊 Resultados")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rango transmisor", f"0 – {high} °C")
        st.metric("Sensor seleccionado", sensor["model"])
        st.metric("Error total", f"{err_total:.3f} °C")

        if "NO CUMPLE" in status:
            st.error(status)
        else:
            st.success(status)

    with col2:
        st.image("output/range_plot.png", caption="Rango del transmisor")
        st.image("output/error_plot.png", caption="Error del sistema")
        st.image("output/thermowell_plot.png", caption="Verificación ASME PTC 19.3")