from util import find

# Delimiters
# Word     : -
# Clause   : .
# Paragraph: &
# Segment  : $
# Chapter  : §
# Line     : /
# Page     : %

def get_entities(nums, delimiter):
    texts = []
    with open("./data/transcription.txt") as lp:
        text = lp.read()
        ends = list(find(text, delimiter))
        for num in nums:
            texts.append(text[0 if num == 0 else ends[num-1]:ends[num]])
    return texts

def get_pages(nums):
    return get_entities(nums, '%')

def get_segments(nums):
    return get_entities(nums, '$')
