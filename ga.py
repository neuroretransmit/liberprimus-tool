import json
from specs import random_specs
from random import getrandbits
from db.db import insert_solution_attempt, solution_exists

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
            # TODO: check if solution tried in database and continue if it has
            scheme_name = getattr(offspring.crypto.scheme, '__name__', 'Unknown')
            skips = json.dumps(offspring.crypto.skips) if offspring.crypto.skips is not None else None
            excludes = json.dumps(offspring.crypto.excludes) if offspring.crypto.excludes is not None else None
            if solution_exists(scheme_name, offspring.crypto.key, offspring.crypto.shift, skips, excludes):
                continue
            # Run the spec and grab fitness
            offspring.rate()
            # TODO: add solution to database
            max_confidence = max([v for k, v in offspring.fitness.items()])
            max_confidence_lang = next(k for k, v in offspring.fitness.items() if v == max_confidence)
            insert_solution_attempt(scheme_name, offspring.crypto.key, offspring.crypto.shift, max_confidence, max_confidence_lang, skips, excludes)
            # Pop the worst individual out of the genepool in-place
            self.pool.pop()
            # Add new offspring
            self.pool.append(offspring)
            # TODO: See if fitness function can find breaks in the language and try to auto specify
            #       skips/excludes
