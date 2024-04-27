#!/usr/bin/env python3

from args import parse_args
from lp import get_pages, get_sections
from gematria import direct_translation, atbash, vigenere, rot, running_shift, ATBASH, RUNE_LOOKUP
from util import totients

# Delimiters
# Word     : -
# Clause   : .
# Paragraph: &
# Segment  : $
# Chapter  : §
# Line     : /
# Page     : %

def run_with_meta(nums, method, show_runes=False, text_retrieval=get_pages, key=None, 
                  lookup=RUNE_LOOKUP, overrides=None, shift=0, excludes=None):
    """ Generic cradle to run decryptions """
    texts = text_retrieval(nums)
    for num, text in zip(nums, texts):
        print(f"=== PAGE {num} ===")
        if show_runes:
            print(text)
            print("-----")
        if key:
            plaintext = method(text, key=key, overrides=overrides, lookup=lookup, shift=shift, excludes=excludes)
            print(plaintext)
        else:
            print(method(text, overrides=overrides, lookup=lookup, shift=shift))

def known():
    """ Decrypt known pages """
    atbash_pages = [0]
    run_with_meta(atbash_pages,
                  atbash,
                  lookup=ATBASH)
    vigenere_divinity_pages = [1]
    vigenere_firfumference_sections = [5] # pages 12, 13
    run_with_meta(vigenere_divinity_pages,
                  vigenere,
                  key="DIUINITY",
                  overrides={'ᚠ': [4, 5, 6, 7, 10, 11, 14]})
    run_with_meta(vigenere_firfumference_sections,
                  vigenere,
                  text_retrieval=get_sections,
                  key="FIRFUMFERENCE",
                  overrides={'ᚠ': [2, 3]},
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
                            'ᚷ': [6]})
    atbash_rot3_pages = [4, 5, 6, 7]
    run_with_meta(atbash_rot3_pages,
                  rot,
                  shift=3,
                  lookup=ATBASH)
    unencrypted_pages = [3, 9, 10, 11, 14, 72]
    run_with_meta(unencrypted_pages,
                  direct_translation)
    running_totient_shift_pages = [71]
    run_with_meta(running_totient_shift_pages,
                  running_shift,
                  key=totients(get_pages(running_totient_shift_pages)[0]),
                  overrides={'ᚠ': [4]})

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
