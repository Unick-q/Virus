import random

class Person:
    id = 0 # Initial population

    def __init__(self):
        Person.id += 1  # Name of the person.
        self.id = Person.id

        # Epidemic state
        self.suceptible = 0 #int(round(random.uniform(0, 1), 0))   # 0 means without disease, 1 means infected
        self.exposed    = 0
        self.vaccinated = 0 # Assume all 0 (None of them took vaccine).
        self.removed    = 0 # 0 means not in R compartment, 1 is.

        self.infection_clock = 0

        self.compartment_history = []

    def make_population(N):
        population = []
        for i in range(N):
            population.append(Person())
        return population
