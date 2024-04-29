import random

class RuleEngine:
    def __init__(self, fsm):
        self.fsm = fsm

    def mutate_parameters(self, parameters):
        possible_transitions = self.fsm.get_possible_transitions()
        if not possible_transitions:
            raise ValueError("No transitions available in the current state")

        # Select a random parameter to mutate
        parameter_to_mutate = random.choice(possible_transitions)

        # Mutate the selected parameter (example: increment by 1)
        parameters[parameter_to_mutate] += 1

        return parameters
