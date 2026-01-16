import streamlit as st
from modules.temperature_calc import *
from modules.thermowell import *
from modules.sensors_db import *
from modules.plots import *
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
#velocity = st.sidebar.number_input("Velocidad fluido (m/s)", value=15.0)
flow = st.sidebar.number_input("Flujo (BPD)", value=1000.0)

st.sidebar.header("Inputs de Tubería")
pipe_diameter = st.sidebar.number_input("Diámetro de tubería (inches)", value=4.0)
pipe_sch = st.sidebar.selectbox("Schedule de tubería", ["SCH 10", "SCH 40", "SCH 80"])
hod = st.sidebar.number_input("HOD (m)", value=6.0)

st.sidebar.header("Termopozo")
diameter = st.sidebar.number_input("Diámetro termopozo (mm)", value=18.0)
length = st.sidebar.number_input("Longitud inserción (mm)", value=180.0)
elastic_modulus = st.sidebar.number_input("Módulo elasticidad (GPa)", value=193.0, help = "Valores típicos: SS316 ≈ 193 GPa, Inconel625 ≈ 207 GPa")
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
    # Calcular velocidad desde flujo y diámetro de tubería
    bbl_to_m3 = 0.158987
    flow_m3_s = flow_bpd * bbl_to_m3 / (24*3600)  # BPD → m³/s

    # Diámetro interno aproximado según Schedule
    sch_dict = {"SCH 10": 0.065, "SCH 40": 0.067, "SCH 80": 0.065}  # ejemplo 4" in
    internal_diameter_in = sch_dict.get(pipe_sch, 0.065)
    diameter_m = internal_diameter_in * 0.0254  # pulgadas → metros

    velocity = flow_m3_s / (3.1416 * (diameter_m/2)**2)
    insertion_length = internal_diameter_in * 2/3 + hod  # regla práctica para longitud de inserción

    # Verificación termopozo (usando función ya existente)
    status, fv, fn = check_thermowell(
        velocity, diameter_m*1000, insertion_length*1000, elastic_modulus, density
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
        st.metric("Velocidad del fluido", f"{velocity_calc:.2f} m/s")
        st.metric("Longitud inserción termopozo", f"{insertion_length:.2f} m")
        
        if "NO CUMPLE" in status:
            st.error(status)
        else:
            st.success(status)

    with col2:
        st.image("output/range_plot.png", caption="Rango del transmisor")
        st.image("output/error_plot.png", caption="Error del sistema")
        st.image("output/thermowell_plot.png", caption="Verificación ASME PTC 19.3")
