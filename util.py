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

