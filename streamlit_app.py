import streamlit as st

st.set_page_config(page_title="EMDR SYNC", layout="wide")

# Title
st.markdown(
    """
    <style>
    .title-box {
        background-color: #a3d5ff;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        color: #1a1a1a;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    </style>
    <div class="title-box">EMDR SYNC</div>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.header("Settings")

speed = st.sidebar.slider("Speed", 1, 25, 10)
size = st.sidebar.slider("Ball Size", 20, 120, 50)

ball_color = st.sidebar.color_picker("Ball Color", "#ff4b4b")
container_color = st.sidebar.color_picker("Container Background", "#f0f4f8")

pattern = st.sidebar.selectbox(
    "Movement Pattern",
    ["Left ↔ Right", "Up ↕ Down", "Circle", "Square", "Diagonal"]
)

duration = st.sidebar.slider(
    "Session Duration (minutes)",
    min_value=1,
    max_value=60,
    value=5
)

pattern_js = {
    "Left ↔ Right": "horizontal",
    "Up ↕ Down": "vertical",
    "Circle": "circle",
    "Square": "square",
    "Diagonal": "diagonal"
}[pattern]

# HTML + JS
html = f"""
<style>

.wrapper {{
display:flex;
flex-direction:column;
align-items:center;
padding-top:20px;
}}

.controls {{
margin-bottom:15px;
}}

button {{
padding:10px 20px;
font-size:16px;
border:none;
border-radius:10px;
background:#4CAF50;
color:white;
cursor:pointer;
box-shadow:0 4px 10px rgba(0,0,0,0.2);
}}

.container {{
position:relative;
height:65vh;
width:90%;
background:{container_color};
border-radius:25px;
box-shadow:0 10px 30px rgba(0,0,0,0.25);
overflow:hidden;
}}

.ball {{
position:absolute;
width:{size}px;
height:{size}px;
border-radius:50%;
background:{ball_color};
}}

.timer {{
margin-top:12px;
font-size:22px;
font-weight:bold;
}}

</style>

<div class="wrapper">

<div class="controls">
<button onclick="toggleAnimation()" id="toggleBtn">Start</button>
</div>

<div class="container" id="container">
<div class="ball" id="ball"></div>
</div>

<div class="timer" id="timerDisplay"></div>

</div>

<script>

const ball = document.getElementById("ball")
const container = document.getElementById("container")
const timerDisplay = document.getElementById("timerDisplay")
const toggleBtn = document.getElementById("toggleBtn")

let x = 100
let y = 100
let dx = {speed}
let dy = {speed}
let angle = 0

let running = false

let totalSeconds = {duration} * 60
let remaining = totalSeconds
let timerInterval = null

// Initialize timer display
updateTimerDisplay()

function toggleAnimation() {{
    running = !running
    toggleBtn.innerText = running ? "Stop" : "Start"

    if (running) {{
        startTimer()
        animate()
    }} else {{
        stopTimer()
    }}
}}

function startTimer() {{
    if (timerInterval) return

    timerInterval = setInterval(() => {{
        remaining--

        updateTimerDisplay()

        if (remaining <= 0) {{
            running = false
            toggleBtn.innerText = "Start"
            stopTimer()
        }}
    }}, 1000)
}}

function stopTimer() {{
    clearInterval(timerInterval)
    timerInterval = null
}}

function updateTimerDisplay() {{
    let min = Math.floor(remaining / 60)
    let sec = remaining % 60

    timerDisplay.innerText = 
        "Time left: " + 
        String(min).padStart(2, '0') + ":" + 
        String(sec).padStart(2, '0')
}}

function animate() {{

    if (!running) return

    const w = container.clientWidth
    const h = container.clientHeight
    const size = {size}

    let mode = "{pattern_js}"

    if(mode === "horizontal") {{
        x += dx
        if(x > w-size || x < 0) dx *= -1
    }}

    else if(mode === "vertical") {{
        y += dy
        if(y > h-size || y < 0) dy *= -1
    }}

    else if(mode === "diagonal") {{
        x += dx
        y += dy

        if(x > w-size || x < 0) dx *= -1
        if(y > h-size || y < 0) dy *= -1
    }}

    else if(mode === "circle") {{

        angle += 0.03 * {speed}

        let cx = w/2
        let cy = h/2
        let r = Math.min(w,h)/3

        x = cx + r * Math.cos(angle)
        y = cy + r * Math.sin(angle)
    }}

    else if(mode === "square") {{

        x += dx

        if(x >= w-size) {{
            x = w-size
            dx = 0
            dy = {speed}
        }}

        if(y >= h-size) {{
            y = h-size
            dy = 0
            dx = -{speed}
        }}

        if(x <= 0 && dx < 0) {{
            dx = 0
            dy = -{speed}
        }}

        if(y <= 0 && dy < 0) {{
            dy = 0
            dx = {speed}
        }}
    }}

    ball.style.left = x + "px"
    ball.style.top = y + "px"

    requestAnimationFrame(animate)
}}

</script>
"""

st.components.v1.html(html, height=700)
