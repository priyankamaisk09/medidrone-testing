# medi.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import time
import random
import numpy as np
from scipy.signal import convolve
from collections import deque
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# ✅ Page setup
st.set_page_config(page_title="MediDrone AI System", layout="wide", page_icon="🚁")

# ------------------------------
# 1️⃣ TRIAGE MODULE
# ------------------------------
def show_triage():
    st.title("AI Triage System & Drone Simulation")

    severity = st.selectbox("Select patient severity:", ["Low", "Medium", "High"])
    priority_map = {"Low": "Normal Priority", "Medium": "Normal Priority", "High": "Launch Immediately"}
    priority = priority_map[severity]

    st.subheader(f"Assigned Priority: {priority}")

    st.subheader("Drone Route Simulation")
    start = [12.9716, 77.5946]
    patient = [12.9750, 77.6050]
    end = [12.9716, 77.5946]

    m = folium.Map(location=start, zoom_start=14)
    folium.Marker(start, tooltip="Drone Base", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(patient, tooltip="Patient", icon=folium.Icon(color="red")).add_to(m)
    folium.Marker(end, tooltip="Return Base", icon=folium.Icon(color="blue")).add_to(m)
    folium.PolyLine([start, patient, end], color="purple", weight=5, opacity=0.8).add_to(m)
    st_folium(m, width=700, height=400)

    st.subheader("Drone Flight Status")
    steps = ["Taking Off", "En Route", "Delivered", "Returning"]
    status_text = st.empty()
    for step in steps:
        status_text.text(f"Drone Status: {step}")
        time.sleep(1.2)
    status_text.text("Drone Status: Completed ✅")


# ------------------------------
# 2️⃣ BIRD AVOIDANCE MODULE
# ------------------------------
def show_bird_avoidance():
    if "control_mode" not in st.session_state:
        st.session_state.control_mode = "AUTO"
    if "logs" not in st.session_state:
        st.session_state.logs = []

    def detect_birds():
        if random.random() < 0.3:
            distance = random.randint(5, 50)
            return {"present": True, "distance": distance}
        return {"present": False}

    def assess_threat(bird):
        if not bird["present"]:
            return "NONE"
        if bird["distance"] > 20:
            return "MONITOR"
        elif bird["distance"] > 10:
            return "AVOID"
        else:
            return "EMERGENCY"

    def plan_maneuver(level):
        options = {
            "AVOID": random.choice(["Climb +2m", "Sidestep Right", "Hover"]),
            "EMERGENCY": random.choice(["Abort Mission", "Return-To-Home", "Descend Rapidly"]),
        }
        return options.get(level, "Continue Mission")

    def log_event(event):
        st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] {event}")

    st.title("🚁 Drone Bird Avoidance Simulation")

    st.sidebar.header("Control Panel")
    if st.sidebar.button("Switch to AUTO Mode"):
        st.session_state.control_mode = "AUTO"
        log_event("Operator switched to AUTO mode")
    if st.sidebar.button("Switch to REMOTE Mode"):
        st.session_state.control_mode = "REMOTE"
        log_event("Operator switched to REMOTE mode")

    play_sound = st.sidebar.checkbox("Enable Sound Deterrent", value=True)
    st.write(f"**Current Control Mode:** {st.session_state.control_mode}")

    if st.button("Run Simulation Step"):
        bird = detect_birds()
        threat = assess_threat(bird)
        if st.session_state.control_mode == "REMOTE":
            log_event("REMOTE control active — operator is flying")
            st.success("REMOTE: Operator in control, no AI action")
        else:
            if threat == "NONE":
                log_event("No bird detected — continuing mission")
                st.info("AUTO: No bird detected. Drone continues mission.")
            elif threat == "MONITOR":
                log_event(f"Bird detected at {bird['distance']}m — monitoring")
                st.warning(f"AUTO: Bird detected at {bird['distance']}m — monitoring.")
            elif threat == "AVOID":
                maneuver = plan_maneuver("AVOID")
                log_event(f"Bird nearby ({bird['distance']}m) — executing {maneuver}")
                st.error(f"AUTO: Avoidance maneuver → {maneuver}")
                if play_sound:
                    st.write("🔊 Sound deterrent activated")
            elif threat == "EMERGENCY":
                maneuver = plan_maneuver("EMERGENCY")
                log_event(f"EMERGENCY! Bird very close ({bird['distance']}m) — {maneuver}")
                st.error(f"AUTO: EMERGENCY action → {maneuver}")
                if play_sound:
                    st.write("🔊 Sound deterrent activated (emergency)")

    st.subheader("📋 Drone Telemetry Log")
    for entry in reversed(st.session_state.logs[-10:]):
        st.write(entry)


