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

# Diámetros internos reales en METROS
PIPE_DIAMETERS = {
    3: {
        "SCH 10": 0.12,
        "SCH 40/STD": 0.216,
        "SCH XS/80": 0.3,
        "SCH 160": 0.438,
        "SCH XXS": 0.6,
    },
    4: {
        "SCH 10": 0.12,
        "SCH 40/STD": 0.237,
        "SCH XS/80": 0.337,
        "SCH 120": 0.438,
        "SCH 160": 0.531,
        "SCH XXS": 0.674,
    },
    6: {
        "SCH 10": 0.134,
        "SCH 40/STD": 0.28,
        "SCH XS/80": 0.432,
        "SCH 120": 0.562,
        "SCH 160": 0.719,
        "SCH XXS": 0.864,
    },
    8: {
        "SCH 10": 0.148,
        "SCH 20": 0.250,
        "SCH 40/STD": 0.322,
        "SCH 60": 0.406,
        "SCH XS/80": 0.500,
        "SCH 120": 0.719,
        "SCH XXS": 0.875,
        "SCH 160": 0.906,
    },
    10: {
        "SCH 10": 0.165,
        "SCH 20": 0.250,
        "SCH 40/STD": 0.365,
        "SCH 60/XS": 0.500,
        "SCH 80": 0.594,
        "SCH 120": 0.844,
        "SCH XXS/140": 1.000,
        "SCH 160": 1.125,
    },
    12: {
        "SCH 10": 0.180,
        "SCH 20": 0.250,
        "SCH STD": 0.375,
        "SCH 40": 0.406,
        "SCH XS": 0.500,
        "SCH 60": 0.562,
        "SCH 80": 0.688,
        "SCH XXS/120": 1.000,
        "SCH 160": 1.312,
    },
    14: {
        "SCH 10": 0.250,
        "SCH 20": 0.312,
        "SCH STD/30": 0.375,
        "SCH 40": 0.438,
        "SCH XS": 0.500,
        "SCH 60": 0.594,
        "SCH 80": 0.750,
        "SCH 120": 1.094,
        "SCH 160": 1.406,
    },
    16: {
        "SCH 10": 0.250,
        "SCH 20": 0.312,
        "SCH STD/30": 0.375,
        "SCH XS/40": 0.500,
        "SCH 60": 0.656,
        "SCH 80": 0.844,
        "SCH 120": 1.219,
        "SCH 160": 1.594,
    },
    20: {
        "SCH 10": 0.250,
        "SCH STD/20": 0.375,
        "SCH XS/30": 0.500,
        "SCH 40": 0.594,
        "SCH 60": 0.812,
        "SCH 80": 1.031,
        "SCH 120": 1.500,
        "SCH 160": 1.969,
    },
    24: {
        "SCH 10": 0.250,
        "SCH STD/20": 0.375,
        "SCH XS": 0.500,
        "SCH 40": 0.688,
        "SCH 60": 0.969,
        "SCH 80": 1.219,
        "SCH 120": 1.812,
        "SCH 160": 2.344,
    },
    30: {
        "SCH 10": 0.312,
        "SCH STD": 0.375,
        "SCH XS/20": 0.500,
    },
    36: {
        "SCH 10": 0.312,
        "SCH STD": 0.375,
        "SCH XS/20": 0.500,
        "SCH 40": 0.750,
    },
    42: {
        "SCH STD": 0.375,
        "SCH XS": 0.500,
    },
}
PIPE_OUTSIDE_DIAMETER = {
    3: 3.500,   # pulgadas
    4: 4.500,   # pulgadas
    6: 6.625,   # pulgadas
    8: 8.625,   # pulgadas
    10: 10.75,   # pulgadas
    12: 12.75,   # pulgadas
    14: 14.00,   # pulgadas
    16: 16.00,   # pulgadas
    20: 20.00,   # pulgadas
    24: 24.00,   # pulgadas
    30: 30.00,   # pulgadas
    36: 36.00,   # pulgadas
    42: 42.00,   # pulgadas
}

