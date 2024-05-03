from crypto.gematria import RUNE_LOOKUP, PLAINTEXT

ATBASH = {k: v for k, v in zip(RUNE_LOOKUP.keys(), reversed(RUNE_LOOKUP.values()))}


def atbash(text, fast=True, skips=None, lookup=ATBASH, shift=0):
    plaintext = ""
    for c in text:
        if fast:
            plaintext += lookup[c][PLAINTEXT][0] if c in lookup else c
        else:
            raise NotImplementedError("Permuatations mode not implemented yet")
    return plaintext
