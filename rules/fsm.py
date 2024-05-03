import random
from util import rsetattr, rgetattr
from args import get_transcription_validations

validations = get_transcription_validations()


class FSM:
    def __init__(self, states=dict()):
        self.states = states  # Dictionary to hold states and their transitions
        self.current_state = None

    def add_state(self, name, transitions):
        self.states[name] = transitions

    def set_state(self, state):
        self.current_state = state

    # FIXME: This is disgusting and the result of no sleep
    def transition(self, mutation_rate):
        transitions = []
        # Top-level {crypto, retrieval}
        for top_rule_k, top_rule_v in self.states.items():
            if (
                hasattr(self.current_state, top_rule_k)
                and getattr(self.current_state, top_rule_k) is not None
            ):
                top_attr = getattr(self.current_state, top_rule_k)
                # Second-level {attrs of crypto, retrieval}
                for second_rule_k, second_rule_v in self.states[top_rule_k].items():
                    # TODO: Scheme doesn't appear to mutate - fix this
                    # TODO continued: Calling random.getrandbits() will intermittently skip scheme to change the scheme
                    # FIXME for TODO continued: with above getrandbits(): need to setup parameters when this happens
                    if (
                        second_rule_k == "scheme"
                        and hasattr(top_attr, second_rule_k)
                        and getattr(top_attr, second_rule_k) is not None
                    ):
                        scheme_callable = getattr(top_attr, second_rule_k)
                        name = getattr(scheme_callable, "__name__", "Unknown")
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
                            elif k == "*":  # Common
                                for i in v:
                                    include.append(i)
                            else:
                                pass
                        if exclude != []:
                            for i in include:
                                if i not in exclude:
                                    for k, v in second_rule_v[i].items():
                                        transitions.append(
                                            (
                                                ".".join(
                                                    [top_rule_k, second_rule_k, k]
                                                ),
                                                v,
                                            )
                                        )
                        else:
                            for i in include:
                                for k, v in second_rule_v[i].items():
                                    transitions.append(
                                        (".".join([top_rule_k, second_rule_k, k]), v)
                                    )
                    else:
                        # FIXME: Need to setup retrieval.num
                        if top_rule_k == "retrieval" and second_rule_k == "nums":
                            mode_callable = getattr(top_attr, "mode")
                            name = getattr(mode_callable, "__name__", "Unknown")
                            if "pages" in name:
                                v = validations["pages"]["num"]
                            elif "sentences" in name:
                                v = validations["sentences"]["num"]
                            elif "clauses" in name:
                                v = validations["clauses"]["num"]
                            elif "paragraphs" in name:
                                v = validations["paragraphs"]["num"]
                            elif "lines" in name:
                                v = validations["lines"]["num"]
                            elif "segments" in name:
                                v = validations["segments"]["num"]
                            else:
                                raise NotImplementedError(
                                    f"found retrieval.mode callable that is not in FSM: {name}"
                                )
                            transitions.append(
                                (
                                    ".".join([top_rule_k, second_rule_k]),
                                    [random.randint(0, v)],
                                )
                            )
                        else:
                            transitions.append(
                                (".".join([top_rule_k, second_rule_k]), second_rule_v)
                            )

        for k, v in transitions:
            if random.random() < mutation_rate:
                if ".scheme." in k:
                    k = k.replace(".scheme", "")
                print("Mutating:", k)
                before = rgetattr(self.current_state, k)
                if callable(before):
                    before = getattr(before, "__name__", "Unknown")
                rsetattr(
                    self.current_state,
                    k,
                    (
                        v()
                        if callable(v)  # Call lambda/callable
                        else (
                            v
                            if not isinstance(v, dict)  # Non-dict value
                            else {k1: v1() for k1, v1 in v.items()}
                        )
                    ),
                )  # Call lambda/callable dict value
                after = rgetattr(self.current_state, k)
                if callable(after):
                    after = getattr(after, "__name__", "Unknown")
                print(f"FSM: {before}->{after}")
