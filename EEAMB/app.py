import streamlit as st
import joblib
import pandas as pd
import os

# Get the directory where app.py is located
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, 'eeamb_model.pkl')

# To this:
model = joblib.load("eeamb_model.pk1")

FEATURES = [
    "VR","VY","VB",
    "IR","IY","IB",
    "temperature",
    "MW","MVAR","MVA"
]

# Prediction function
def predict_fault(input_dict):
    df = pd.DataFrame([input_dict])[FEATURES]
    return model.predict(df)[0]

def calculate_load(ir,iy,ib,rated=100):
    return round(((ir+iy+ib)/3)/rated*100,2)

# UI
st.title("⚡ eeamb - Electrical Equipment Analysis")

tag = st.text_input("Enter Tag Number")

st.subheader("SCADA Inputs")

vr = st.number_input("Voltage R", value=415.0)
vy = st.number_input("Voltage Y", value=412.0)
vb = st.number_input("Voltage B", value=418.0)

ir = st.number_input("Current R", value=120.0)
iy = st.number_input("Current Y", value=118.0)
ib = st.number_input("Current B", value=122.0)

temp = st.number_input("Temperature", value=95.0)

mw = st.number_input("MW", value=0.05)
mvar = st.number_input("MVAR", value=0.01)
mva = st.number_input("MVA", value=0.06)

if st.button("Analyze"):

    input_data = {
        "VR":vr,"VY":vy,"VB":vb,
        "IR":ir,"IY":iy,"IB":ib,
        "temperature":temp,
        "MW":mw,"MVAR":mvar,"MVA":mva
    }

    fault = predict_fault(input_data)
    load = calculate_load(ir,iy,ib)

    st.subheader("🚨 Fault Analysis")

    st.write(f"Fault: {fault}")
    st.write(f"Load: {load}%")

    if load > 120:
        st.error("🔴 CRITICAL CONDITION")

        st.write("Thermal Protection Activated")
        st.write("Current: 120A")
        st.write("Rated: 100A")
        st.write("Trip Setting: 110A")
        st.write("Trip Relay Acted Current: 129A")
        st.write("Load: 120%")
        st.write("Alarm Time: 5 sec")
        st.write("Trip Time: 10 sec")

    st.subheader("🧠 Reason")

    st.write("""
Overload condition occurred due to current exceeding 120% of rated capacity

Possible Causes:
- Excess mechanical load
- Bearing failure
- Voltage imbalance
- Cooling failure
    """)

    st.subheader("🔧 Maintenance")

    st.write("""
Recommended Maintenance Type:
Predictive + Corrective

Suggested Actions:
- Immediate load reduction
- Bearing inspection
- Lubrication check
- Thermal relay calibration
    """)