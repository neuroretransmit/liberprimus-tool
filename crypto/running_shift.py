from crypto.gematria import RUNE_LOOKUP, PLAINTEXT


def running_shift(
    text, key=None, key_index=0, fast=True, lookup=RUNE_LOOKUP, skips=None, excludes=None, shift=0
):
    plaintext = ""
    lookup_keys = list(lookup.keys())
    key_index = key_index
    if skips:
        skip_occurences = {k: 0 for k, _ in skips.items()}
    for c in text:
        if c in lookup:
            if (
                skips and c in skips and len(skips[c]) > 0
            ):  # and skip_occurences[c] + 1 == skips[c][0]:
                skip_occurences[c] += 1
                if skip_occurences[c] == skips[c][0]:
                    if fast:
                        plaintext += lookup[c][PLAINTEXT][0]
                        skips[c] = skips[c][1:]
                        continue
                    else:
                        raise NotImplementedError(
                            "Permutations mode not implemented yet"
                        )
            if fast:
                rune_lookup_key = lookup_keys[
                    (lookup_keys.index(c) - key[key_index]) % len(lookup_keys)
                ]
                plaintext += lookup[rune_lookup_key][PLAINTEXT][0]
                key_index += 1
            else:
                raise NotImplementedError("Permutations mode not implemented yet")
        else:
            plaintext += c
    return plaintext
