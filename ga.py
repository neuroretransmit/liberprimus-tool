from specs import random_specs
from random import getrandbits

class GeneticAlgorithm:
    def __init__(self, target: float, initial_pool:list = []):
        self.target = target
        if initial_pool != []:
            self.pool = initial_pool
        else:
            self.pool = random_specs()

    def evolve(self):
        while True:
            self.pool.sort(key=lambda i: max([v for k, v in i.fitness.items()]))
            # select two fittest
            parents = self.pool[:2]
            print(f"BEST: {self.pool[0].fitness}")
            if parents[0].fitness == self.target:
                break
            # crossover
            print("TODO: crossover")
            offspring = parents[0].crossover(**parents[1].__dict__)
            print("TODO: mutate")
            offspring.mutate()
            offspring.rate()
            self.pool = self.pool[:-1]
            self.pool.append(offspring)
            # FIXME: Walk nested objects/mutate shifts/use wordlist for keys/exchange lookups
            # TODO: See if fitness function can find breaks in the language and try to auto specify
            #       skips/excludes
            raise NotImplementedError("evolve not implemented yet")

