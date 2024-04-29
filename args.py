import argparse
from util import find, find_occurences

def get_transcription_validations():
    with open("./data/transcription.txt", "r", encoding="utf-8") as lp:
        text = lp.read()
        pages = list(find(text, '%'))
        segments = list(find(text, '$'))
        segments_per_page = find_occurences(text, pages, '$')
        paragraphs = list(find(text, '&'))
        paragraphs_per_page = find_occurences(text, pages, '&')
        paragraphs_per_segment = find_occurences(text, segments, '&')
        clauses = list(find(text, '.'))
        clauses_per_page = find_occurences(text, pages, '.')
        clauses_per_segment = find_occurences(text, segments, '.')
        clauses_per_paragraph= find_occurences(text, paragraphs, '.')
        lines = list(find(text, '/'))
        lines_per_page = find_occurences(text, pages, '/')
        lines_per_paragraph = find_occurences(text, paragraphs, '/')
        lines_per_clause = find_occurences(text, clauses, '/')
        lines_per_segment = find_occurences(text, segments, '/')
        words = list(find(text, '-'))
        words_per_page = find_occurences(text, pages, '-')
        words_per_paragraph = find_occurences(text, paragraphs, '-')
        words_per_clause = find_occurences(text, clauses, '-')
        words_per_segment = find_occurences(text, segments, '-')
        words_per_line = find_occurences(text, lines, '-')
        return {
            "pages": {
                "num": len(pages),
            },
            "segments": {
                "num": len(segments),
                "per_page": segments_per_page,
            },
            "paragraphs": {
                "num": len(paragraphs),
                "per_page": paragraphs_per_page,
                "per_segment": paragraphs_per_segment
            },
            "clauses": {
                "num": len(clauses),
                "per_page": clauses_per_page,
                "per_segment": clauses_per_segment,
                "per_paragraph": clauses_per_paragraph
            },
            "lines": {
                "num": len(lines),
                "per_page": lines_per_page,
                "per_segment": lines_per_segment,
                "per_clause": lines_per_clause,
                "per_paragraph": lines_per_paragraph,
            },
            "words": {
                "num": len(words),
                "per_page": words_per_page,
                "per_segment": words_per_segment,
                "per_clause": words_per_clause,
                "per_paragraph": words_per_paragraph,
                "per_line": words_per_line
            }
        }

def parse_args():
    parser = argparse.ArgumentParser(description="Options for Liber Primus Tool")
    parser.add_argument('--pages', nargs='+', type=int)
    parser.add_argument('--lines', nargs='+', type=int)
    parser.add_argument('--segments', nargs='+', type=int)
    parser.add_argument('--paragraphs', nargs='+', type=int)
    parser.add_argument('--clauses', nargs='+', type=int)
    parser.add_argument('--words', nargs='+', type=int)
    parser.add_argument('--runes', action=argparse.BooleanOptionalAction)
    parser.add_argument('--ga', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    validations = get_transcription_validations()
    target = {}

    # TODO: Finite state machine if multiple selected to validate through dict
    if args.ga:
        target["ga"] = args.ga
    if args.pages:
        pages = set(args.pages)
        if len(pages) > 0 and len(pages - set(range(0, validations["pages"]["num"]))) > 0:
            raise ValueError(f"Pages must be in range of 0-{validations['pages']['num']}")
        target["pages"] = pages
    if args.lines:
        lines = set(args.lines)
        if len(lines) > 0 and len(lines - set(range(0, validations["lines"]["num"]))) > 0:
            raise ValueError(f"Lines must be in range of 0-{validations['lines']['num']}")
        target["lines"] = lines
    if args.segments:
        segments = set(args.segments)
        if len(segments) > 0 and len(segments - set(range(0, validations["segments"]["num"]))) > 0:
            raise ValueError(f"Lines must be in range of 0-{validations['segments']['num']}")
        target["segments"] = segments
    if args.paragraphs:
        paragraphs = set(args.paragraphs)
        if len(paragraphs) > 0 and len(paragraphs - set(range(0, validations["paragraphs"]["num"]))) > 0:
            raise ValueError(f"Paragraphs must be in range of 0-{validations['paragraphs']['num']}")
        target["paragraphs"] = paragraphs
    if args.clauses:
        clauses = set(args.clauses)
        if len(clauses) > 0 and len(clauses - set(range(0, validations["clauses"]["num"]))) > 0:
            raise ValueError(f"Clauses must be in range of 0-{validations['clauses']['num']}")
        target["clauses"] = clauses
    if args.words:
        words = set(args.words)
        if len(words) > 0 and len(words - set(range(0, validations["words"]["num"]))) > 0:
            raise ValueError(f"Words must be in range of 0-{validations['words']['num']}")
        target["words"] = words
    if args.runes:
        target["runes"] = args.runes

    return target

