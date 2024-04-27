from util import find

def get_pages(pages):
    page_texts = []
    with open("./data/transcription.txt") as lp:
        text = lp.read()
        page_ends = list(find(text, '%'))
        for page in pages:
            page_texts.append(text[0 if page == 0 else page_ends[page-1]:page_ends[page]])
    return page_texts
