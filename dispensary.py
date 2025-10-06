import streamlit as st
import time

# Set page title and icon
st.set_page_config(page_title="Medicine Dispenser", page_icon="💊")

st.title("💊 Smart Medicine Dispenser")
st.write("Click a medicine button to dispense:")

# List of medicines
medicines = ["Paracetamol", "Amoxicillin", "Ibuprofen", "Cetirizine", "Metformin"]

# Loop through medicines and create buttons
for med in medicines:
    if st.button(med):
        # Show spinner for 2 seconds to simulate dispensing
        with st.spinner(f"Dispensing {med}..."):
            time.sleep(2)
        # Show success message with emoji
        st.success(f"✅ Dispensing {med} 💊")
        # Fun animation
        st.balloons()