st.sidebar.header("Inputs de Tubería")
pipe_diameter = st.sidebar.selectbox("Diámetro nominal (NPS)", options=list(PIPE_DIAMETERS.keys()))
pipe_od = PIPE_OUTSIDE_DIAMETER[pipe_diameter]
pipe_sch = st.sidebar.selectbox("Schedule", options=list(PIPE_DIAMETERS[pipe_diameter].keys()))
wall_thickness_in = PIPE_DIAMETERS[pipe_diameter][pipe_sch]
#pipe_diameter = st.sidebar.number_input("Diámetro de tubería (inches)", value=4.0)
#pipe_sch = st.sidebar.selectbox("Schedule de tubería", ["SCH 10", "SCH 40", "SCH 80"])
hod = st.sidebar.number_input("HOD (in)", value=6.0)

st.sidebar.header("Termopozo")
mounting = st.sidebar.selectbox("Estilo Montaje", ["Welded", "Threaded", "Flanged"])
connection = st.sidebar.selectbox("Diametro Conexión", ["1/4 in", "1/2 in", "3/4 in", "1 in", "1-1/2 in", "2 in"])
connection1 = st.sidebar.selectbox("Tipo Conexión", ["NPT", "RF 150#", "RF 300#", "RF 600#", "RTJ 900/1500#", "RTJ 2500#"])
diameter = st.sidebar.number_input("Diámetro termopozo (mm)", value=18.0)
#length = st.sidebar.number_input("Longitud inserción (mm)", value=180.0)
elastic_modulus = st.sidebar.number_input("Módulo elasticidad (GPa)", value=193.0, help = "Valores típicos: SS316 ≈ 193 GPa, Inconel625 ≈ 207 GPa")
density = st.sidebar.number_input("Densidad fluido (kg/m³)", value=1000.0)

# =====================
# BOTÓN
# =====================
if st.sidebar.button("Calcular temperatura"):
    input_unit = unit
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
    flow_m3_s = flow * bbl_to_m3 / (24*3600)  # BPD → m³/s

    # Diámetro interno aproximado según Schedule
    internal_diameter_in = pipe_od - 2 * wall_thickness_in
    #internal_diameter_in = sch_dict.get(pipe_sch, 0.0895)
    diameter_m = internal_diameter_in * 0.0254  # pulgadas → metros

    velocity = flow_m3_s / (3.1416 * (diameter_m/2)**2)
    velocity_ft_s = velocity*3.2804
    insertion_length = 2/3 * internal_diameter_in  # regla práctica para longitud de inserción
    length_mm = (insertion_length + hod) * 25.4

    # Verificación termopozo (usando función ya existente)
    status, fv, fn = check_thermowell(
        velocity, diameter_m*1000, insertion_length*25.4, elastic_modulus, density
    )
    
    # mostrar unidades seleccionadas
    
    if input_unit == "°F":
        Tn_out = Tn * 9/5 + 32
        Tmax_out = Tmax * 9/5 + 32
        high_out = high * 9/5 + 32
        err_sensor_out = err_sensor * 9/5
        err_tx_out = err_tx * 9/5
        err_total_out = err_total * 9/5   # error también escala
        temp_unit = "°F"
    else:
        Tn_out = Tn
        Tmax_out = Tmax
        high_out = high
        err_sensor_out = err_sensor
        err_tx_out = err_tx
        err_total_out = err_total
        temp_unit = "°C"    
        
    os.makedirs("output", exist_ok=True)

    plot_transmitter_range(Tn_out, Tmax_out, high_out, "output/range_plot.png")
    plot_error(err_sensor_out, err_tx_out, err_total_out, "output/error_plot.png")
    plot_thermowell(fn, fv, "output/thermowell_plot.png")

    # =====================
    # RESULTADOS
    # =====================
    st.subheader("📊 Resultados")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rango transmisor", f"0 – {high_out:.1f} {temp_unit}")
        st.metric("Sensor seleccionado", sensor["model"])
        st.metric("Error total", f"{err_total_out:.3f} {temp_unit}")
        st.metric("Velocidad del fluido", f"{velocity_ft_s:.2f} ft/s")
        st.metric("Longitud inserción termopozo", f"{length_mm:.2f} mm")
        
        if "NO CUMPLE" in status:
            st.error(status)
        else:
            st.success(status)

    with col2:
        st.image("output/range_plot.png", caption="Rango del transmisor")
        st.image("output/error_plot.png", caption="Error del sistema")
        st.image("output/thermowell_plot.png", caption="Verificación ASME PTC 19.3")
