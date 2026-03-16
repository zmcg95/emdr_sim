import streamlit as st

st.set_page_config(page_title="EMDR SYNC", layout="wide")

# Title Box
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    .title-box {
        background-color: #a3d5ff; /* pastel blue */
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        color: #1a1a1a;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        font-family: 'Roboto', sans-serif;
    }

    .intro-box {
        background-color: #ffffff; /* white */
        border-radius: 20px;
        padding: 25px;
        margin-top: 30px;
        margin-left: 5%;
        margin-right: 5%;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        font-family: 'Roboto', sans-serif;
        font-size: 1.1em;
        line-height: 1.6em;
        color: #1a1a1a;
    }
    </style>

    <div class="title-box">EMDR SYNC</div>
    """,
    unsafe_allow_html=True
)

# Sidebar Settings
st.sidebar.header("Settings")

speed = st.sidebar.slider(
    "Speed",
    min_value=1,
    max_value=25,
    value=10
)

size = st.sidebar.slider(
    "Ball Size",
    min_value=20,
    max_value=120,
    value=50
)

ball_color = st.sidebar.color_picker(
    "Ball Color",
    "#ff4b4b"
)

container_color = st.sidebar.color_picker(
    "Container Background",
    "#f0f4f8"
)

pattern = st.sidebar.selectbox(
    "Movement Pattern",
    [
        "Left ↔ Right",
        "Up ↕ Down",
        "Circle",
        "Square",
        "Diagonal"
    ]
)

pattern_js = {
    "Left ↔ Right": "horizontal",
    "Up ↕ Down": "vertical",
    "Circle": "circle",
    "Square": "square",
    "Diagonal": "diagonal"
}[pattern]

# Animation HTML
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

function animate() {{

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

animate()

</script>
"""

st.components.v1.html(html, height=650)

# Intro / Instructions Box
st.markdown(
    """
    <div class="intro-box">
    <strong>Welcome to EMDR SYNC</strong><br><br>
    EMDR (Eye Movement Desensitization and Reprocessing) therapy uses bilateral visual stimulation to help process and reduce emotional stress.<br><br>
    <strong>Instructions:</strong> Adjust the speed, ball size, color, and movement pattern using the sidebar. Focus your gaze on the moving ball, following it with your eyes smoothly from side to side, up and down, or in the chosen motion pattern. Use this tool as part of a guided EMDR session under professional supervision.
    </div>
    """,
    unsafe_allow_html=True
)
