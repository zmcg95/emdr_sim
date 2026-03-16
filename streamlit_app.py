import streamlit as st

st.set_page_config(page_title="EMDR Bilateral Stimulation Tool", layout="wide")

st.title("🧠 EMDR Bilateral Stimulation Tool")

st.sidebar.header("Settings")

speed = st.sidebar.slider(
    "Speed",
    min_value=1,
    max_value=20,
    value=8,
    help="Higher = faster movement"
)

size = st.sidebar.slider(
    "Ball Size",
    min_value=20,
    max_value=120,
    value=50
)

color = st.sidebar.color_picker(
    "Ball Color",
    "#ff4b4b"
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

html = f"""
<style>

.container {{
position:relative;
height:70vh;
width:100%;
background-color:black;
overflow:hidden;
}}

.ball {{
position:absolute;
width:{size}px;
height:{size}px;
border-radius:50%;
background:{color};
}}

</style>

<div class="container">
<div class="ball" id="ball"></div>
</div>

<script>

const ball = document.getElementById("ball")
const container = document.querySelector(".container")

let x = 0
let y = 0
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

st.components.v1.html(html, height=600)
