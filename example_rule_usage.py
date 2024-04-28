#!/usr/bin/env python3

from rules.fsm import FSM
from rules.engine import RuleEngine

# Example usage
if __name__ == "__main__":
    # Initialize the FSM
    fsm = FSM()

    # Add states and transitions to the FSM
    states_transitions = {
        "State1": ["Parameter1", "Parameter2"],
        "State2": ["Parameter2", "Parameter3"],
        # Add more states and transitions as needed
    }
    for state, transitions in states_transitions.items():
        fsm.add_state(state, transitions)

    # Set the initial state of the FSM
    fsm.set_state("State1")

    # Example parameters
    initial_parameters = {"Parameter1": 10, "Parameter2": 20, "Parameter3": 30}

    # Initialize the rule engine with the FSM
    rule_engine = RuleEngine(fsm)

    # Mutate the parameters based on the current state
    mutated_parameters = rule_engine.mutate_parameters(initial_parameters)

    print("Mutated parameters:", mutated_parameters)
