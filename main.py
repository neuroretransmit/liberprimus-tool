#!/usr/bin/env python3

from args import parse_args
from lp import get_pages
from gematria import direct_translation, atbash, vigenere, rot, ATBASH

# Delimiters
# Word     : -
# Clause   : .
# Paragraph: &
# Segment  : $
# Chapter  : §
# Line     : /
# Page     : %

def run_with_meta(pages, method, key=None, show_runes=False, lookup=None, overrides=None, shift=0):
    page_texts = get_pages(pages)
    for page, text in zip(pages, page_texts):
        print(f"=== PAGE {page} ===")
        if show_runes:
            print(text)
            print("-----")
        if key:
            print(method(text, key, overrides=overrides, lookup=lookup, shift=shift))
        else:
            print(method(text, overrides=overrides, lookup=lookup, shift=shift))

def known():
    """ Decrypt known pages """
    atbash_pages = [0]
    run_with_meta(atbash_pages, atbash)
    vigenere_pages = [1]
    run_with_meta(vigenere_pages, vigenere, key="DIUINITY", show_runes=True, overrides={'ᚠ': [4, 5, 6, 7, 10, 11, 14]})
    atbash_rot3_pages = [4, 5, 6, 7]
    run_with_meta(atbash_rot3_pages, rot, shift=3, show_runes=True, lookup=ATBASH)
    unencrypted_pages = [3, 9, 10, 11, 14, 72]
    run_with_meta(unencrypted_pages, direct_translation)

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
