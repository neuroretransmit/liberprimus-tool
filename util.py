def find(haystack, needle):
    """
    Find the start of all (possibly-overlapping) instances of needle in haystack
    """
    offs = -1
    while True:
        offs = haystack.find(needle, offs+1)
        if offs == -1:
            break
        else:
            yield offs

def find_occurences(full_text, parent_entity, divider_char):
    if divider_char not in "%/$&.-":
        raise ValueError("Invalid divider char, must be one of % / $ & . - (page, line, segment, paragraph, section, word)")
    lookup = {}
    last = None
    for entity in parent_entity:
        lookup[entity] = len(list(find(full_text[0 if not last else last:entity], divider_char)))
        last = entity
    return lookup

def gen_primes():
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1

def totients(data):
    return [p - 1 for i, p in zip(range(len(data)), gen_primes())]

