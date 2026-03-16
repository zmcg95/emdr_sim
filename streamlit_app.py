import streamlit as st

st.set_page_config(page_title="EMDR Tools", layout="wide")

# ---- SESSION STATE FOR PAGES ----
if 'page' not in st.session_state:
    st.session_state.page = "home"

# ---- PAGE NAVIGATION FUNCTION ----
def go_to(page_name):
    st.session_state.page = page_name

# ---- HOME PAGE ----
if st.session_state.page == "home":
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        .home-title {
            text-align:center;
            font-size:4em;
            font-weight:bold;
            color:#1a1a1a;
            font-family:'Roboto', sans-serif;
            margin-bottom:50px;
        }

        .card-container {
            display:flex;
            justify-content:space-around;
            flex-wrap:wrap;
        }

        .card {
            background-color:#a3d5ff;
            border-radius:20px;
            width:300px;
            height:200px;
            display:flex;
            justify-content:center;
            align-items:center;
            font-size:1.5em;
            font-weight:bold;
            cursor:pointer;
            transition: transform 0.2s;
            text-align:center;
            box-shadow:0 8px 20px rgba(0,0,0,0.2);
            margin:20px;
            font-family:'Roboto', sans-serif;
        }

        .card:hover {
            transform: scale(1.05);
        }
        </style>

        <div class="home-title">EMDR TOOLS</div>
        """,
        unsafe_allow_html=True
    )

    # Navigation buttons (cards)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("EMDR SYNC", key="sync_btn"):
            go_to("sync")
    with col2:
        st.button("Coming Soon", key="coming1", disabled=True)
    with col3:
        st.button("Coming Soon", key="coming2", disabled=True)

# ---- EMDR SYNC PAGE ----
elif st.session_state.page == "sync":
    st.button("← Back to Home", on_click=lambda: go_to("home"))

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

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
            font-family: 'Roboto', sans-serif;
        }
        </style>

        <div class="title-box">EMDR SYNC</div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar Settings
    st.sidebar.header("Settings")
    speed = st.sidebar.slider("Speed", 1, 25, 10)
    size = st.sidebar.slider("Ball Size", 20, 120, 50)
    ball_color = st.sidebar.color_picker("Ball Color", "#ff4b4b")
    container_color = st.sidebar.color_picker("Container Background", "#f0f4f8")
    pattern = st.sidebar.selectbox("Movement Pattern", ["Left ↔ Right","Up ↕ Down","Circle","Square","Diagonal"])
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
    const ball = document.getElementById("ball");
    const container = document.getElementById("container");
    let x = 100, y = 100, dx = {speed}, dy = {speed}, angle = 0;

    function animate() {{
        const w = container.clientWidth;
        const h = container.clientHeight;
        let mode = "{pattern_js}";

        if(mode==="horizontal") {{ x += dx; if(x > w-{size} || x < 0) dx *= -1; }}
        else if(mode==="vertical") {{ y += dy; if(y > h-{size} || y < 0) dy *= -1; }}
        else if(mode==="diagonal") {{ x += dx; y += dy; if(x > w-{size} || x < 0) dx *= -1; if(y > h-{size} || y < 0) dy *= -1; }}
        else if(mode==="circle") {{
            angle += 0.03*{speed};
            let cx = w/2, cy = h/2, r = Math.min(w,h)/3;
            x = cx + r*Math.cos(angle);
            y = cy + r*Math.sin(angle);
        }}
        else if(mode==="square") {{
            x += dx;
            if(x >= w-{size}) {{ x = w-{size}; dx = 0; dy = {speed}; }}
            if(y >= h-{size}) {{ y = h-{size}; dy = 0; dx = -{speed}; }}
            if(x <= 0 && dx < 0) {{ dx = 0; dy = -{speed}; }}
            if(y <= 0 && dy < 0) {{ dy = 0; dx = {speed}; }}
        }}

        ball.style.left = x + "px";
        ball.style.top = y + "px";
        requestAnimationFrame(animate);
    }}

    animate();
    </script>
    """
    st.components.v1.html(html, height=650)