# ------------------------------
# 3️⃣ DIAGNOSTICS MODULE
# ------------------------------
def show_diagnostics():
    st.title("🧪 Diagnostic Lab - Point of Care Tests")
    st.write("Upload a sample file or choose a test type to get diagnostic results.")

    uploaded_file = st.file_uploader("📂 Upload a blood sample file", type=["csv", "jpg", "png"])
    test_choice = st.selectbox("Or choose a test type", ["None", "Glucose Test", "Hemoglobin Test", "RBC Count"])

    outcomes = {
        "Glucose Test": ["High Glucose", "Normal Glucose", "Low Glucose"],
        "Hemoglobin Test": ["High Hemoglobin", "Normal Hemoglobin", "Low Hemoglobin"],
        "RBC Count": ["High RBC", "Normal RBC", "Low RBC"]
    }

    def show_result(test_name, result):
        if "High" in result:
            st.warning(f"⚠️ {test_name}: {result}")
        elif "Low" in result:
            st.error(f"❌ {test_name}: {result}")
        else:
            st.success(f"✅ {test_name}: {result}")

    if uploaded_file is not None:
        st.success(f"✅ Sample file received: {uploaded_file.name}")
        with st.spinner("Analyzing sample..."):
            time.sleep(1.5)
            test_name = random.choice(list(outcomes.keys()))
            result = random.choice(outcomes[test_name])
            show_result(test_name, result)
    elif test_choice != "None":
        with st.spinner(f"Running {test_choice}..."):
            time.sleep(1.5)
            result = random.choice(outcomes[test_choice])
            show_result(test_choice, result)
    else:
        st.info("👉 Please upload a file or select a test type to see results.")


# ------------------------------
# 4️⃣ TELECONSULTATION MODULE
# ------------------------------
def show_consultation():
    st.title("Telecommunication Module: Doctor–Patient Interaction")

    st.subheader("Video Consultation")
    st.video("https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4")

    st.subheader("Chat with Doctor")
    user_message = st.text_area("Type your message here:")
    if st.button("Send"):
        if user_message.strip() == "":
            st.warning("Please type a message!")
        else:
            responses = {
                "hello": "Hello! How are you feeling today?",
                "fever": "I see. Please take rest and stay hydrated.",
                "pain": "Can you describe the severity of the pain?",
            }
            reply = "Doctor: " + responses.get(user_message.lower(), "Doctor: Thank you for the info. We'll guide you further.")
            st.text_area("Chat History", value=f"You: {user_message}\n{reply}", height=150)


