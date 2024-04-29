import copy
import random
from lp import get_pages
from crypto.gematria import RUNE_LOOKUP
from crypto.vigenere import vigenere
from abc import ABC, abstractmethod
from lingua import Language, LanguageDetectorBuilder

LANGUAGES = [Language.ENGLISH, Language.LATIN]
DETECTOR = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()

class DNA(ABC):
    crossover_rate = 0.1
    mutation_rate = .05

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
            if attr == "mode" and random.random() < self.crossover_rate:
                print("crossing over retrieval.mode")
                pass
            elif attr == "nums" and random.random() < self.crossover_rate:
                print("crossing over retrieval.nums")
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
            if attr == "scheme" and random.random() < self.crossover_rate:
                print("crossing over crypto.scheme")
                pass
            # TODO: Extract keyable schemes to variable that can be easily referenced
            elif attr == "scheme" and v in [vigenere] and random.random() < self.crossover_rate:
                if attr == "key" and v and random.random() < self.crossover_rate:
                    print("crossing over crypto.key")
                    pass
                elif attr == "skips" and random.random() < self.crossover_rate:
                    print("crossing over crypto.skips")
                    pass
                elif attr == "excludes" and random.random() < self.crossover_rate:
                    print("crossing over crypto.excludes")
                    pass
            elif attr == "shift" and random.random() < self.crossover_rate:
                print("crossing over crypto.shift")
                pass
            elif attr == "lookup" and random.random() < self.crossover_rate:
                print("crossing over crypto.lookup")
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
        self.fitness = {
            "eng": 0,
            "lat": 0
        }

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

    #def run(self, section_type="PAGE", silent=False):
    #    """ Generic cradle to run decryptions """
    #    plaintexts = []  # List to store decrypted texts for multiple sections
    #    for num, text in zip(self.retrieval.nums, self.retrieval.retrieve()):
    #        if not silent:
    #            print(f"=== {section_type} {num} ===")  # Prints the section type dynamically
    #        if not silent and self.show_runes:
    #            print(text)
    #            print("-----")
    #        if self.crypto.key:
    #            plaintext = self.crypto.scheme(text,
    #                                           key=self.crypto.key,
    #                                           shift=self.crypto.shift,
    #                                           lookup=self.crypto.lookup,
    #                                           skips=self.crypto.skips,
    #                                           excludes=self.crypto.excludes)
    #            if not silent:
    #                print(plaintext)
    #            else:
    #                plaintexts.append(plaintext)  # Adds the decrypted text to the list
    #        else:
    #            plaintext = self.crypto.scheme(text, lookup=self.crypto.lookup, shift=self.crypto.shift, skips=self.crypto.skips)
    #            if not silent:
    #                print(plaintext)
    #            else:
    #                plaintexts.append(plaintext)  # Adds the decrypted text to the list
    #    if silent:
    #        self.plaintext = plaintexts  # Stores decrypted texts for multiple sections


    def rate(self):
        """ Rate the fitness of this spec's outcome """
        self.run(silent=True)
        # TODO: Sanitize plaintext
        # TODO: Store list of confidences for multiple sections
        # TODO: Iterate overplaintext for multiple sections when implemented, see run()
        confidence = DETECTOR.compute_language_confidence_values(self.plaintext)
        self.fitness["eng"] = next(obj.value for obj in confidence if obj.language == Language.ENGLISH)
        self.fitness["lat"] = next(obj.value for obj in confidence if obj.language == Language.LATIN)
        print("FITNESS:", self.fitness)

    #def rate(self):
    #    """ Rate the fitness of this spec's outcome """
    #    self.run(silent=True)
        # TODO: Sanitize plaintext
        # Assuming you have a method sanitize_text() for sanitizing the plaintext
    #    sanitized_text = sanitize_text(self.plaintext)
        
        # TODO: Store list of confidences for multiple sections
    #    confidences = []
    #    for section_text in sanitized_text:
    #        confidence = DETECTOR.compute_language_confidence_values(section_text)
    #        confidences.append({
    #            "eng": next(obj.value for obj in confidence if obj.language == Language.ENGLISH),
    #            "lat": next(obj.value for obj in confidence if obj.language == Language.LATIN)
    #        })
        
        # TODO: Iterate over plaintext for multiple sections when implemented, see run()
    #    print("FITNESS:", confidences)
    #    return confidences


    def crossover(self, **entries):
        offspring = copy.deepcopy(self)
        solution_dict = self.__dict__
        for attr, v in entries.items():
            if attr in {"crypto", "retrieval"}:
                v.crossover(**entries[attr].__dict__)
                setattr(offspring, attr, v)
            else:
                continue
        #offspring.__dict__.update(solution_dict)
        return offspring

    def mutate(self):
        # FIXME: use wordlist for keys/exchange lookups
        pass

    # TODO: Use this implementation when FSM/rule engine are integrated, d4vi's is much better → I was thinking on something like this:
    #def crossover(self, **kwargs):
    #    child = SolutionSpec(
    #        retrieval=self.retrieval,
    #        crypto=self.crypto,
    #        show_runes=self.show_runes
    #    )
    #    for key in self.__dict__:
    #        if random.random() < 0.5:
    #            setattr(child, key, self.__dict__[key])
    #        else:
    #            setattr(child, key, kwargs[key])
    #    return child

    #def mutate(self):
    #    mutation_rate = 0.1  # Adjust this mutation rate
    #    offspring = copy.deepcopy(self)
    #    for key in self.__dict__:
    #        if random.random() < mutation_rate:
    #             Example of mutation: increment or decrement by a small random amount
    #            setattr(offspring, key, offspring.__dict__[key] + random.uniform(-0.1, 0.1))
    #    return offspring

def random_spec():
    raise NotImplementedError("random_spec not implemented")

def random_specs():
    raise NotImplementedError("random spec not implemented")
