import copy
import random
from functools import reduce
from lp import get_pages, get_segments, get_paragraphs, get_lines, get_clauses
from rules.fsm import FSM
from crypto.gematria import RUNE_LOOKUP
from crypto.vigenere import vigenere
from crypto.atbash import ATBASH
from args import get_transcription_validations
from abc import ABC, abstractmethod
from lingua import Language, LanguageDetectorBuilder

LANGUAGES = [Language.ENGLISH, Language.LATIN]
DETECTOR = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()

# TODO: Make use of in state transitions when mode is changed for retrieval
transcription_validations = get_transcription_validations()

state_transitions = {
    "crypto": {
        # We can define all rule transitions for crypto based on scheme
        "scheme": {
            "vigenere": {
                "$includes": ["$keyed", "*"]
            },
            "running_shift": {
                "$includes": ["$keyed", "*"],
                "$excludes": ["$keyed.key"],
                "key": lambda: [random.sample(range(-29, 29), random.randint(0, 10))]
            },
            "atbash": {
                "$includes": ["*"]
            },
            "rot": {
                "$includes": ["*"]
            },
            # Attrs prepended with $ should be referenced by their appropriate types
            "$keyed": {
                # TODO: Will pick from wordlist in future
                "key": lambda: random.choice(["DIUINITY", "WELCOMEPILGRIM", "FIRFUMFERENCE"]),
                "excludes": {'a': lambda: random.randint(0, 10), 'b': lambda: random.randint(0, 10)},
                "skips": {},
                # TODO: Needs to be modified out of dict to lookup the key in use
                "key_index": lambda: random.randint(0, len("MUTATED") - 1)
            },
            # * denotes common attributes referenced in all
            "*": {
                "lookup": lambda: random.choice([ATBASH, RUNE_LOOKUP]), # Should probably create random lookups too
                "shift": lambda: random.randint(-29, 29)
            }
        }
    },
    "retrieval": {
        "mode": lambda: random.choice([get_pages, get_segments, get_paragraphs, get_lines, get_clauses]),
        # TODO: nums - using tooling in argument validations to pull valid ranges
        "nums": [0]
    }
}

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
        self.fsm = FSM(states=state_transitions)

    def run(self, silent=False):
        """ Generic cradle to run decryptions """
        plaintexts = []
        for num, text in zip(self.retrieval.nums, self.retrieval.retrieve()):
            if not silent:
                # FIXME: This shouldn't always show PAGE, we can retrieve segments, etc.
                name = getattr(self.retrieval.mode, '__name__', 'Unknown')
                name = name[:-1].replace("get_", "").upper()
                print(f"=== {name} {num} ===")
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
                    plaintexts.append(plaintext)
            else:
                plaintext = self.crypto.scheme(text, lookup=self.crypto.lookup, shift=self.crypto.shift, skips=self.crypto.skips)
                if not silent:
                    print(plaintext)
                else:
                    plaintexts.append(plaintext)
        if silent:
            self.plaintext = plaintexts

    def rate(self):
        """ Rate the fitness of this spec's outcome """
        self.run(silent=True)
        # TODO: Sanitize plaintext
        # TODO: Store list of confidences for multiple sections
        # TODO: Iterate overplaintext for multiple sections when implemented, see run()
        confidences = [DETECTOR.compute_language_confidence_values(plaintext) for plaintext in self.plaintext]
        eng = []
        lat = []
        for confidence in confidences:
            eng.append(next(obj.value for obj in confidence if obj.language == Language.ENGLISH))
            lat.append(next(obj.value for obj in confidence if obj.language == Language.LATIN))
        self.fitness["eng"] = reduce(lambda a, b: a+b, eng) / len(eng)
        self.fitness["lat"] = reduce(lambda a, b: a+b, lat) / len(lat)
        print("FITNESS:", self.fitness)

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
        self.fsm.set_state(self)
        self.fsm.transition(self.mutation_rate)
        self.__dict__.update(self.fsm.current_state.__dict__)


    # TODO: Use this implementation when FSM/rule engine are integrated, d4vi's is much better
    #def crossover(self, **kwargs):
    #    child = SolutionSpec()
    #    for key in self.__dict__:
    #        if random.random() < 0.5:
    #            setattr(child, key, self.__dict__[key])
    #        else:
    #            setattr(child, key, kwargs[key])
    #    return child

    #def mutate(self):
    #    mutation_rate = 0.1  # Adjust this mutation rate
    #    for key in self.__dict__:
    #        if random.random() < mutation_rate:
    #            # Example of mutation: increment or decrement by a small random amount
    #            setattr(self, key, self.__dict__[key] + random.uniform(-0.1, 0.1))

def random_spec():
    raise NotImplementedError("random_spec not implemented")

def random_specs():
    raise NotImplementedError("random spec not implemented")
