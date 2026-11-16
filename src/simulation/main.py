import pandas as pd
from src.CommunityData import CommunityData
from src.model.Battery import Battery
from src.config import EXCEL_DATASET_PATH
from src.simulation.core.controller import RuleBasedController


def run_simulation(
        community_data: CommunityData,
        controller: RuleBasedController,
        time_step_hours: float = 0.25,
        use_batteries: bool = True,
        allow_sharing: bool = False
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
        step_cost = 0.0
        step_revenue = 0.0
        step_charged = 0.0
        step_discharged = 0.0
        final_bought = 0.0
        final_sold = 0.0

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

            if use_batteries and hid in batteries:
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

            step_cost += bought_kwh * float(row["buy_price"])
            step_revenue += sold_kwh * float(row["sell_price"])

            # Aggregate community totals
            step_solar += solar_kwh
            step_consumption += base_kw * time_step_hours
            step_ev += ev_kw * time_step_hours
            step_charged += energy_charged
            step_discharged += energy_discharged
            step_bought += bought_kwh
            step_sold += sold_kwh

            # if sharing between neighbors enabled:
            shared_kwh = 0.0
            final_bought = step_bought
            final_sold = step_sold

            if allow_sharing:
                shared_kwh = min(step_sold, step_bought)
                final_bought = max(0.0, step_bought - step_sold)
                final_sold = max(0.0, step_sold - step_bought)

        records.append({
            "time_step": t,
            "solar_kwh": step_solar,
            "consumption_kwh": step_consumption,
            "ev_kwh": step_ev,
            "total_demand_kwh": step_consumption + step_ev,
            "battery_charged_kwh": step_charged,
            "battery_discharged_kwh": step_discharged,
            "grid_bought_kwh": final_bought,
            "grid_sold_kwh": final_sold,
            "cost_eur": step_cost,
            "revenue_eur": step_revenue,
        })

    return pd.DataFrame(records)


def compute_results(table: pd.DataFrame, time_step_hours: float = 0.25) -> dict:
    """Compute community cost metrics from record table"""
    total_bought = table["grid_bought_kwh"].sum()
    total_sold = table["grid_sold_kwh"].sum()
    total_cost = table["cost_eur"].sum() - table["revenue_eur"].sum()

    total_solar = table["solar_kwh"].sum()
    solar_used_inside = total_solar - total_sold
    self_consumption_ratio = (solar_used_inside / total_solar) * 100 if total_solar > 0 else 0.0

    peak_grid_power = (table["grid_bought_kwh"] / time_step_hours).max()

    return {
        "Total Energy Bought": total_bought,
        "Total Energy Sold": total_sold,
        "Total Cost": total_cost,
        "Self-Consumption": self_consumption_ratio,
        "Peak Grid Power (kW)": peak_grid_power,
    }

def check_energy_balance(table: pd.DataFrame, tolerance: float = 1e-4) -> bool:
    """Energy In = Energy Out check"""
    energy_in = (table["solar_kwh"] + table["grid_bought_kwh"] + table["battery_discharged_kwh"])
    energy_out = (table["total_demand_kwh"] + table["grid_sold_kwh"] + table["battery_charged_kwh"])
    diff = (energy_in - energy_out).abs()
    max_error = diff.max()
    if max_error > tolerance:
        bad_step = diff.idxmax() + 1
        raise ValueError(f"Energy Balance failed at step {bad_step}. IN={energy_in:.4f}, OUT={energy_out:.4f}")
    return True

if __name__ == "__main__":
    community = CommunityData(EXCEL_DATASET_PATH)
    controller = RuleBasedController()

    table = run_simulation(
        community,
        controller,
        time_step_hours=0.25,
        use_batteries = True,
        allow_sharing = True
    )

    check_energy_balance(table)

    results = compute_results(table)
    for metric, val in results.items():
        print(f"{metric}: {val:.2f}")