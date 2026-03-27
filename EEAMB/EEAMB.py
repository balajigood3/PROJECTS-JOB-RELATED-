import pandas as pd
import numpy as np
import random

# 🔥 All Equipment Types
equipment_types = [
    "Motor","Transformer","Generator","Switchboard",
    "UPS","Battery","VFD","Lighting",
    "SurgeArrestor","CT","PT","CircuitBreaker",
    "CapacitorBank","PLC","Sensor"
]

# 🔥 Tag Mapping
equipment_codes = {
    "Motor":"PM",
    "Transformer":"TR",
    "Generator":"G",
    "Switchboard":"SB",
    "UPS":"UPS",
    "Battery":"BB",
    "VFD":"VFD",
    "Lighting":"LP",
    "SurgeArrestor":"SA",
    "CT":"CT",
    "PT":"PT",
    "CircuitBreaker":"CB",
    "CapacitorBank":"CAP",
    "PLC":"PLC",
    "Sensor":"SNS"
}

def generate_tag(eq):
    train = random.randint(1,7)
    code = equipment_codes[eq]
    num = random.randint(100,999)
    suffix = random.choice(["A","B",""])
    return f"{train}{code}-{num}{suffix}"

data=[]

for _ in range(15000):

    eq = random.choice(equipment_types)
    tag = generate_tag(eq)

    # 3 Phase Voltage
    vr,vy,vb = np.random.uniform(380,420,3)

    # 3 Phase Current
    ir,iy,ib = np.random.uniform(20,150,3)

    temp = np.random.uniform(25,100)

    avg_current = (ir+iy+ib)/3
    rated_current = 100

    load = (avg_current/rated_current)*100

    # ⚠️ Fault Logic
    if load > 120:
        fault = "Overload"
        protection = "Thermal"
        reason = "Load exceeded limit"
    elif temp > 90:
        fault = "Overheating"
        protection = "Thermal"
        reason = "High temperature"
    else:
        fault = "Normal"
        protection = "None"
        reason = "Normal operation"

    # ⚡ Power
    mw = round(random.uniform(0.01,0.1),3)
    mvar = round(random.uniform(0.005,0.05),3)
    mva = round(mw + mvar,3)

    data.append([
        tag, eq,
        vr,vy,vb,
        ir,iy,ib,
        temp,
        mw,mvar,mva,
        fault,reason,protection,load
    ])

df = pd.DataFrame(data, columns=[
    "tag","equipment",
    "VR","VY","VB",
    "IR","IY","IB",
    "temperature",
    "MW","MVAR","MVA",
    "fault","reason","protection","load_percent"
])

df.to_csv("bm3_full_dataset.csv",index=False)

print("✅ BM3 Dataset Created Successfully")