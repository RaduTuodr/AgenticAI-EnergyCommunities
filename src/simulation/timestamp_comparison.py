from src.CommunityData import CommunityData
from src.PrettyPrint import table_print
from src.config import EXCEL_DATASET_PATH
from src.simulation.core.controller import RuleBasedController
from src.simulation.main import run_simulation, compute_results, check_energy_balance

base_community = CommunityData(EXCEL_DATASET_PATH)
controller = RuleBasedController()

time_steps = [0.25, 0.5, 1.0]
results = []

for dt in time_steps:
    community = base_community.resample(dt)

    table = run_simulation(
        community_data=community,
        controller=controller,
        time_step_hours=dt,
        use_batteries=True,
        allow_sharing=True,
    )

    passed_check = check_energy_balance(table, tolerance=1e-3)
    print(f"  Energy balance  : {passed_check}")

    results.append((f"{int(dt * 60)} min", compute_results(table, time_step_hours=dt)))

table_print(results)
