import random
from util import rsetattr, rgetattr

class FSM:
    def __init__(self, states = dict()):
        self.states = states  # Dictionary to hold states and their transitions
        self.current_state = None

    def add_state(self, name, transitions):
        self.states[name] = transitions

    def set_state(self, state):
        self.current_state = state

    def transition(self, mutation_rate):
        transitions = []
        # Top-level {crypto, retrieval}
        for top_rule_k, top_rule_v in self.states.items():
            #path = [top_rule_k]
            if hasattr(self.current_state, top_rule_k) and getattr(self.current_state, top_rule_k) is not None:
                top_attr = getattr(self.current_state, top_rule_k)
                # Second-level {attrs of crypto, retrieval}
                for second_rule_k, second_rule_v in self.states[top_rule_k].items():
                    if second_rule_k == "scheme" and hasattr(top_attr, second_rule_k) and getattr(top_attr, second_rule_k) is not None:
                        scheme_callable = getattr(top_attr, second_rule_k)
                        name = getattr(scheme_callable, '__name__', 'Unknown')
                        attrs = second_rule_v[name]
                        exclude = []
                        include = []
                        for k, v in attrs.items():
                            if k == "$excludes":
                                for e in v:
                                    exclude.append(e)
                            elif k == "$includes":
                                for i in v:
                                    include.append(i)
                            else:
                                pass
                        if exclude != []:
                            for i in include:
                                if i not in exclude:
                                    for k, v in second_rule_v[i].items():
                                        transitions.append(('.'.join([top_rule_k, second_rule_k, k]), v))
                        else:
                            for i in include:
                                for k, v in second_rule_v[i].items():
                                    transitions.append(('.'.join([top_rule_k, second_rule_k, k]), v))

        for k, v in transitions:
            if random.random() < mutation_rate:
                print("Mutating:", k)
                rsetattr(self.current_state, k, v() 
                         if callable(v) 
                         else (v 
                               if not isinstance(v, dict) 
                               else {k1: v1() for k1, v1 in v.items()}))
                after = rgetattr(self.current_state, k)
                print(after)

