import streamlit as st

# ---------------- DATABASE ---------------- #
equipment_db = {
    "1PM-700A": {
        "type": "Motor",
        "manufacturer": "Siemens",
        "rated_voltage": 415,
        "rated_current": 100,
        "power": "55kW"
    },
    "1TR-100A": {
        "type": "Transformer",
        "manufacturer": "ABB",
        "hv": "220kV",
        "lv": "11kV"
    }
}

# ---------------- FAULT LOGIC ---------------- #
def fault_analysis():

    current = 120
    rated = 100
    trip = 110
    trip_current = 129

    load = (current/rated)*100

    if load >= 120:
        return "CRITICAL", load, current, rated, trip, trip_current
    else:
        return "NORMAL", load, current, rated, trip, trip_current

# ---------------- UI ---------------- #
st.set_page_config(page_title="EEAMB", layout="wide")

st.title("⚡ EEAMB - Electrical Equipment Analysis of Maintenance Details")

tag = st.text_input("Enter Tag Number")

if st.button("Analyze"):

    if tag not in equipment_db:
        st.error("❌ Tag not found")
    else:
        eq = equipment_db[tag]

        status, load, current, rated, trip, trip_current = fault_analysis()

        # -------- EQUIPMENT DETAILS -------- #
        st.subheader("🧾 Equipment Details")

        st.write("Type:", eq["type"])
        st.write("Manufacturer:", eq["manufacturer"])

        if eq["type"] == "Motor":
            st.write("Rated Voltage:", eq["rated_voltage"], "V")
            st.write("Rated Current:", eq["rated_current"], "A")
            st.write("Power:", eq["power"])

        if eq["type"] == "Transformer":
            st.write("HV:", eq["hv"])
            st.write("LV:", eq["lv"])

        # -------- FAULT -------- #
        st.subheader("🚨 Fault Analysis")

        if status == "CRITICAL":
            st.error("🔴 CRITICAL CONDITION")
        else:
            st.success("🟢 NORMAL")

        st.write("Thermal Protection Activated")
        st.write("Current:", current, "A")
        st.write("Rated:", rated, "A")
        st.write("Trip Setting:", trip, "A")
        st.write("Trip Relay Acted Current:", trip_current, "A")
        st.write("Load:", round(load,2), "%")
        st.write("Alarm Time: 5 sec")
        st.write("Trip Time: 10 sec")

        # -------- REASON -------- #
        st.subheader("🧠 Reason")

        st.write("""
Overload condition occurred due to current exceeding 120% of rated capacity

Possible Causes:
- Excess mechanical load
- Bearing failure
- Voltage imbalance
- Cooling failure
        """)

        # -------- PROTECTION -------- #
        st.subheader("🛡️ Protection Details")

        st.write("Thermal Protection → Setting: 100A, Trip: 110A, Trip Current: 120A (120%)")
        st.write("Overload Protection → Setting: 100A, Trip: 115A, Trip Current: 120A (120%)")

        # -------- MAINTENANCE -------- #
        st.subheader("🔧 Maintenance")

        st.write("Recommended Maintenance Type: Predictive + Corrective")

        st.write("""
Suggested Actions:
- Immediate load reduction
- Bearing inspection
- Lubrication check
- Thermal relay calibration
        """)

        # -------- PROCEDURE -------- #
        st.subheader("📜 Procedure")

        st.write("""
Step 1: Safety & Isolation
- PTW
- MCCB OFF / Isolator OFF / Breaker OFF
- Rack-out feeder
- LOTO
- Zero voltage

Step 6: Re-commission
- Ensure proper de-isolation with safety
- Remove LOTO after clearance
- Rack-in feeder / CB
- Restore supply
- No-load run
- Monitor current & temperature
        """)