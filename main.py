#!/usr/bin/env python3

from args import parse_args
from lp import get_pages, get_sections
from gematria import direct_translation, atbash, vigenere, rot, running_shift, ATBASH, RUNE_LOOKUP
from math import  totients

class TextRetrievalSpec:
    def __init__(self, nums: list, mode=get_pages):
        """ The specification for how to retrieve text from Liber Primus
        @param num  the number of the part (page, segment, line, etc.)
        @param mode a function reference to the retrieval method
        """
        self.nums = nums
        self.mode = mode

    def retrieve(self):
        return self.mode(self.nums)

class CryptoSpec:
    def __init__(self, scheme, key=None, shift=0, lookup=RUNE_LOOKUP, skips=None, excludes=None):
        """ The specification for the cryptography to be performed
        @param scheme   The encryption scheme to use
        @param key      The key for the cipher
        @param shift    The shift value for lookups
        @param lookup   A dict of <rune->tuple of (list[char/bigram], gematria value)
        @param skips    A dict of <rune->occurence number> to use original unkeyed lookup, key index
                        doesn't increment and is continued on the next character.
        @param excludes A dict of <rune->occurence number> to use original unkeyed lookup, key index
                        does increment
        """
        self.scheme = scheme
        self.key = key
        self.shift = shift
        self.lookup = lookup
        self.skips = skips
        self.excludes = excludes

class SolutionSpec:
    def __init__(self, retrieval: TextRetrievalSpec, crypto: CryptoSpec, show_runes: bool = False):
        self.retrieval = retrieval
        self.crypto = crypto
        self.show_runes = show_runes

    def run(self):
        """ Generic cradle to run decryptions """
        for num, text in zip(self.retrieval.nums, self.retrieval.retrieve()):
            print(f"=== PAGE {num} ===")
            if self.show_runes:
                print(text)
                print("-----")
            if self.crypto.key:
                plaintext = self.crypto.scheme(text,
                                               key=self.crypto.key,
                                               shift=self.crypto.shift,
                                               lookup=self.crypto.lookup,
                                               skips=self.crypto.skips,
                                               excludes=self.crypto.excludes)
                print(plaintext)
            else:
                plaintext = self.crypto.scheme(text, lookup=self.crypto.lookup, shift=self.crypto.shift, skips=self.crypto.skips)
                print(plaintext)

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
    12: SolutionSpec(TextRetrievalSpec([5], mode=get_sections), CryptoSpec(vigenere,
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

def known():
    """ Decrypt known pages """
    for spec in SOLUTIONS.values():
        spec.run()

def attempt_target():
    """ Attempt decryption on specified pieces of liber primus """
    print(target)
    if "pages" in target:
        page_texts = get_pages(target["pages"])
        for page, text in zip(target["pages"], page_texts):
            print(f"=== PAGE {page} ===")
            if target["runes"]:
                print(text)
                print("-----")
            # TODO: Implement ciphers as arguments and call run_with_meta
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
