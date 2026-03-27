import streamlit as st
import pandas as pd
import joblib
import os

# Get the directory where app_v5.py is located
base_path = os.path.dirname(__file__)
model_path = os.path.join(base_path, "eeamb_model.pk1")

model = joblib.load(model_path)

# Load dataset & model
df = pd.read_csv(r"C:\Balaji - AI Course\Project\EEAMB.csv")
model = joblib.load(r"c:\Balaji - AI Course\Project\eeamb_model.pk1")

FEATURES = [
    "VR","VY","VB",
    "IR","IY","IB",
    "temperature",
    "MW","MVAR","MVA"
]

# -------- EQUIPMENT DETECTION -------- #
def detect_equipment(tag):
    if "PM" in tag:
        return "Motor"
    elif "TR" in tag:
        return "Transformer"
    elif "G" in tag:
        return "Generator"
    elif "UPS" in tag:
        return "UPS"
    else:
        return "Electrical Equipment"

# -------- PREDICTION -------- #
def predict_fault(row):
    data = pd.DataFrame([row])[FEATURES]
    return model.predict(data)[0]

if data.empty:
    row = df.sample(1).iloc[0]
    
# -------- REASON ENGINE -------- #
def get_reason(load):
    if load >= 120:
        return """Overload condition occurred due to current exceeding 120% of rated capacity

Possible Causes:
- Excess mechanical load
- Bearing failure
- Vol❌ Tag not found imbalance
- Cooling failure"""
    return "Normal operation"

# -------- MAINTENANCE ENGINE -------- #
def get_maintenance(eq):

    if eq == "Motor":
        return """Preventive Maintenance - Motor

Step 1: Safety
- PTW
- MCCB OFF / Isolator OFF / Breaker OFF
- Rack-out feeder
- LOTO
- Zero voltage

Step 6: Re-commission
- Ensure proper de-isolation with safety
- Remove LOTO
- Rack-in feeder / CB
- Monitor current & temperature"""
    
    if eq == "Transformer":
        return """Transformer Maintenance

- Oil level check
- Buchholz relay check
- Winding temperature monitoring"""

    return "General Maintenance Required"

# -------- PROTECTION ENGINE -------- #
def get_protection():
    return """Thermal Protection → Setting: 100A, Trip: 110A, Trip Current: 120A (120%)

Overload Protection → Setting: 100A, Trip: 115A, Trip Current: 120A (120%)

Earth Fault → Setting: 30mA, Trip: 35mA, Trip Current: 40mA"""

# -------- UI -------- #
st.set_page_config(layout="wide")
st.title("⚡ EEAMB - Electrical Equipment Analysis")

tag = st.text_input("Enter Tag Number (Ex: 1PM-700A)")

mode = st.selectbox(
    "Select Output Type",
    ["Condition","Fault","Maintenance","Protection","Full Output"]
)

if st.button("Analyze"):

    data = df[df["tag"] == tag]

    if data.empty:
        st.error("❌ Tag not found")
    else:
        row = data.iloc[0]
        eq = detect_equipment(tag)

        load = row["load_percent"]

        fault = predict_fault(row)
        reason = get_reason(load)

        # -------- EQUIPMENT -------- #
        st.subheader("🧾 Equipment Details")
        st.write("Type:", eq)
        st.write("Tag:", tag)

        # -------- CONDITION -------- #
        if mode == "Condition":
            st.write("Load:", load, "%")

        # -------- FAULT -------- #
        elif mode == "Fault":
            st.subheader("🚨 Fault")
            st.write(fault)

            st.subheader("🧠 Reason")
            st.write(reason)

        # -------- MAINTENANCE -------- #
        elif mode == "Maintenance":
            st.subheader("🔧 Maintenance")
            st.write(get_maintenance(eq))

        # -------- PROTECTION -------- #
        elif mode == "Protection":
            st.subheader("🛡️ Protection")
            st.write(get_protection())

        # -------- FULL OUTPUT (IMPORTANT 🔥) -------- #
        elif mode == "Full Output":

            st.subheader("🚨 Fault Analysis")
            st.write("Fault:", fault)
            st.write("Load:", load, "%")

            if load >= 120:
                st.error("🔴 CRITICAL CONDITION")

            st.subheader("🧠 Reason")
            st.write(reason)

            st.subheader("🛡️ Protection")
            st.write(get_protection())

            st.subheader("🔧 Maintenance")
            st.write(get_maintenance(eq))