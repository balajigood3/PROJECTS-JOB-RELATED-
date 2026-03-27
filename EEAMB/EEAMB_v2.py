# 1. Define the DB first so functions can access it, or pass it as an argument
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
        "hv": "220kV",
        "lv": "11kV",
        "manufacturer": "ABB"
    },
    "1G-200A": {
        "type": "Generator",
        "power": "5MW"
    }
}

def fault_analysis(eq):
    # Simulated values (replace with real sensor data later)
    current = 120
    rated = eq.get("rated_current", 100) # Use DB value if available
    
    load = (current / rated) * 100

    if load >= 120:
        return {
            "status": "CRITICAL",
            "fault": "Overload",
            "reason": f"Overload condition at {load}% capacity.\n\nPossible Causes:\n- Excess mechanical load\n- Bearing failure\n- Voltage imbalance\n- Cooling failure"
        }

    return {
        "status": "NORMAL",
        "fault": "None",
        "reason": "Normal operation within limits."
    }

def EEAMB_v2(tag):
    if tag not in equipment_db:
        print(f"❌ Tag '{tag}' not found in database.")
        return

    eq = equipment_db[tag]

    print("\n" + "="*25)
    print("   EEAMB OUTPUT")
    print("="*25)

    # Equipment details
    print(f"Equipment Type: {eq['type']}")
    print(f"Manufacturer:   {eq.get('manufacturer', '-')}")

    # Fault Analysis
    result = fault_analysis(eq)

    print("\n🚨 Fault Analysis")
    print(f"Status: {result['status']}")
    print(f"Fault:  {result['fault']}")

    print("\n🧠 Reason")
    print(result["reason"])

    # Protection (Fixed template)
    print("\n🛡️ Protection")
    print("Thermal Protection → Setting: 100A, Trip: 110A, Trip Current: 120A (120%)")

    # Maintenance
    print("\n🔧 Maintenance")
    print("Recommended: Predictive + Corrective")

# 2. Correct the main entry point
if __name__ == "__main__":
    tag_input = input("Enter Tag (e.g., 1PM-700A): ").strip()
    EEAMB_v2(tag_input)
