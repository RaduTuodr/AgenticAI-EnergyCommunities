from pandas import DataFrame
from dataclasses import dataclass
from src.CommunityData import Timestamp

@dataclass
class State:
    timestamp: Timestamp
    household_id: int
    snapshot: DataFrame
