from src.model.Battery import Battery

BATTERY_SPECS = {
    "1": {
        "name": "BYD Battery-Box Premium HVS",
        "capacity_kwh": 10.24,
        "max_charge_kw": 10.24,
        "max_discharge_kw": 10.24,
        "efficiency": 0.96,
        "initial_charge_kwh": 5.12,
        "final_charge_kwh": 5.12,
    },
    "2": {
        "name": "Tesla Powerwall 2",
        "capacity_kwh": 13.5,
        "max_charge_kw": 5.0,
        "max_discharge_kw": 5.0,
        "efficiency": 0.90,
        "initial_charge_kwh": 6.75,
        "final_charge_kwh": 6.75,
    },
    "3": {
        "name": "LG RESU10H",
        "capacity_kwh": 9.8,
        "max_charge_kw": 5.0,
        "max_discharge_kw": 5.0,
        "efficiency": 0.95,
        "initial_charge_kwh": 4.9,
        "final_charge_kwh": 4.9,
    },
    "4": {
        "name": "SonnenBatterie 10",
        "capacity_kwh": 11.0,
        "max_charge_kw": 4.6,
        "max_discharge_kw": 4.6,
        "efficiency": 0.95,
        "initial_charge_kwh": 5.5,
        "final_charge_kwh": 5.5,
    },
    "5": {
        "name": "Huawei LUNA2000",
        "capacity_kwh": 15.0,
        "max_charge_kw": 5.0,
        "max_discharge_kw": 5.0,
        "efficiency": 0.95,
        "initial_charge_kwh": 7.5,
        "final_charge_kwh": 7.5,
    },
    "6": {
        "name": "Pylontech US5000",
        "capacity_kwh": 4.8,
        "max_charge_kw": 2.4,
        "max_discharge_kw": 2.4,
        "efficiency": 0.95,
        "initial_charge_kwh": 2.4,
        "final_charge_kwh": 2.4,
    },
    "7": {
        "name": "Sungrow SBR",
        "capacity_kwh": 12.8,
        "max_charge_kw": 12.8,
        "max_discharge_kw": 12.8,
        "efficiency": 0.95,
        "initial_charge_kwh": 6.4,
        "final_charge_kwh": 6.4,
    },
    "8": {
        "name": "Generic Industrial BESS",
        "capacity_kwh": 50.0,
        "max_charge_kw": 25.0,
        "max_discharge_kw": 25.0,
        "efficiency": 0.92,
        "initial_charge_kwh": 25.0,
        "final_charge_kwh": 25.0,
    },
}

battery = Battery.from_dict(8, BATTERY_SPECS["1"])

print(f"Initial SoC: {battery.soc:.1%}")

actual_kw = battery.charge(power_kw=2.0, duration_hours=0.25)

print(battery.current_charge)

discharged_kw = battery.discharge(power_kw=1.5, duration_hours=0.25)

print(battery.current_charge)

print('='*30)

full_bat = Battery(
    model_id=1, name="Test", capacity=10.0, max_charge=5.0,
    max_discharge=5.0, efficiency=0.9, current_charge=10.0
)
stored = full_bat.charge(power_kw=4.0, duration_hours=0.25)
print(f"Case 1 (Full Battery Charge): stored = {stored} kWh (expected 0.0)")

# 2. Discharging an empty battery should deliver NOTHING (0.0 kWh)
empty_bat = Battery(
    model_id=1, name="Test", capacity=10.0, max_charge=5.0,
    max_discharge=5.0, efficiency=0.9, current_charge=0.0
)
delivered = empty_bat.discharge(power_kw=4.0, duration_hours=0.25)
print(f"Case 2 (Empty Battery Discharge): delivered = {delivered} kWh (expected 0.0)")

# 3. Power exceeding max_charge should be capped
bat3 = Battery(
    model_id=1, name="Test", capacity=20.0, max_charge=4.0,
    max_discharge=4.0, efficiency=1.0, current_charge=0.0
)
# Request 10 kW for 1 hour -> capped at 4 kW * 1h = 4.0 kWh
stored = bat3.charge(power_kw=10.0, duration_hours=1.0)
print(f"Case 3 (Max Charge Power Limit): stored = {stored} kWh (expected 4.0)")

# 4. Check efficiency: 4 kWh absorbed at 90% efficiency -> 3.6 kWh stored
bat4 = Battery(
    model_id=1, name="Test", capacity=10.0, max_charge=10.0,
    max_discharge=10.0, efficiency=0.90, current_charge=0.0
)
stored = bat4.charge(power_kw=4.0, duration_hours=1.0)
print(f"Case 4 (Efficiency 90%): stored = {stored} kWh (expected 3.6)")
