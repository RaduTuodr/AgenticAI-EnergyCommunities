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
