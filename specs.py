from lp import get_pages
from gematria import RUNE_LOOKUP

class TextRetrievalSpec:
    def __init__(self, nums: list, mode=get_pages):
        """ The specification for how to retrieve text from Liber Primus
        @param num  the number of the part (page, segment, line, etc.)
        @param mode a function reference to the retrieval method
        """
        self.nums = nums
        self.mode = mode

    def retrieve(self):
        return self.mode(self.nums)

class CryptoSpec:
    def __init__(self, scheme, key=None, shift=0, lookup=RUNE_LOOKUP, skips=None, excludes=None):
        """ The specification for the cryptography to be performed
        @param scheme   The encryption scheme to use
        @param key      The key for the cipher
        @param shift    The shift value for lookups
        @param lookup   A dict of <rune->tuple of (list[char/bigram], gematria value)
        @param skips    A dict of <rune->occurence number> to use original unkeyed lookup, key index
                        doesn't increment and is continued on the next character.
        @param excludes A dict of <rune->occurence number> to use original unkeyed lookup, key index
                        does increment
        """
        self.scheme = scheme
        self.key = key
        self.shift = shift
        self.lookup = lookup
        self.skips = skips
        self.excludes = excludes

class SolutionSpec:
    def __init__(self, retrieval: TextRetrievalSpec, crypto: CryptoSpec, show_runes: bool = False):
        self.retrieval = retrieval
        self.crypto = crypto
        self.show_runes = show_runes
        # Used by ga.py (Genetic Algorithm)
        self.plaintext = None
        self.fitness = 0

    def run(self, silent=False):
        """ Generic cradle to run decryptions """
        for num, text in zip(self.retrieval.nums, self.retrieval.retrieve()):
            if not silent:
                # FIXME: This shouldn't always show PAGE, we can retrieve segments, etc.
                print(f"=== PAGE {num} ===")
            if not silent and self.show_runes:
                print(text)
                print("-----")
            if self.crypto.key:
                plaintext = self.crypto.scheme(text,
                                               key=self.crypto.key,
                                               shift=self.crypto.shift,
                                               lookup=self.crypto.lookup,
                                               skips=self.crypto.skips,
                                               excludes=self.crypto.excludes)
                if not silent:
                    print(plaintext)
                else:
                    self.plaintext = plaintext
            else:
                plaintext = self.crypto.scheme(text, lookup=self.crypto.lookup, shift=self.crypto.shift, skips=self.crypto.skips)
                if not silent:
                    print(plaintext)
                else:
                    self.plaintext = plaintext

    def rate(self):
        """ Rate the fitness of this spec's outcome """
        raise NotImplementedError("rate is not implemented")

    def random_attr(self):
        #match attr to new individual - TODO
        #return random.choice([attr, v for attr, v in vars(self).items()
        raise NotImplementedError("random_attr not implemented")

def random_spec():
    raise NotImplementedError("random_spec not implemented")

def random_specs():
    raise NotImplementedError("random spec not implemented")
