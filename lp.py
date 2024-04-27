from util import find

def get_pages(pages):
    page_texts = []
    with open("./data/transcription.txt") as lp:
        text = lp.read()
        page_ends = list(find(text, '%'))
        for page in pages:
            page_texts.append(text[0 if page == 0 else page_ends[page-1]:page_ends[page]])
    return page_texts

def get_sections(nums):
    section_texts = []
    with open("./data/transcription.txt") as lp:
        text = lp.read()
        section_ends = list(find(text, '$'))
        for section in nums:
            section_texts.append(text[0 if section == 0 else section_ends[section-1]:section_ends[section]])
    return section_texts
