from enum import Enum

PLAINTEXT = 0
VALUE = 1
RUNE_LOOKUP = {
    "ᚠ": (["F"], 2),
    "ᚢ": (["U"], 3),
    "ᚦ": (["TH"], 5),
    "ᚩ": (["O"], 7),
    "ᚱ": (["R"], 11),
    "ᚳ": (["C", "K"], 13),
    "ᚷ": (["G"], 17),
    "ᚹ": (["W"], 19),
    "ᚻ": (["H"], 23),
    "ᚾ": (["N"], 29),
    "ᛁ": (["I"], 31),
    "ᛄ": (["J"], 37),
    "ᛇ": (["EO"], 41),
    "ᛈ": (["P"], 43),
    "ᛉ": (["X"], 47),
    "ᛋ": (["S", "Z"], 53),
    "ᛏ": (["T"], 59),
    "ᛒ": (["B"], 61),
    "ᛖ": (["E"], 67),
    "ᛗ": (["M"], 71),
    "ᛚ": (["L"], 73),
    "ᛝ": (["NG", "ING"], 79),
    "ᛟ": (["OE"], 83),
    "ᛞ": (["D"], 89),
    "ᚪ": (["A"], 97),
    "ᚫ": (["AE"], 101),
    "ᚣ": (["Y"], 103),
    "ᛡ": (["IA", "IO"], 107),
    "ᛠ": (["EA"], 109),
}


def direct_translation(
    text, fast=True, skips=None, excludes=None, lookup=RUNE_LOOKUP, shift=0
):
    plaintext = ""
    for c in text:
        if fast:
            plaintext += lookup[c][PLAINTEXT][0] if c in lookup else c
        else:
            raise NotImplementedError("Permuatations mode not implemented yet")
    return plaintext
