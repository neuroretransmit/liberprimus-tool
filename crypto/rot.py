from crypto.gematria import RUNE_LOOKUP, PLAINTEXT

def rot(text, shift=0, fast=True, lookup=RUNE_LOOKUP, skips=None):
    plaintext = ''
    lookup_keys = list(lookup.keys())
    for c in text:
        if c in lookup:
            if fast:
                rune_lookup_key = lookup_keys[(lookup_keys.index(c) - shift) % len(lookup_keys)]
                plaintext += lookup[rune_lookup_key][PLAINTEXT][0]
            else:
                raise NotImplementedError("Permutations mode not implemented yet")
        else:
            plaintext += c
    return plaintext

