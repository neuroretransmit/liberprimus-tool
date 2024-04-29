class FSM:
    def __init__(self, states = dict()):
        self.states = states  # Dictionary to hold states and their transitions
        self.current_state = None

    def add_state(self, name, transitions):
        self.states[name] = transitions

    def set_state(self, name):
        if name in self.states:
            self.current_state = name
        else:
            raise ValueError("Invalid state")

    def get_possible_transitions(self):
        if self.current_state is None:
            return []
        else:
            return self.states[self.current_state]
