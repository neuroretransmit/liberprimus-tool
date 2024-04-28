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


    def evolve(self):
        while True:
            new_population = []
            for _ in range(self.population_size):
                # parents selection
                parent1, parent2 = self.select_parents()
                # crossover
                child = parent1.crossover(**parent2.__dict__)
                # mutation
                child.mutate()
                new_population.append(child)
    
            self.population = new_population
