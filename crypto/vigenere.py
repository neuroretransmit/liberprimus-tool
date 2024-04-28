from crypto.gematria import RUNE_LOOKUP, PLAINTEXT
from crypto.keys import key_to_shifts

def vigenere(text, key=None, fast=True, skips=None, lookup=RUNE_LOOKUP, shift=0, excludes=None, key_index=0):
    plaintext = ''
    shifts = key_to_shifts(key)
    key_index = key_index
    if skips:
        skip_occurences = { k: 0 for k, v in skips.items() }
    if excludes:
        exclude_occurences = { k: 0 for k, v in excludes.items() }
    lookup_keys = list(lookup.keys())
    for c in text:
        shift = shifts[key_index % len(shifts)]
        if c in lookup:
            if skips and c in skips and len(skips[c]) > 0: #and skip_occurences[c] + 1 == skips[c][0]:
                skip_occurences[c] += 1
                if skip_occurences[c] == skips[c][0]:
                    if fast:
                        plaintext += lookup[c][PLAINTEXT][0]
                        skips[c] = skips[c][1:]
                        continue
                    else:
                        raise NotImplementedError("Permutations mode not implemented yet")
            elif excludes and c in excludes and len(excludes[c]) > 0:
                exclude_occurences[c] += 1
                if exclude_occurences[c] == excludes[c][0]:
                    if fast:
                        plaintext += lookup[c][PLAINTEXT][0]
                        excludes[c] = excludes[c][1:]
                        key_index += 1
                        continue
                    else:
                        raise NotImplementedError("Permutations mode not implemented yet")
            if fast:
                rune_lookup_key = lookup_keys[(lookup_keys.index(c) - shift) % len(lookup_keys)]
                plaintext += lookup[rune_lookup_key][PLAINTEXT][0]
            else:
                raise NotImplementedError("Permuatations mode not implemented yet")
            key_index += 1
        else:
            plaintext += c
    return plaintext

