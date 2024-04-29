import functools

# For the following two functions see: https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties
def rsetattr(obj, attr, val):
    """ Recursive setattr for rule engine """
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    """ Recursive getattr for rule engine """
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))

# Use to get start/end of substrings within the Liber Primus for lexing
def find(haystack, needle):
    """ Find the start of all (possibly-overlapping) instances of needle in haystack """
    offs = -1
    while True:
        offs = haystack.find(needle, offs+1)
        if offs == -1:
            break
        else:
            yield offs

# Primarily used for arguments/validations - for example if you selected words and paragraphs
# This would be used to find how many words are in those paragraphs
def find_occurences(full_text, parent_entity, divider):
    """ Find the number of occurences of an entity within a parent (i.e. words in a paragraph)
    @param full_text     The full text to search
    @param parent_entity The parent entity to search
    @param divider       The part delimiter (see lp.py)
    """
    if divider not in "%/$&.-":
        raise ValueError("Invalid divider char, must be one of % / $ & . - (page, line, segment, paragraph, section, word)")
    lookup = {}
    last = None
    for entity in parent_entity:
        lookup[entity] = len(list(find(full_text[0 if not last else last:entity], divider)))
        last = entity
    return lookup

