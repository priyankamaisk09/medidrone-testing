# vitals_streamlit.py
"""
Streamlit-friendly Biosensor Vitals Simulator
- ECG waveform (synthetic)
- SpO₂ values (random)
- Body temperature values (random)
- Real-time plotting without blocking loops
"""

import streamlit as st
import numpy as np
from scipy.signal import convolve
import time
from collections import deque
import math
import random
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# -------------------------
# Helper functions
# -------------------------
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
    return beat, t

def generate_ecg_chunk(hr_bpm, duration_s, fs, beat_template, noise_std=0.01, beat_jitter=0.02):
    n_samples = int(duration_s * fs)
    t = np.arange(n_samples)/fs
    avg_rr = 60.0/hr_bpm
    window_len = duration_s + 2.0
    Nbig = int(window_len*fs)
    impulses = np.zeros(Nbig)
    offset = random.uniform(0, avg_rr)
    beat_time = -1.0 + offset
    while beat_time < window_len:
        idx = int(round((beat_time + 1.0) * fs))
        if 0 <= idx < Nbig:
            impulses[idx] = 1.0
        beat_time += avg_rr*(1.0 + random.uniform(-beat_jitter, beat_jitter))
    ecg_big = convolve(impulses, beat_template, mode='same')
    start_idx = int(1.0*fs)
    ecg = ecg_big[start_idx:start_idx + n_samples]
    baseline = 0.02*np.sin(2*np.pi*0.2*t + random.uniform(0,2*math.pi))
    ecg = ecg + baseline + np.random.normal(0, noise_std, size=ecg.shape)
    return t, ecg

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Vitals Monitoring Simulator", layout="wide")
st.title("Vitals Monitoring Simulator — ECG, SpO₂, Body Temp")

# Auto-refresh every 200 ms
st_autorefresh(interval=200, key="vitals_refresh")

# -------------------------
# Controls
# -------------------------
col_ctrl, col_display = st.columns([1,3])
with col_ctrl:
    st.header("Controls")
    fs = st.slider("Sampling rate (Hz)", 125, 1000, 250, step=25)
    buffer_seconds = st.slider("ECG buffer (seconds shown)", 5, 30, 10)
    hr = st.slider("Heart rate (bpm)", 40, 140, 72)
    noise_level = st.slider("ECG noise level (std dev)", 0.0, 0.05, 0.01, step=0.001)
    beat_jitter = st.slider("Beat interval jitter (±fraction)", 0.0, 0.1, 0.02, step=0.005)
    spo2_baseline = st.slider("SpO₂ baseline (%)", 85, 100, 97)
    temp_baseline = st.slider("Body temp baseline (°C)", 35.0, 39.0, 36.6, step=0.1)
    run_sim = st.checkbox("Run simulation", value=True)

with col_display:
    st.header("Live signals")
    ecg_placeholder = st.empty()
    spo2_placeholder = st.empty()
    temp_placeholder = st.empty()
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    spo2_metric = metric_col1.empty()
    temp_metric = metric_col2.empty()
    hr_metric = metric_col3.empty()

# -------------------------
# Initialize buffers
# -------------------------
if "ecg_buffer" not in st.session_state:
    max_len = int(buffer_seconds*fs)
    st.session_state.ecg_buffer = deque([0.0]*max_len, maxlen=max_len)
    st.session_state.time_buffer = deque(np.linspace(-buffer_seconds,0,max_len,endpoint=False), maxlen=max_len)
    st.session_state.spo2_buffer = deque([spo2_baseline]*60, maxlen=60)
    st.session_state.temp_buffer = deque([temp_baseline]*60, maxlen=60)
    st.session_state.last_update = time.time()

beat_template, _ = make_beat_template(fs=fs)
expected_len = int(buffer_seconds*fs)
if st.session_state.ecg_buffer.maxlen != expected_len:
    st.session_state.ecg_buffer = deque([0.0]*expected_len, maxlen=expected_len)
    st.session_state.time_buffer = deque(np.linspace(-buffer_seconds,0,expected_len,endpoint=False), maxlen=expected_len)

# -------------------------
# Update buffers (one chunk per refresh)
# -------------------------
if run_sim:
    chunk_duration = 0.15
    _, ecg_chunk = generate_ecg_chunk(hr, chunk_duration, fs, beat_template, noise_level, beat_jitter)
    for s in ecg_chunk:
        st.session_state.ecg_buffer.append(s)
    last_time = st.session_state.time_buffer[-1] if st.session_state.time_buffer else 0.0
    for _ in ecg_chunk:
        last_time += 1.0/fs
        st.session_state.time_buffer.append(last_time)
    times = np.array(st.session_state.time_buffer)
    times = times - times[-1]
    st.session_state.time_buffer = deque(times, maxlen=st.session_state.time_buffer.maxlen)

    now = time.time()
    if now - st.session_state.last_update >= 1.0:
        st.session_state.last_update = now
        prev_spo2 = st.session_state.spo2_buffer[-1]
        new_spo2 = prev_spo2 + np.random.normal(0,0.15)
        new_spo2 += (spo2_baseline - new_spo2)*0.02
        new_spo2 = float(np.clip(new_spo2,80,100))
        st.session_state.spo2_buffer.append(new_spo2)

        prev_temp = st.session_state.temp_buffer[-1]
        new_temp = prev_temp + np.random.normal(0,0.01)
        new_temp += (temp_baseline - new_temp)*0.01
        new_temp = float(np.clip(new_temp,35.0,39.0))
        st.session_state.temp_buffer.append(new_temp)

# -------------------------
# Plotting
# -------------------------
# ECG
fig_ecg = go.Figure()
fig_ecg.add_trace(go.Scatter(x=np.array(st.session_state.time_buffer), y=np.array(st.session_state.ecg_buffer), mode='lines'))
fig_ecg.update_layout(title=f"ECG (last {buffer_seconds}s)", xaxis_title="Time (s)", yaxis_title="Amplitude", xaxis=dict(range=[-buffer_seconds,0]), height=300)
ecg_placeholder.plotly_chart(fig_ecg, use_container_width=True)

# SpO2
spo2_arr = np.array(st.session_state.spo2_buffer)
spo2_times = np.linspace(-len(spo2_arr)+1, 0, len(spo2_arr))
fig_spo2 = go.Figure()
fig_spo2.add_trace(go.Scatter(x=spo2_times, y=spo2_arr, mode='lines+markers'))
fig_spo2.update_layout(title="SpO₂ (last 60s)", yaxis=dict(range=[80,100]), height=250)
spo2_placeholder.plotly_chart(fig_spo2, use_container_width=True)

# Temp
temp_arr = np.array(st.session_state.temp_buffer)
temp_times = np.linspace(-len(temp_arr)+1,0,len(temp_arr))
fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(x=temp_times, y=temp_arr, mode='lines+markers'))
fig_temp.update_layout(title="Body Temp (last 60s)", yaxis=dict(range=[35,39]), height=250)
temp_placeholder.plotly_chart(fig_temp, use_container_width=True)

# Metrics
spo2_metric.metric("SpO₂ (%)", f"{st.session_state.spo2_buffer[-1]:.1f}")
temp_metric.metric("Temp (°C)", f"{st.session_state.temp_buffer[-1]:.2f}")
hr_metric.metric("HR (bpm)", f"{hr}")
