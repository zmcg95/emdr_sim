import streamlit as st
import time

st.set_page_config(page_title="EMDR Tool", layout="wide")

st.title("🧠 EMDR Bilateral Stimulation Tool")

# Sidebar controls
st.sidebar.header("Settings")

speed = st.sidebar.slider(
    "Ball Speed",
    min_value=0.01,
    max_value=0.2,
    value=0.05,
    step=0.01,
    help="Lower = faster movement"
)

color = st.sidebar.color_picker("Ball Color", "#ff4b4b")

direction = st.sidebar.selectbox(
    "Start Direction",
    ["Left → Right", "Right → Left"]
)

if direction == "Left → Right":
    direction_value = 1
else:
    direction_value = -1

# Controls
start = st.sidebar.button("Start")
stop = st.sidebar.button("Stop")

# Center container
container = st.empty()

# HTML animation template
def render_ball(position, color):
    html = f"""
    <div style="position:relative;height:200px;">
        <div style="
            position:absolute;
            left:{position}%;
            top:50%;
            transform:translate(-50%, -50%);
            width:50px;
            height:50px;
            border-radius:50%;
            background:{color};
            ">
        </div>
    </div>
    """
    container.markdown(html, unsafe_allow_html=True)


# Animation loop
if start:

    pos = 0 if direction_value == 1 else 100
    direction = direction_value

    while True:

        render_ball(pos, color)

        pos += direction * 2

        if pos >= 100:
            direction = -1

        if pos <= 0:
            direction = 1

        time.sleep(speed)

        if stop:
            break

else:
    render_ball(50, color)
