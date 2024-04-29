#!/usr/bin/env python3

import random

from specs import SolutionSpec, TextRetrievalSpec, CryptoSpec
from rules.fsm import FSM
from crypto.vigenere import vigenere
from crypto.atbash import ATBASH, RUNE_LOOKUP
from lp import get_pages, get_segments

if __name__ == "__main__":
    state_transitions = {
        "crypto": {
            # We can define all rule transitions for crypto based on scheme
            "scheme": {
                "vigenere": {
                    "$includes": ["$keyed", "*"]
                },
                "running_shift": {
                    "$includes": ["$keyed", "*"],
                    "$excludes": ["$keyed.key"],
                    "key": lambda: [random.sample(range(-29, 29), random.randint(0, 10))]
                },
                "atbash": {
                    "$includes": ["*"]
                },
                "rot": {
                    "$includes": ["*"]
                },
                # Attrs prepended with $ should be referenced by their appropriate types
                "$keyed": {
                    # TODO: Will pick from wordlist in future
                    "key": "MUTATED",
                    "excludes": {'a': lambda: random.randint(0, 10), 'b': lambda: random.randint(0, 10)},
                    "skips": {},
                    "key_index": lambda: random.randint(0, len("MUTATED") - 1)
                },
                # * denotes common attributes referenced in all
                "*": {
                    "lookup": lambda: random.choice([ATBASH, RUNE_LOOKUP]), # Should probably create random lookups too
                    "shift": lambda: random.randint(-29, 29)
                }
            }
        },
        "retrieval": {
            "mode": lambda: random.choice([get_pages, get_segments]),
            # TODO: nums - using tooling in argument validations to pull valid ranges
        }
    }

    crypto = CryptoSpec(vigenere, key="TEST")
    retrieval = TextRetrievalSpec([0])
    spec = SolutionSpec(retrieval, crypto)

    fsm = FSM(states=state_transitions)
    fsm.set_state(spec)
    fsm.transition(0.1)
