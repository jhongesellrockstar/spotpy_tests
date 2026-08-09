"""Conceptual setup contract. Activate only after paths and file semantics are verified."""
class SwatPlusSetupPrototype:
    def __init__(self, message="Configure verified SWAT+ project first"): self.message=message
    def simulation(self, vector): raise RuntimeError(self.message)
    def evaluation(self): raise RuntimeError(self.message)
    def objectivefunction(self, simulation, evaluation, params=None): raise RuntimeError(self.message)
