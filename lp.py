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
            if num < 0 or num >= len(ends):
                print(f"Warning: Entity index {num} is out of range.")
                texts.append("") 
            else:
                texts.append(text[0 if num == 0 else ends[num-1]:ends[num]])
    return texts

# TODO
def print_page_context(page_num, text):
    """ Print context information for a page """
    print(f"=== PAGE {page_num} CONTEXT ===")
    print("Imagery or context information goes here")
    print("===============================")
    print(text)

def print_section_context(page_num, segment_num, paragraph_num, sentence_num, word_num, text):
    print(f"=== PAGE {page_num}:SEGMENT {segment_num}:PARAGRAPH {paragraph_num};SENTENCE {sentence_num};WORD {word_num} CONTEXT ===")
    print("Imagery or context information goes here")
    print("===============================")
    print(text)

def get_pages(nums):
    return get_entities(nums, '%')

def get_segments(nums):
    return get_entities(nums, '$')

def get_paragraphs(nums):
    return get_entities(nums, '&')

def get_lines(nums):
    return get_entities(nums, '/')

def get_clauses(nums):
    return get_entities(nums, '.')
