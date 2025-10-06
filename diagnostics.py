# diagnostics.py
# Yuva — Diagnostics Module (Point-of-Care Tests)

import streamlit as st
import random
import time

def show_diagnostics():
    st.title("🧪 Diagnostic Lab - Point of Care Tests")
    st.write("Upload a sample file or choose a test type to get diagnostic results.")

    # --- Input Options ---
    uploaded_file = st.file_uploader("📂 Upload a blood sample file (CSV/Image)", type=["csv", "jpg", "png"])
    test_choice = st.selectbox("Or choose a test type", ["None", "Glucose Test", "Hemoglobin Test", "RBC Count"])

    # --- Mock Result Generator ---
    outcomes = {
        "Glucose Test": ["High Glucose", "Normal Glucose", "Low Glucose"],
        "Hemoglobin Test": ["High Hemoglobin", "Normal Hemoglobin", "Low Hemoglobin"],
        "RBC Count": ["High RBC", "Normal RBC", "Low RBC"]
    }

    # --- Helper function to display results with color ---
    def show_result(test_name, result):
        if "High" in result:
            st.warning(f"⚠️ {test_name}: {result}")
        elif "Low" in result:
            st.error(f"❌ {test_name}: {result}")
        elif "Normal" in result:
            st.success(f"✅ {test_name}: {result}")
        else:
            st.info(f"ℹ️ {test_name}: {result}")

    # --- Display Results ---
    if uploaded_file is not None:
        st.success(f"✅ Sample file received: {uploaded_file.name}")
        with st.spinner("Analyzing sample..."):
            time.sleep(1.5)  # simulate processing delay
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
