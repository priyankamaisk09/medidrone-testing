# triage.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import time

# ------------------------------
# Function: AI Triage Simulation
# ------------------------------
def show_triage():
    st.title("AI Triage System & Drone Simulation")

    # Severity Selection
    severity = st.selectbox("Select patient severity:", ["Low", "Medium", "High"])

    # Assign priority based on severity
    priority_map = {"Low": "Normal Priority", "Medium": "Normal Priority", "High": "Launch Immediately"}
    priority = priority_map[severity]

    st.subheader(f"Assigned Priority: {priority}")

    # Map simulation
    st.subheader("Drone Route Simulation")
    # Coordinates: start, patient, base (example locations)
    start = [12.9716, 77.5946]      # Drone base
    patient = [12.9750, 77.6050]    # Patient location
    end = [12.9716, 77.5946]        # Return to base

    # Create folium map
    m = folium.Map(location=start, zoom_start=14)
    folium.Marker(start, tooltip="Drone Base", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(patient, tooltip="Patient", icon=folium.Icon(color="red")).add_to(m)
    folium.Marker(end, tooltip="Return Base", icon=folium.Icon(color="blue")).add_to(m)

    # Draw route
    folium.PolyLine([start, patient, end], color="purple", weight=5, opacity=0.8).add_to(m)

    st_folium(m, width=700, height=400)

    # Fake flight steps animation
    st.subheader("Drone Flight Status")
    steps = ["Taking Off", "En Route", "Delivered", "Returning"]
    status_text = st.empty()

    for step in steps:
        status_text.text(f"Drone Status: {step}")
        time.sleep(1.5)
    status_text.text("Drone Status: Completed ✅")


# --------------------------------------
# Function: Doctor–Patient Consultation
# --------------------------------------
def show_consultation():
    st.title("Telecommunication Module: Doctor–Patient Interaction")

    # Video Consultation Simulation
    st.subheader("Video Consultation")
    sample_video = "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4"
    st.video(sample_video)

    # Chat Simulation
    st.subheader("Chat with Doctor")
    user_message = st.text_area("Type your message here:")
    if st.button("Send"):
        if user_message.strip() == "":
            st.warning("Please type a message!")
        else:
            # Fake doctor response
            responses = {
                "hello": "Hello! How are you feeling today?",
                "fever": "I see. Please take rest and stay hydrated.",
                "pain": "Can you describe the severity of the pain?",
            }
            user_lower = user_message.lower()
            reply = "Doctor: " + responses.get(user_lower, "Doctor: Thank you for the info. We'll guide you further.")
            st.text_area("Chat History", value=f"You: {user_message}\n{reply}", height=150)


# --------------------------------------
# Optional: Run standalone in Streamlit
# --------------------------------------
if __name__ == "__main__":
    st.sidebar.title("MediDrone AI")
    option = st.sidebar.selectbox("Select Module", ["Triage Module", "Telecommunication Module"])
    if option == "Triage Module":
        show_triage()
    else:
        show_consultation()
