from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd


Timestamp = Union[int, str]


class CommunityData:
    _SHEETS = {
        "consumption": "Load",
        "solar_production": "PV",
        "ev1_consumption": "EV1 Load",
        "ev2_consumption": "EV2 Load",
    }

    def __init__(self, workbook_path: str | Path):
        self.__workbook_path = Path(workbook_path)
        self._data = self._load_data()

    def get_data(self, timestamp: Timestamp) -> pd.DataFrame:
        """
        description: Return consumption, solar production, and EV consumption per household.
        params: timestamp can be a 1-based interval number (1-96), or an interval label such as ``"08:30 - 08:45".
        """
        row_index = self._timestamp_to_index(timestamp)
        result = pd.DataFrame(
            {
                name: frame.iloc[row_index].to_numpy()
                for name, frame in self._data.items()
            },
            index=self._household_ids,
        )
        result["ev_consumption"] = (result["ev1_consumption"] + result["ev2_consumption"])
        return result[
            ["consumption", "solar_production", "ev_consumption"]
        ].rename_axis("household_id")

    def _load_data(self) -> dict[str, pd.DataFrame]:
        sheets = {
            name: pd.read_excel(self.__workbook_path, sheet_name=sheet)
            for name, sheet in self._SHEETS.items()
        }

        household_ids = sheets["consumption"].columns[1:]
        expected_rows = len(sheets["consumption"])
        if any(
            not household_ids.equals(frame.columns[1:])
            or len(frame) != expected_rows
            for frame in sheets.values()
        ):
            raise ValueError("Energy sheets must have matching household columns and rows")

        self._household_ids = household_ids.map(str)
        return {
            name: frame.iloc[:, 1:].set_axis(self._household_ids, axis=1)
            for name, frame in sheets.items()
        }

    def _timestamp_to_index(self, timestamp: Timestamp) -> int:
        if isinstance(timestamp, int):
            if 1 <= timestamp <= len(next(iter(self._data.values()))):
                return timestamp - 1
            raise IndexError(f"Timestamp must be between 1 and {len(next(iter(self._data.values())))}")

        if isinstance(timestamp, str):
            interval = timestamp.strip()
            if interval in self._interval_labels():
                return self._interval_labels().index(interval)

        raise ValueError("Timestamp must be a 1-based interval number or an interval label such as '08:30 - 08:45'")

    @staticmethod
    def _interval_labels() -> list[str]:
        return [
            f"{minutes // 60:02d}:{minutes % 60:02d} - "
            f"{(minutes + 15) // 60:02d}:{(minutes + 15) % 60:02d}"
            for minutes in range(0, 24 * 60, 15)
        ]
