import streamlit as st
import random
import time

# --- Initialize session state ---
if "control_mode" not in st.session_state:
    st.session_state.control_mode = "AUTO"
if "logs" not in st.session_state:
    st.session_state.logs = []

# --- Helper functions ---
def detect_birds():
    """Simulate AI bird detection with random chance"""
    if random.random() < 0.3:  # 30% chance of bird appearing
        distance = random.randint(5, 50)  # meters
        return {"present": True, "distance": distance}
    return {"present": False}

def assess_threat(bird):
    """Decide threat level based on distance"""
    if not bird["present"]:
        return "NONE"
    if bird["distance"] > 20:
        return "MONITOR"
    elif bird["distance"] > 10:
        return "AVOID"
    else:
        return "EMERGENCY"

def plan_maneuver(level):
    """Pick avoidance maneuver"""
    options = {
        "AVOID": random.choice(["Climb +2m", "Sidestep Right", "Hover"]),
        "EMERGENCY": random.choice(["Abort Mission", "Return-To-Home", "Descend Rapidly"]),
    }
    return options.get(level, "Continue Mission")

def log_event(event):
    st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] {event}")

# --- Streamlit UI ---
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

# --- Simulation step ---
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
            log_event(f"Bird detected at safe distance ({bird['distance']}m). Monitoring.")
            st.warning(f"AUTO: Bird detected at {bird['distance']}m — monitoring.")
        elif threat == "AVOID":
            maneuver = plan_maneuver("AVOID")
            log_event(f"Bird nearby ({bird['distance']}m) — executing avoidance: {maneuver}")
            st.error(f"AUTO: Avoidance maneuver triggered → {maneuver}")
            if play_sound:
                st.write("🔊 Sound deterrent activated")
        elif threat == "EMERGENCY":
            maneuver = plan_maneuver("EMERGENCY")
            log_event(f"EMERGENCY! Bird very close ({bird['distance']}m) — {maneuver}")
            st.error(f"AUTO: EMERGENCY action → {maneuver}")
            if play_sound:
                st.write("🔊 Sound deterrent activated (emergency)")

# --- Telemetry log ---
st.subheader("📋 Drone Telemetry Log")
for entry in reversed(st.session_state.logs[-10:]):  # show last 10 logs
    st.write(entry)
