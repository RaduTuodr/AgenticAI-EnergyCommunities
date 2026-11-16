import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


def _time_axis(num_steps: int, time_step_hours: float) -> list[datetime]:
    base = datetime(2024, 1, 1)
    delta = timedelta(hours=time_step_hours)
    return [base + i * delta for i in range(num_steps)]


def plot_community(community_df: pd.DataFrame, time_step_hours: float = 0.25) -> plt.Figure:
    times = _time_axis(len(community_df), time_step_hours)
    dt = time_step_hours

    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    fig.suptitle("Community — 24-hour Overview", fontsize=13)

    axes[0].plot(times, community_df["solar_kwh"] / dt, color="gold", label="Solar")
    axes[0].set_ylabel("kW")
    axes[0].legend()

    axes[1].plot(times, community_df["total_demand_kwh"] / dt, color="steelblue", label="Consumption")
    axes[1].set_ylabel("kW")
    axes[1].legend()

    # Approximate community battery SoC as running net energy stored
    batt_net = (community_df["battery_charged_kwh"] - community_df["battery_discharged_kwh"]).cumsum()
    axes[2].plot(times, batt_net, color="green", label="Battery Net (kWh)")
    axes[2].set_ylabel("kWh")
    axes[2].legend()

    grid_kw = (community_df["grid_bought_kwh"] - community_df["grid_sold_kwh"]) / dt
    axes[3].fill_between(times, grid_kw, 0, where=(grid_kw >= 0), color="tomato",        alpha=0.6, label="Bought")
    axes[3].fill_between(times, grid_kw, 0, where=(grid_kw < 0),  color="mediumseagreen", alpha=0.6, label="Sold")
    axes[3].axhline(0, color="black", linewidth=0.5)
    axes[3].set_ylabel("kW")
    axes[3].legend()

    axes[3].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    axes[3].xaxis.set_major_locator(mdates.HourLocator(interval=2))
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def plot_households(
    household_df: pd.DataFrame,
    household_ids: list[str],
    time_step_hours: float = 0.25,
) -> plt.Figure:
    times = _time_axis(household_df["time_step"].nunique(), time_step_hours)
    dt = time_step_hours
    n = len(household_ids)

    fig, axes = plt.subplots(4, n, figsize=(6 * n, 10), sharex=True, sharey="row")
    if n == 1:
        axes = [[ax] for ax in axes]   # keep 2-D indexing consistent

    fig.suptitle("Individual Households — 24-hour Overview", fontsize=13)
    row_labels = ["Solar (kW)", "Consumption (kW)", "Battery SoC (kWh)", "Grid Exchange (kW)"]

    for col, hid in enumerate(household_ids):
        hh = household_df[household_df["household_id"] == hid].sort_values("time_step")

        axes[0][col].plot(times, hh["solar_kwh"].values / dt, color="gold")
        axes[1][col].plot(times, hh["demand_kwh"].values / dt, color="steelblue")
        axes[2][col].plot(times, hh["battery_soc_kwh"].values, color="green")

        grid_kw = (hh["grid_bought_kwh"] - hh["grid_sold_kwh"]).values / dt
        axes[3][col].fill_between(times, grid_kw, 0, where=(grid_kw >= 0), color="tomato",        alpha=0.6)
        axes[3][col].fill_between(times, grid_kw, 0, where=(grid_kw < 0),  color="mediumseagreen", alpha=0.6)
        axes[3][col].axhline(0, color="black", linewidth=0.5)

        axes[0][col].set_title(f"Household {hid}")
        axes[3][col].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        axes[3][col].xaxis.set_major_locator(mdates.HourLocator(interval=4))

    for row, label in enumerate(row_labels):
        axes[row][0].set_ylabel(label)

    fig.autofmt_xdate()
    fig.tight_layout()
    return fig
