from abc import ABC, abstractmethod


class DNA(ABC):
    crossover_rate = 0.1
    mutation_rate = 0.05

    @abstractmethod
    def crossover(self, *args, **kwargs):
        raise NotImplementedError("crossover not implemented")

    @abstractmethod
    def mutate(self):
        raise NotImplementedError("mutate not implemented")

    @staticmethod
    @abstractmethod
    def random():
        raise NotImplementedError("random not implemented")
