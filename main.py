#!/usr/bin/env python3

import os

from args import parse_args
from lp import get_pages, get_segments
from crypto.gematria import direct_translation
from crypto.atbash import atbash, ATBASH
from crypto.rot import rot
from crypto.vigenere import vigenere
from crypto.running_shift import running_shift
from crypto.math import totients
from specs import SolutionSpec, CryptoSpec, TextRetrievalSpec
from ga import GeneticAlgorithm

SOLUTIONS = {
    0 : SolutionSpec(TextRetrievalSpec([0]), CryptoSpec(atbash, lookup=ATBASH)),
    # TODO: 2
    1 : SolutionSpec(TextRetrievalSpec([1]), CryptoSpec(vigenere, key="DIUINITY", skips={'ᚠ': [4, 5, 6, 7, 10, 11, 14]})),
    3 : SolutionSpec(TextRetrievalSpec([3]), CryptoSpec(direct_translation)),
    4 : SolutionSpec(TextRetrievalSpec([4]), CryptoSpec(rot, lookup=ATBASH, shift=3)),
    5 : SolutionSpec(TextRetrievalSpec([5]), CryptoSpec(rot, lookup=ATBASH, shift=3)),
    6 : SolutionSpec(TextRetrievalSpec([6]), CryptoSpec(rot, lookup=ATBASH, shift=3)),
    7 : SolutionSpec(TextRetrievalSpec([7]), CryptoSpec(rot, lookup=ATBASH, shift=3)),
    9 : SolutionSpec(TextRetrievalSpec([9]), CryptoSpec(direct_translation)),
    10: SolutionSpec(TextRetrievalSpec([10]), CryptoSpec(direct_translation)),
    11: SolutionSpec(TextRetrievalSpec([11]), CryptoSpec(direct_translation)),
    12: SolutionSpec(TextRetrievalSpec([5], mode=get_segments), CryptoSpec(vigenere,
                  key="FIRFUMFERENCE",
                  skips={'ᚠ': [2, 3]},
                  excludes={'ᛖ': [1, 2, 3, 5, 7],
                            'ᚻ': [3],
                            'ᚩ': [2, 4, 6],
                            'ᚪ': [6, 11, 17],
                            'ᚱ': [5, 11],
                            'ᚳ': [7],
                            'ᛠ': [8],
                            'ᚢ': [4, 6],
                            'ᛋ': [7],
                            'ᛗ': [11],
                            'ᛞ': [9, 11],
                            'ᛁ': [15],
                            'ᚷ': [6]})),
    # 13 - is part of section in text retrieval of 12
    14: SolutionSpec(TextRetrievalSpec([14]), CryptoSpec(direct_translation)),
    # TODO: 15-70
    71: SolutionSpec(TextRetrievalSpec([71]), CryptoSpec(running_shift,
                  key=totients(get_pages([71])[0]),
                  skips={'ᚠ': [4]})),
    72: SolutionSpec(TextRetrievalSpec([72]), CryptoSpec(direct_translation))
}

def ga():
    if not os.path.isfile("./solution_attempts.db"):
        raise RuntimeError("database not found, please run ./scripts/setup-db.sh")
    ga = GeneticAlgorithm(1, initial_pool=[SOLUTIONS[0], SOLUTIONS[1]])
    ga.evolve()

def known():
    """ Decrypt known pages """
    for spec in SOLUTIONS.values():
        spec.run()

def attempt_target():
    """ Attempt decryption on specified pieces of liber primus """
    print("ARGS:", target)
    if "ga" in target:
        ga()
    elif "pages" in target:
        page_texts = get_pages(target["pages"])
        for page, text in zip(target["pages"], page_texts):
            print(f"=== PAGE {page} ===")
            if target["runes"]:
                print(text)
                print("-----")
            # TODO: Implement cascading parts, i.e. words and paragraphs where the words are from
            #       from the specified paragraph
            # TODO: Implement ciphers as  arguments
    if "segments" in target:
        pass
    if "paragraphs" in target:
        pass
    if "words" in target:
        pass
    if "lines" in target:
        pass
    if "clause" in target:
        pass

if __name__ == "__main__":
    target = parse_args()
    if not target:
        known()
    else:
        attempt_target()
