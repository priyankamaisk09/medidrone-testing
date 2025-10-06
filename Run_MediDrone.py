import streamlit as st
from streamlit_folium import st_folium
import folium
import random
import time
import plotly.express as px

# Page setup
st.set_page_config(page_title="MediDrone Dashboard", layout="wide")
st.title("🩺 MediDrone Interactive Dashboard")

# Sidebar module selection
module = st.sidebar.selectbox("Select Module", [
    "AI Triage System & Drone Simulation",
    "Drone Bird Avoidance Simulation",
    "Teleconsultation",
    "Vitals Monitoring Simulator",
    "Smart Medicine Dispenser"
])

# ---------------- AI TRIAGE & DRONE SIMULATION ----------------
if module == "AI Triage System & Drone Simulation":
    st.subheader("AI Triage System & Drone Simulation")
    
    # Patient Severity Selection
    severity = st.selectbox("Select patient severity:", ["Low", "Medium", "High"])
    priority_map = {"Low":"Normal Priority", "Medium":"Moderate Priority", "High":"High Priority"}
    assigned_priority = priority_map[severity]
    st.write(f"**Assigned Priority:** {assigned_priority}")
    
    # Drone Route Simulation
    st.markdown("**Drone Route Simulation:**")
    m = folium.Map(location=[12.9716, 77.5946], zoom_start=13)
    folium.Marker([12.9716, 77.5946], popup="Start Point").add_to(m)
    folium.Marker([12.9816, 77.6046], popup="Destination").add_to(m)
    folium.PolyLine([[12.9716, 77.5946], [12.9816, 77.6046]], color="blue", weight=3).add_to(m)
    st_folium(m, width=700, height=450)
    
    # Drone Flight Status Simulation
    st.markdown("**Drone Flight Status:**")
    status = st.empty()
    drone_states = ["Taking off", "En route", "Delivered", "Returning", "Completed ✅"]
    for s in drone_states:
        status.info(f"Drone Status: {s}")
        time.sleep(0.5)

# ---------------- BIRD AVOIDANCE ----------------
elif module == "Drone Bird Avoidance Simulation":
    st.subheader("🚁 Drone Bird Avoidance Simulation")
    
    # Drone Telemetry Log
    st.markdown("📋 Drone Telemetry Log")
    for i in range(5):
        st.write(f"Telemetry Entry {i+1}: Altitude {random.randint(50,150)}m, Speed {random.randint(20,50)} km/h")
    
    # Control Panel
    st.sidebar.markdown("### Control Panel")
    mode = st.sidebar.radio("Mode:", ["AUTO", "REMOTE"])
    st.sidebar.checkbox("Ensure sound deterrent")

# ---------------- DIAGNOSTICS ---------------------

# app.py
# Mini test app to run only Yuva's diagnostics module

import streamlit as st
from diagnostics import show_diagnostics

st.set_page_config(page_title="MediDrone — Diagnostics Test", layout="centered")

st.sidebar.title("MediDrone Prototype (Test Mode)")
page = st.sidebar.radio("Choose Module", ["Diagnostics"])

if page == "Diagnostics":
    show_diagnostics()

# ---------------- TELECONSULTATION ----------------
elif module == "Teleconsultation":
    st.subheader("Telecommunication Module: Doctor–Patient Interaction")

    st.markdown("**Video Consultation Placeholder**")
    st.button("Start Video Call")

    # Live Chat simulation
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input message
    msg = st.text_input("Type your message here:")

    if st.button("Send Message"):
        if msg.strip() != "":
            # Add patient message
            st.session_state.chat_history.append(f"Patient: {msg}")
            
            # Simulate doctor reply
            reply = f"Doctor: Prescription/Advice for '{msg}'"
            st.session_state.chat_history.append(reply)

    # Display chat history
    st.markdown("### Chat History")
    for chat in st.session_state.chat_history:
        st.write(chat)

# ---------------- VITALS MONITORING ----------------
elif module == "Vitals Monitoring Simulator":
    st.subheader("Vitals Monitoring Simulator — ECG, SpO₂, Body Temperature")
    
    # Sliders for vitals
    hr = st.slider("Heart Rate (bpm)", 40, 140, 78)
    ecg_noise = st.slider("ECG Noise Level", 0.0, 0.05, 0.01)
    spo2 = st.slider("SpO₂ Baseline (%)", 85, 100, 98)
    temp = st.slider("Temperature Baseline (°C)", 35.0, 40.0, 36.7)  # FIXED
    
    # Display table
    st.table({
        "Heart Rate (bpm)": [hr],
        "ECG Noise Level": [ecg_noise],
        "SpO₂ (%)": [spo2],
        "Temperature (°C)": [temp]
    })
    
    # Live signals simulation
    st.markdown("**Live Signals:**")
    fig = px.line(x=list(range(10)), y=[random.randint(60,100) for _ in range(10)], labels={"x":"Time", "y":"ECG"})
    st.plotly_chart(fig, use_container_width=True)

# ---------------- MEDICINE DISPENSER ----------------
elif module == "Smart Medicine Dispenser":
    st.subheader("💊 Smart Medicine Dispenser")
    medicines = ["Paracetamol", "Amoxicillin", "Ibuprofen", "Cetirizine", "Metformin"]
    
    for med in medicines:
        if st.button(f"Dispense {med}"):
            st.success(f"{med} dispensed successfully!")
            st.balloons()