# ------------------------------
# 5️⃣ VITALS MONITORING MODULE
# ------------------------------
def show_vitals():
    st.title("Vitals Monitoring Simulator — ECG, SpO₂, Body Temperature")

    st_autorefresh(interval=500, key="refresh_vitals")

    if "vitals_init" not in st.session_state:
        st.session_state.vitals_init = True
        st.session_state.fs = 250
        st.session_state.buffer_seconds = 10
        fs = st.session_state.fs
        st.session_state.ecg_buffer = deque([0.0]*(fs*10), maxlen=fs*10)
        st.session_state.time_buffer = deque(np.linspace(-10,0,fs*10), maxlen=fs*10)
        st.session_state.spo2 = 97.0
        st.session_state.temp = 36.6
        st.session_state.last_update = time.time()

    fs = st.session_state.fs
    buffer_seconds = st.session_state.buffer_seconds

    col1, col2 = st.columns([1,2])
    with col1:
        hr = st.slider("Heart Rate (bpm)", 40, 140, 72)
        noise = st.slider("ECG Noise Level", 0.0, 0.05, 0.01, step=0.001)
        spo2_base = st.slider("SpO₂ Baseline (%)", 85, 100, 97)
        temp_base = st.slider("Temperature Baseline (°C)", 35.0, 39.0, 36.6, step=0.1)
        run = st.checkbox("Run Simulation", value=True)

    with col2:
        st.write("### Live ECG Signal")
        ecg_placeholder = st.empty()
        colm1, colm2, colm3 = st.columns(3)
        spo2_metric, temp_metric, hr_metric = colm1.empty(), colm2.empty(), colm3.empty()

    def make_beat_template(fs=250):
        t = np.linspace(-0.5, 0.8, int(1.3 * fs), endpoint=False)
        beat = np.zeros_like(t)
        def gauss(center, width, amp):
            return amp * np.exp(-0.5 * ((t - center)/width)**2)
        beat += gauss(-0.18, 0.03, 0.08)
        beat += gauss(-0.02, 0.005, -0.05)
        beat += gauss(0.0, 0.006, 1.0)
        beat += gauss(0.03, 0.006, -0.12)
        beat += gauss(0.32, 0.05, 0.25)
        beat = beat / np.max(np.abs(beat))
        return beat

    def generate_ecg(hr_bpm, fs, noise_std):
        beat = make_beat_template(fs)
        rr = 60.0/hr_bpm
        samples = int(rr*fs)
        impulses = np.zeros(samples)
        impulses[0] = 1
        ecg = convolve(impulses, beat, mode='same')
        baseline = 0.02*np.sin(2*np.pi*0.3*np.arange(samples)/fs)
        ecg += baseline + np.random.normal(0, noise_std, size=samples)
        return ecg

    if run:
        ecg_chunk = generate_ecg(hr, fs, noise)
        for s in ecg_chunk:
            st.session_state.ecg_buffer.append(s)
        t_vals = np.linspace(-buffer_seconds, 0, len(st.session_state.ecg_buffer))
        st.session_state.time_buffer = deque(t_vals, maxlen=len(t_vals))

        if time.time() - st.session_state.last_update > 1:
            st.session_state.last_update = time.time()
            st.session_state.spo2 += (spo2_base - st.session_state.spo2) * 0.05 + np.random.normal(0, 0.1)
            st.session_state.temp += (temp_base - st.session_state.temp) * 0.05 + np.random.normal(0, 0.01)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=np.array(st.session_state.time_buffer),
        y=np.array(st.session_state.ecg_buffer),
        mode='lines'
    ))
    fig.update_layout(title=f"ECG (last {buffer_seconds}s)", height=300,
                      xaxis=dict(range=[-buffer_seconds, 0]),
                      xaxis_title="Time (s)", yaxis_title="Amplitude")
    ecg_placeholder.plotly_chart(fig, use_container_width=True)

    spo2_metric.metric("SpO₂ (%)", f"{st.session_state.spo2:.1f}")
    temp_metric.metric("Temp (°C)", f"{st.session_state.temp:.2f}")
    hr_metric.metric("HR (bpm)", f"{hr}")


# ------------------------------
# 6️⃣ MEDICINE DISPENSER MODULE
# ------------------------------
def show_medicine_dispenser():
    st.title("💊 Smart Medicine Dispenser")
    st.write("Click a medicine button to dispense:")

    medicines = ["Paracetamol", "Amoxicillin", "Ibuprofen", "Cetirizine", "Metformin"]
    for med in medicines:
        if st.button(med):
            with st.spinner(f"Dispensing {med}..."):
                time.sleep(2)
            st.success(f"✅ Dispensing {med} 💊")
            st.balloons()


# ------------------------------
# 🧭 MAIN SIDEBAR NAVIGATION
# ------------------------------
st.sidebar.title("🚀 MediDrone AI System")

option = st.sidebar.selectbox(
    "Select Module",
    [
        "Triage",
        "Bird Avoidance",
        "Diagnostics",
        "Teleconsultation",
        "Vitals Monitoring",
        "Medicine Dispenser"
    ]
)

if option == "Triage":
    show_triage()
elif option == "Bird Avoidance":
    show_bird_avoidance()
elif option == "Diagnostics":
    show_diagnostics()
elif option == "Teleconsultation":
    show_consultation()
elif option == "Vitals Monitoring":
    show_vitals()
elif option == "Medicine Dispenser":
    show_medicine_dispenser()
