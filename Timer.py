import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path

st.set_page_config(page_title="MK316 Customized Timer", layout="centered")

st.title("🐧 MK316 Customized Timer")

seconds = st.number_input(
    "Set Countdown Time (in seconds)",
    min_value=1,
    max_value=7200,
    value=10
)

# Optional audio file
audio_html = ""
audio_path = Path("timesup.mp3")

if audio_path.exists():
    audio_bytes = audio_path.read_bytes()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
    <audio id="alarmSound">
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """

components.html(
    f"""
    <div style="text-align:center; font-family:Arial, sans-serif;">

        <h3>Current Time in Korea</h3>

        <div id="clock" style="
            font-size:60px;
            font-weight:700;
            color:#5785A4;
            margin-bottom:25px;">
        </div>

        <svg width="230" height="230" viewBox="0 0 230 230">
            <circle
                cx="115" cy="115" r="90"
                stroke="#D5DEDD"
                stroke-width="22"
                fill="none"
            />
            <circle
                id="progressCircle"
                cx="115" cy="115" r="90"
                stroke="#5785A4"
                stroke-width="22"
                fill="none"
                stroke-linecap="round"
                transform="rotate(-90 115 115)"
            />
            <text
                id="timerText"
                x="115" y="123"
                text-anchor="middle"
                font-size="28"
                font-weight="700"
                fill="#333">
                00:00
            </text>
        </svg>

        <div style="margin-top:20px;">
            <button onclick="startTimer()" style="
                font-size:18px;
                padding:10px 24px;
                margin-right:10px;
                border-radius:8px;
                border:1px solid #ccc;
                cursor:pointer;">
                Start
            </button>

            <button onclick="resetTimer()" style="
                font-size:18px;
                padding:10px 24px;
                border-radius:8px;
                border:1px solid #ccc;
                cursor:pointer;">
                Reset
            </button>
        </div>

        <p id="message" style="
            font-size:22px;
            font-weight:700;
            color:#666;
            margin-top:20px;">
        </p>

        {audio_html}
    </div>

    <script>
        const totalTime = {seconds};
        let remainingTime = totalTime;
        let timerInterval = null;

        const circle = document.getElementById("progressCircle");
        const radius = 90;
        const circumference = 2 * Math.PI * radius;

        circle.style.strokeDasharray = circumference;
        circle.style.strokeDashoffset = 0;

        function formatTime(seconds) {{
            const min = Math.floor(seconds / 60);
            const sec = seconds % 60;
            return String(min).padStart(2, "0") + ":" + String(sec).padStart(2, "0");
        }}

        function updateClock() {{
            const now = new Date();
            const koreaTime = new Intl.DateTimeFormat("en-GB", {{
                timeZone: "Asia/Seoul",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hour12: false
            }}).format(now);

            document.getElementById("clock").innerHTML = koreaTime;
        }}

        function updateTimerDisplay() {{
            document.getElementById("timerText").textContent = formatTime(remainingTime);

            const progress = remainingTime / totalTime;
            circle.style.strokeDashoffset = circumference * (1 - progress);
        }}

        function startTimer() {{
            if (timerInterval !== null) return;

            document.getElementById("message").textContent = "";

            timerInterval = setInterval(() => {{
                remainingTime -= 1;
                updateTimerDisplay();

                if (remainingTime <= 0) {{
                    clearInterval(timerInterval);
                    timerInterval = null;
                    remainingTime = 0;
                    updateTimerDisplay();

                    document.getElementById("timerText").textContent = "Done";
                    document.getElementById("message").textContent = "⏰ Time's Up!";

                    const alarm = document.getElementById("alarmSound");
                    if (alarm) {{
                        alarm.play();
                    }}
                }}
            }}, 1000);
        }}

        function resetTimer() {{
            clearInterval(timerInterval);
            timerInterval = null;
            remainingTime = totalTime;
            document.getElementById("message").textContent = "";
            updateTimerDisplay();
        }}

        updateClock();
        setInterval(updateClock, 1000);
        updateTimerDisplay();
    </script>
    """,
    height=560
)
