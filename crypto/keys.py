from crypto.gematria import RUNE_LOOKUP, PLAINTEXT


def key_to_shifts(key, doubles=False, lookup=RUNE_LOOKUP):
    """Convert text key to shifts
    @key     Key as string to turn into lookup shifts
    @doubles Use double character lookups (i.e. use two letters for TH rather than the TH rune)
    @lookup  Rune lookup dict - can supply different orderings
    """
    # Preprocessing
    key = key.upper()

    if isinstance(key, str):
        lookup_vals = [v[PLAINTEXT] for v in lookup.values()]
        shifts = []
        for i, c in enumerate(key):
            lookup_idx = 0
            for v in lookup_vals:
                before = len(shifts)
                peek = key[i + 1] if i + 1 < len(key) and doubles else None
                for p in v:
                    if peek and c + peek == p:
                        shifts.append(lookup_idx)
                    elif c == p:
                        shifts.append(lookup_idx)
                    # FIXME: Hm, wtf was i doing
                    elif c == " ":
                        shifts.append(0)
                if before < len(shifts):
                    break
                lookup_idx += 1
        return shifts
    else:
        raise NotImplementedError("Keys of type other than string are not implemented")
