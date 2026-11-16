import pandas as pd
from src.CommunityData import CommunityData
from src.model.Battery import Battery
from src.config import EXCEL_DATASET_PATH
from src.simulation.core.controller import RuleBasedController


def run_simulation(
        community_data: CommunityData,
        controller: RuleBasedController,
        time_step_hours: float = 0.25,
) -> pd.DataFrame:

    battery_specs = community_data.get_battery_specs()
    batteries: dict[str, Battery] = {
        hid: Battery.from_dict(spec["model_id"], spec)
        for hid, spec in battery_specs.items()
    }

    records = []
    num_steps = 96

    for t in range(1, num_steps + 1):
        df = community_data.get_data(t)

        step_solar = 0.0
        step_consumption = 0.0
        step_ev = 0.0
        step_bought = 0.0
        step_sold = 0.0
        step_charged = 0.0
        step_discharged = 0.0

        for hid, row in df.iterrows():
            solar_kw = float(row["solar_production"])
            base_kw = float(row["consumption"])
            ev_kw = float(row["ev_consumption"])
            demand_kw = base_kw + ev_kw

            # Power * Time -> Energy
            solar_kwh = solar_kw * time_step_hours
            demand_kwh = demand_kw * time_step_hours

            # Request update from controller
            charge_kw, discharge_kw = controller.decide(solar_kw, demand_kw)

            energy_charged = 0.0
            energy_discharged = 0.0

            if hid in batteries:
                battery = batteries[hid]
                if charge_kw > 0.0:
                    battery.charge(charge_kw, duration_hours=time_step_hours)
                    energy_charged = battery.last_energy_absorbed
                    if battery.last_energy_absorbed is None:
                        energy_charged = charge_kw * time_step_hours
                elif discharge_kw > 0.0:
                    energy_discharged = battery.discharge(discharge_kw, duration_hours=time_step_hours)

            # Buy what is missing or sell what is left over
            # Net balance at household busbar
            net_energy = (solar_kwh + energy_discharged) - (demand_kwh + energy_charged)

            if net_energy > 0:
                sold_kwh = net_energy
                bought_kwh = 0.0
            else:
                bought_kwh = -net_energy
                sold_kwh = 0.0

            # Aggregate community totals
            step_solar += solar_kwh
            step_consumption += base_kw * time_step_hours
            step_ev += ev_kw * time_step_hours
            step_charged += energy_charged
            step_discharged += energy_discharged
            step_bought += bought_kwh
            step_sold += sold_kwh

        records.append({
            "time_step": t,
            "solar_kwh": step_solar,
            "consumption_kwh": step_consumption,
            "ev_kwh": step_ev,
            "total_demand_kwh": step_consumption + step_ev,
            "battery_charged_kwh": step_charged,
            "battery_discharged_kwh": step_discharged,
            "grid_bought_kwh": step_bought,
            "grid_sold_kwh": step_sold,
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    community = CommunityData(EXCEL_DATASET_PATH)
    controller = RuleBasedController()

    table = run_simulation(community, controller)
    print("Simulation finished. RecordedTable.head():")
    print(table)