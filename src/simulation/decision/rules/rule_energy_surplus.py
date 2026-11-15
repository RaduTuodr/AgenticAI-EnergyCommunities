from src.simulation.core.state import State


class RuleEnergySurplus:
    @staticmethod
    def evaluate(state: State) -> bool:
        return State.snapshot[state.household_id]["consumption"] > 0.0
