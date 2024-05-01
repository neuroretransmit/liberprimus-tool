#!/usr/bin/env python3

import os

from args import parse_args
from lp import get_pages, get_segments
from crypto.gematria import direct_translation, RUNE_LOOKUP
from crypto.atbash import atbash, ATBASH
from crypto.rot import rot
from crypto.vigenere import vigenere
from crypto.running_shift import running_shift
from crypto.math import totients
from specs import SolutionSpec, CryptoSpec, TextRetrievalSpec
from ga import GeneticAlgorithm

SOLUTIONS = {
    0 : SolutionSpec(TextRetrievalSpec([0]), CryptoSpec(atbash, lookup=ATBASH)),
    1 : SolutionSpec(TextRetrievalSpec([1]), CryptoSpec(vigenere, key="DIUINITY", skips={'ᚠ': [4, 5, 6, 7, 10, 11, 14]})),
    # TODO: 2
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
    72: SolutionSpec(TextRetrievalSpec([72]), CryptoSpec(direct_translation)),
}

# + [13] since 12 and 13 are solved by segment 5 and include both in that segment
# so it is not technically listed in the dict
KNOWN_PAGES = list(SOLUTIONS.keys()) + [13]

def ga():
    # Run infinitely by going over 1
    ga = GeneticAlgorithm(1.1, initial_pool=[SOLUTIONS[0], SOLUTIONS[1]])
    ga.evolve()

def known(page=None):
    """ Decrypt known pages """
    if page is None:  # Quando nenhum argumento --pages for passado
        for v in SOLUTIONS.values():
            v.run()
    else:  # Quando o argumento --pages for passado
        # A parte original do known() vai aqui
        if page in KNOWN_PAGES:
            if page == 12 or page == 13:
                SOLUTIONS[12].run()
            else:
                SOLUTIONS[page].run()

def translate_page(text, page):
    """Traduz a página de acordo com o mapeamento de página"""
    if page in KNOWN_PAGES:
        known(page)
    else:
        print("Translation not available for this page.")


# mapping pages for the correspondent traduce functions
PAGE_TRANSLATIONS = {
    0: direct_translation,
    1: vigenere,
    3: direct_translation,
    4: rot,
    5: rot,
    6: rot,
    7: rot,
    9: direct_translation,
    10: direct_translation,
    11: direct_translation,
    12: vigenere,
    14: direct_translation,
    71: running_shift,
    72: direct_translation,
}


def attempt_target():
    """ Tentativa de decifrar partes especificadas do Liber Primus """
    if "pages" in target:
        page_texts = get_pages(target["pages"])
        for page, text in zip(target["pages"], page_texts):
            if "runes" in target and target["runes"]:
                print(text)
            else:
                translate_page(text, page)
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
    else:
        if not target:
            for page in PAGE_TRANSLATIONS:
                known(page)


if __name__ == "__main__":
    target = parse_args()
    if not target:
        known()
    elif "ga" in target:
        ga()
    else:
        attempt_target()
