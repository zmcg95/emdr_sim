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

st.sidebar.markdown("---")

# Sidebar controls (UI moved here)
st.sidebar.markdown("### Session Control")

start_button = st.sidebar.button("Start / Stop")

timer_placeholder = st.sidebar.empty()

pattern_js = {
    "Left ↔ Right": "horizontal",
    "Up ↕ Down": "vertical",
    "Circle": "circle",
    "Square": "square",
    "Diagonal": "diagonal"
}[pattern]

# HTML + JS (no controls inside)
html = f"""
<style>

.wrapper {{
display:flex;
justify-content:center;
align-items:center;
padding-top:20px;
}}

.container {{
position:relative;
height:70vh;
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

</style>

<div class="wrapper">
<div class="container" id="container">
<div class="ball" id="ball"></div>
</div>
</div>

<script>

const ball = document.getElementById("ball")
const container = document.getElementById("container")

let x = 100
let y = 100
let dx = {speed}
let dy = {speed}
let angle = 0

let running = false

let totalSeconds = {duration} * 60
let remaining = totalSeconds

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

st.components.v1.html(html, height=750)

# -----------------------
# Python-side timer logic
# -----------------------

if "running" not in st.session_state:
    st.session_state.running = False
    st.session_state.remaining = duration * 60

# Handle button
if start_button:
    st.session_state.running = not st.session_state.running

# Timer update loop
if st.session_state.running:
    st.session_state.remaining -= 1

    if st.session_state.remaining <= 0:
        st.session_state.running = False
        st.session_state.remaining = 0

    st.rerun()

# Display timer in sidebar
minutes = st.session_state.remaining // 60
seconds = st.session_state.remaining % 60

timer_placeholder.markdown(
    f"### ⏱ Time left: {minutes:02d}:{seconds:02d}"
)
