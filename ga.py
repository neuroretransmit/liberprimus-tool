from specs import random_specs
from random import getrandbits

class GeneticAlgorithm:
    def __init__(self, target: float, initial_pool:list = None):
        self.target = target
        if initial_pool:
            self.pool = initial_pool
        else:
            self.pool = random_specs()

    def evolve(self):
        while True:
            self.pool.sort(key=lambda i: i.fitness)
            # select two fittest
            parents = self.pool[:2]
            print(f"BEST: {self.pool[0].fitness}", end="\r")
            if parents[0].fitness == self.target:
                break
            # crossover
            # FIXME: Walk nested objects/mutate shifts/use wordlist for keys/exchange lookups
            # TODO: See if fitness function can find breaks in the language and try to auto specify
            #       skips/excludes
            for attr, v in vars(parents[0]).items():
                if getrandbits(1):
                    parents[1][attr] = v
        raise NotImplementedError("evolve not implemented yet")

