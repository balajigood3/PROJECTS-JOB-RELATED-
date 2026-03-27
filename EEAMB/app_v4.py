import streamlit as st

# ---------------- TAG → EQUIPMENT ---------------- #
def detect_equipment(tag):
    if "PM" in tag:
        return "Motor"
    elif "TR" in tag:
        return "Transformer"
    elif "G" in tag:
        return "Generator"
    else:
        return "Unknown"

# ---------------- CONDITION ---------------- #
def get_condition():
    return "CRITICAL", 120

# ---------------- FAULT ---------------- #
def get_fault():
    return """
Overload condition occurred due to current exceeding 120% of rated capacity

Possible Causes:
- Excess mechanical load
- Bearing failure
- Voltage imbalance
- Cooling failure
"""

# ---------------- MAINTENANCE ---------------- #
def get_maintenance(eq):

    if eq == "Motor":
        return """
Preventive Maintenance – Motor

Step 1: Safety
- PTW
- MCCB OFF / Isolator OFF
- LOTO
- Zero voltage

Step 2: Cleaning
- Motor cleaned
- Fan checked

Step 3: Lubrication
- Grease applied (DE/NDE)

Step 6: Re-commission
- De-isolation
- Rack-in feeder
- Monitor current
"""
    return "General maintenance"

# ---------------- PROTECTION ---------------- #
def get_protection():
    return """
Thermal Protection → Setting: 100A, Trip: 110A, Trip Current: 120A (120%)
Overload Protection → Setting: 100A, Trip: 115A, Trip Current: 120A (120%)
"""

# ---------------- UI ---------------- #
st.title("⚡ EEAMB - Electrical Equipment Analysis")

tag = st.text_input("Enter Tag Number (Ex: 1PM-700A)")

mode = st.selectbox(
    "Select Output Type",
    ["Condition","Fault","Maintenance","Protection"]
)

if st.button("Analyze"):

    eq = detect_equipment(tag)

    st.subheader(f"Equipment: {eq}")

    if mode == "Condition":
        status, load = get_condition()
        st.write("Status:", status)
        st.write("Load:", load, "%")

    elif mode == "Fault":
        st.subheader("Fault Reason")
        st.write(get_fault())

    elif mode == "Maintenance":
        st.subheader("Maintenance Procedure")
        st.write(get_maintenance(eq))

    elif mode == "Protection":
        st.subheader("Protection Details")
        st.write(get_protection())