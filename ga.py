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
            # rank population by fitness
            self.pool.sort(key=lambda i: max([v for k, v in i.fitness.items()]))
            # select two fittest
            parents = self.pool[:2]
            print(f"BEST: {self.pool[0].fitness}")
            if parents[0].fitness == self.target:
                break
            # TODO: finish crossover
            offspring = parents[0].crossover(**parents[1].__dict__)
            # TODO: finish mutation
            offspring.mutate()
            # Run the spec and grab fitness
            offspring.rate()
            # Pop the worst individual out of the genepool in-place
            self.pool.pop()
            # Add new offspring
            self.pool.append(offspring)
            # TODO: See if fitness function can find breaks in the language and try to auto specify
            #       skips/excludes
