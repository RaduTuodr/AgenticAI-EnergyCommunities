from CommunityData import *

excel_path = '../data/EC_EV_dataset (fixed error).xlsx'
community = CommunityData(excel_path)

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