import matplotlib.pyplot as plt

from src.CommunityData import CommunityData
from src.config import EXCEL_DATASET_PATH
from src.simulation.core.controller import RuleBasedController
from src.simulation.main import run_simulation
from src.plots.plot_day import plot_community, plot_households

HOUSEHOLDS_TO_PLOT = ["1", "2", "3"]   # adjust to any household IDs in your dataset
TIME_STEP = 0.25

community_data = CommunityData(EXCEL_DATASET_PATH)
controller = RuleBasedController()

community_df, household_df = run_simulation(
    community_data=community_data,
    controller=controller,
    time_step_hours=TIME_STEP,
    use_batteries=True,
    allow_sharing=True,
    track_households=True,
)

plot_community(community_df, time_step_hours=TIME_STEP)
plt.savefig("../../community_day.png", dpi=150)

plot_households(household_df, HOUSEHOLDS_TO_PLOT, time_step_hours=TIME_STEP)
plt.savefig("../../households_day.png", dpi=150)

plt.show()
