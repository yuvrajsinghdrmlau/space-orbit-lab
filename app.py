import plotly.graph_objects as go
import streamlit as st

from model import simulate

st.set_page_config(page_title="Space Orbit Lab", layout="wide")
st.title("Space Orbit Lab")
st.caption("A bounded Earth/Mars two-body orbit simulator.")

with st.sidebar:
    body = st.selectbox("Body", ["Mars", "Earth"])
    altitude = st.number_input("Initial altitude (km)", 1.0, 100000.0, 400.0)
    duration = st.number_input("Duration (minutes)", 0.1, 100000.0, 120.0)
    inclination = st.slider("Inclination (degrees)", 0.0, 180.0, 35.0)
    speed_factor = st.number_input("Circular-speed factor", 0.05, 5.0, 1.0)
    run = st.button("Simulate", type="primary")

if run:
    result = simulate(body, altitude, duration, inclination, speed_factor)
    st.subheader(result["status"])
    columns = st.columns(len(result["summary"]))
    for column, (label, value) in zip(columns, result["summary"].items()):
        column.metric(label, f"{value:.6g}")
    channel = result["channels"]
    orbit = go.Figure(go.Scatter3d(x=channel["x_km"], y=channel["y_km"], z=channel["z_km"], mode="lines"))
    orbit.update_layout(title=f"Trajectory around {body}", scene_aspectmode="data")
    st.plotly_chart(orbit, width="stretch")
    history = go.Figure()
    history.add_scatter(x=channel["time_min"], y=channel["altitude_km"], name="Altitude (km)")
    history.add_scatter(x=channel["time_min"], y=channel["speed_km_s"], name="Speed (km/s)", yaxis="y2")
    history.update_layout(yaxis2={"overlaying": "y", "side": "right"})
    st.plotly_chart(history, width="stretch")
    st.json(result["checks"])
else:
    st.info("Choose parameters and click Simulate.")
