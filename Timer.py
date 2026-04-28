import streamlit as st
import time
import pytz
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="MK316 Customized Timer", layout="centered")

# ---------- Session State ----------
if "running" not in st.session_state:
    st.session_state.running = False
if "end_time" not in st.session_state:
    st.session_state.end_time = None
if "total_time" not in st.session_state:
    st.session_state.total_time = 10
if "time_up" not in st.session_state:
    st.session_state.time_up = False

# ---------- Functions ----------
def get_seoul_time():
    seoul_tz = pytz.timezone("Asia/Seoul")
    return datetime.now(seoul_tz).strftime("%H:%M:%S")

def draw_progress_circle(remaining_time, total_time, time_up=False):
    fig, ax = plt.subplots(figsize=(2.3, 2.3))

    if time_up:
        ax.pie(
            [1],
            colors=["#6d8c9c"],
            startangle=90,
            counterclock=False,
            wedgeprops=dict(width=0.25)
        )
        ax.text(0, 0, "Time's Up!", fontsize=12, ha="center", va="center", color="gray")
    else:
        fraction = remaining_time / total_time if total_time > 0 else 0
        ax.pie(
            [fraction, 1 - fraction],
            colors=["#5785A4", "#D5DEDD"],
            startangle=90,
            counterclock=False,
            wedgeprops=dict(width=0.3)
        )

        minutes, seconds = divmod(int(remaining_time), 60)
        ax.text(0, 0, f"{minutes:02d}:{seconds:02d}", fontsize=14, ha="center", va="center")

    ax.set_aspect("equal")
    ax.axis("off")
    return fig

def start_timer(seconds):
    st.session_state.total_time = seconds
    st.session_state.end_time = time.time() + seconds
    st.session_state.running = True
    st.session_state.time_up = False

def reset_timer():
    st.session_state.running = False
    st.session_state.end_time = None
    st.session_state.time_up = False

# ---------- UI ----------
st.title("🐧 MK316 Customized Timer")

st.markdown(
    f"""
    <h2 style='text-align:center; font-size:60px; color:#5785A4;'>
        {get_seoul_time()}
    </h2>
    """,
    unsafe_allow_html=True
)

seconds = st.number_input(
    "Set Countdown Time (in seconds)",
    min_value=1,
    max_value=7200,
    value=10
)

col1, col2 = st.columns([2, 1])

with col1:
    start_col, reset_col = st.columns(2)

    with start_col:
        if st.button("Start"):
            start_timer(seconds)

    with reset_col:
        if st.button("Reset"):
            reset_timer()

with col2:
    progress_placeholder = st.empty()

message_placeholder = st.empty()

# ---------- Timer Logic ----------
if st.session_state.running:
    remaining_time = max(0, int(st.session_state.end_time - time.time()))

    if remaining_time > 0:
        fig = draw_progress_circle(remaining_time, st.session_state.total_time)
        progress_placeholder.pyplot(fig)

        minutes, seconds_left = divmod(remaining_time, 60)
        message_placeholder.write(f"**Remaining Time:** {minutes:02d}:{seconds_left:02d}")

        time.sleep(1)
        st.rerun()

    else:
        st.session_state.running = False
        st.session_state.time_up = True

if st.session_state.time_up:
    fig = draw_progress_circle(0, st.session_state.total_time, time_up=True)
    progress_placeholder.pyplot(fig)
    message_placeholder.success("⏰ Time's Up!")

    try:
        with open("timesup.mp3", "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
    except FileNotFoundError:
        st.warning("timesup.mp3 file was not found. Please upload it to the app folder.")
else:
    fig = draw_progress_circle(st.session_state.total_time, st.session_state.total_time)
    progress_placeholder.pyplot(fig)
