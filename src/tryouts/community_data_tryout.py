from src.CommunityData import *
from src.config import EXCEL_DATASET_PATH

community = CommunityData(EXCEL_DATASET_PATH)

print(community.get_data(1))

#               consumption  solar_production  ev_consumption
# household_id
# 1                1.556923               0.0             0.0
# 2                0.326013               0.0             0.0
# 3                0.164274               0.0             0.0
# 4                0.414113               0.0             0.0
# 5                1.794511               0.0             0.0
# ...                   ...               ...             ...
# 246              0.169195               0.0             0.0
# 247              0.403638               0.0             0.0
# 248              0.506335               0.0             0.0
# 249              0.181176               0.0             0.0
# 250              0.142578               0.0             0.0
#
# [250 rows x 3 columns]

print(community.get_data("00:00 - 00:15"))

# Same output

print(community.get_data("00:00 - 00:15").loc["1", "consumption"])

# 1.556922571

battery_specs = community.get_battery_specs()
print(f"Total households with batteries: {len(battery_specs)} / 250")
print("Household 1 Battery Spec:", battery_specs.get("1"))

# Total households with batteries: 150 / 250
# Household 1 Battery Spec: {'model_id': 8, 'capacity': 6.4, 'max_charge': 2.0, 'max_discharge': 2.0, 'efficiency': 0.95, 'initial_charge': 3.2, 'final_charge': 3.2}