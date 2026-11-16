class RuleBasedController:
    """
    Rule-based controller:
    - surplus (solar > demand), charge the battery.
    - deficit (demand > solar), discharge the battery.
    - EVs charge when the data says they charge.
    """
    @staticmethod
    def decide(solar_kw: float, demand_kw: float) -> tuple[float, float]:
        """
        Receives the current situation and returns (charge_kw, discharge_kw).
        """
        if solar_kw > demand_kw:
            return solar_kw - demand_kw, 0.0
        elif demand_kw > solar_kw:
            return 0.0, demand_kw - solar_kw
        return 0.0, 0.0
