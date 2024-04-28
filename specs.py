import copy
from lp import get_pages
from crypto.gematria import RUNE_LOOKUP
from crypto.vigenere import vigenere
from abc import ABC, abstractmethod
from lingua import Language, LanguageDetectorBuilder

LANGUAGES = [Language.ENGLISH, Language.LATIN]
DETECTOR = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()

class DNA(ABC):
    @abstractmethod
    def crossover(self, *args, **kwargs):
        pass

    @abstractmethod
    def mutate(self):
        pass

class TextRetrievalSpec(DNA):
    def __init__(self, nums: list, mode=get_pages):
        """ The specification for how to retrieve text from Liber Primus
        @param num  the number of the part (page, segment, line, etc.)
        @param mode a function reference to the retrieval method
        """
        self.nums = nums
        self.mode = mode

    def retrieve(self):
        return self.mode(self.nums)

    # TODO: Implement crossover
    def crossover(self, **entries):
        offspring = copy.deepcopy(self)
        text_retrieval_dict = self.__dict__
        for attr, v in entries.items():
            if attr == "mode":
                pass
            elif attr == "nums":
                pass
            else:
                continue
        offspring.__dict__.update(text_retrieval_dict)
        return offspring

    def mutate(self):
        pass

class CryptoSpec(DNA):
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

    # TODO: Implement crossover
    def crossover(self, **entries):
        offspring = copy.deepcopy(self)
        crypto_dict = self.__dict__
        for attr, v in entries.items():
            if attr == "scheme":
                pass
            elif attr == "scheme" and v == vigenere:
                if attr == "key" and v:
                    pass
                elif attr == "skips":
                    pass
                elif attr == "excludes":
                    pass
            elif attr == "shift":
                pass
            elif attr == "lookup":
                pass
        offspring.__dict__.update(crypto_dict)
        return offspring

    def mutate(self):
        pass

class SolutionSpec(DNA):
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
                    # TODO: Store list of plaintexts for multiple sections
                    self.plaintext = plaintext
            else:
                plaintext = self.crypto.scheme(text, lookup=self.crypto.lookup, shift=self.crypto.shift, skips=self.crypto.skips)
                if not silent:
                    print(plaintext)
                else:
                    # TODO: Store list of plaintexts for multiple sections
                    self.plaintext = plaintext

    def rate(self):
        """ Rate the fitness of this spec's outcome """
        self.run(silent=True)
        # TODO: Sanitize plaintext
        # TODO: Store list of confidences for multiple sections
        # TODO: Iterate overplaintext for multiple sections when implemented, see run()
        confidence = DETECTOR.compute_language_confidence_values(self.plaintext)
        self.fitness = confidence
        print("FITNESS:", self.fitness)

    def crossover(self, **entries):
        offspring = copy.deepcopy(self)
        solution_dict = self.__dict__
        for attr, v in entries.items():
            if attr in {"crypto", "retrieval"}:
                v.crossover(**entries[attr].__dict__)
                solution_dict[attr] = v
            else:
                continue
        offspring.__dict__.update(solution_dict)
        return offspring

    def mutate(self):
        pass

    def crossover(self, **kwargs):
        child = SolutionSpec()
        for key in self.__dict__:
            if random.random() < 0.5:
                setattr(child, key, self.__dict__[key])
            else:
                setattr(child, key, kwargs[key])
        return child

    def mutate(self):
        mutation_rate = 0.1  # Adjust this mutation rate
        for key in self.__dict__:
            if random.random() < mutation_rate:
                # Example of mutation: increment or decrement by a small random amount
                setattr(self, key, self.__dict__[key] + random.uniform(-0.1, 0.1))

def random_spec():
    raise NotImplementedError("random_spec not implemented")

def random_specs():
    raise NotImplementedError("random spec not implemented")
