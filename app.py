# app.py
# Mini test app to run only Yuva's diagnostics module

import streamlit as st
from diagnostics import show_diagnostics

st.set_page_config(page_title="MediDrone — Diagnostics Test", layout="centered")

st.sidebar.title("MediDrone Prototype (Test Mode)")
page = st.sidebar.radio("Choose Module", ["Diagnostics"])

if page == "Diagnostics":
    show_diagnostics()
