from enum import Enum

PLAINTEXT = 0
VALUE = 1
RUNE_LOOKUP = {
    'ᚠ': (['F'],           2),
    'ᚢ': (['U'],           3),
    'ᚦ': (['TH'],          5),
    'ᚩ': (['O'],           7),
    'ᚱ': (['R'],          11),
    'ᚳ': (['C', 'K'],     13),
    'ᚷ': (['G'],          17),
    'ᚹ': (['W'],          19),
    'ᚻ': (['H'],          23),
    'ᚾ': (['N'],          29),
    'ᛁ': (['I'],          31),
    'ᛄ': (['J'],          37),
    'ᛇ': (['EO'],         41),
    'ᛈ': (['P'],          43),
    'ᛉ': (['X'],          47),
    'ᛋ': (['S', 'Z'],     53),
    'ᛏ': (['T'],          59),
    'ᛒ': (['B'],          61),
    'ᛖ': (['E'],          67),
    'ᛗ': (['M'],          71),
    'ᛚ': (['L'],          73),
    'ᛝ': (['NG', 'ING'],  79),
    'ᛟ': (['OE'],         83),
    'ᛞ': (['D'],          89),
    'ᚪ': (['A'],          97),
    'ᚫ': (['AE'],        101),
    'ᚣ': (['Y'],         103),
    'ᛡ': (['IA', 'IO'],  107),
    'ᛠ': (['EA'],        109),
}

ATBASH = { k: v for k, v in zip(RUNE_LOOKUP.keys(), reversed(RUNE_LOOKUP.values()))}

def key_to_shifts(key, doubles=False, lookup=RUNE_LOOKUP):
    """ Convert text key to shifts
    @key     Key as string to turn into lookup shifts
    @doubles Use double character lookups (i.e. use two letters for TH rather than the TH rune)
    @lookup  Rune lookup dict - can supply different orderings
    """
    if isinstance(key, str):
        lookup_vals = [v[PLAINTEXT] for v in lookup.values()]
        shifts = []
        for i, c in enumerate(key):
            lookup_idx = 0
            for v in lookup_vals:
                before = len(shifts)
                peek = key[i+1] if i + 1 < len(key) and doubles else None
                for p in v:
                    if peek and c + peek == p:
                        shifts.append(lookup_idx)
                    elif c == p:
                        shifts.append(lookup_idx)
                    # FIXME: Hm, wtf was i doing
                    elif c == ' ':
                        shifts.append(0)
                if before < len(shifts):
                    break
                lookup_idx += 1
        return shifts

def direct_translation(text, fast=True, skips=None, excludes=None, lookup=RUNE_LOOKUP, shift=0):
    plaintext = ''
    for c in text:
        if fast:
            plaintext += lookup[c][PLAINTEXT][0] if c in lookup else c
        else:
            raise NotImplementedError("Permuatations mode not implemented yet")
    return plaintext

def atbash(text, fast=True, skips=None, lookup=ATBASH, shift=0):
    plaintext = ''
    for c in text:
        if fast:
            plaintext += lookup[c][PLAINTEXT][0] if c in lookup else c
        else:
            raise NotImplementedError("Permuatations mode not implemented yet")
    return plaintext

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

def running_shift(text, key=None, fast=True, lookup=RUNE_LOOKUP, skips=None, excludes=None, shift=0):
    plaintext = ''
    lookup_keys = list(lookup.keys())
    key_index = 0
    if skips:
        skip_occurences = {k: 0 for k, _ in skips.items()}
    for c in text:
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
            if fast:
                rune_lookup_key = lookup_keys[(lookup_keys.index(c) - key[key_index]) % len(lookup_keys)]
                plaintext += lookup[rune_lookup_key][PLAINTEXT][0]
                key_index += 1
            else:
                raise NotImplementedError("Permutations mode not implemented yet")
        else:
            plaintext += c
    return plaintext


