from typing import Final, List
import random
import math

# A simple genetic algorithm implementation
# Genome length is 8, and each gene can be either 0 or 1.
GENOME_LENGTH: Final = 8
LIMITS: Final[List[int]] = [-10, 10]
Genome = List[int]
Population = List[Genome]
Fitness = List[float]

def generate_genome() -> Genome:
    return [random.randint(0, 1) for _ in range(GENOME_LENGTH)]

def generate_population(size: int) -> Population:
    return [generate_genome() for _ in range(size)]

def binary_decode(genome: Genome) -> float:
    return LIMITS[0] + (LIMITS[1] - LIMITS[0])/(sum(2**(-i) for i in range(1, GENOME_LENGTH//2 + 1))) * sum(gene * (2**(-i)) for i, gene in enumerate(genome, start=1))

def fitness_value(genome: Genome) -> float:
    BinaryLeft = binary_decode(genome[:GENOME_LENGTH//2])
    BinaryRight = binary_decode(genome[GENOME_LENGTH//2:])

    trig_term = math.sin(BinaryLeft) * math.cos(BinaryRight) * math.tan(BinaryRight + BinaryLeft)

    exp_term = 0.5 * math.exp(1 - math.sqrt(BinaryRight**2))

    return -(trig_term + exp_term)

def main():
    population_size = 100
    generations = 500
    mutation_rate = 0.0001
    population = generate_population(population_size)
    for generation in range(generations):
        fitness_values = [fitness_value(genome) for genome in population]
        best_genome = population[fitness_values.index(min(fitness_values))]
        print(f"Generation {generation+1}: Best Genome: {best_genome}, Decoded Genome: {[binary_decode(best_genome[:GENOME_LENGTH//2]), binary_decode(best_genome[GENOME_LENGTH//2:])]}, Fitness: {min(fitness_values)}")
        # Selection (roulette wheel)
        total_fitness = sum(fitness_values)
        probabilities = [(total_fitness - fitness) / total_fitness for fitness in fitness_values]
        # New Population
        new_population = []
        for _ in range(population_size):
            parent1 = random.choices(population, weights=probabilities, k=1)[0]
            parent2 = random.choices(population, weights=probabilities, k=1)[0]
            # Crossover
            crossover_point = random.randint(1, GENOME_LENGTH - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]
            # Mutation
            child = [gene if random.random() > mutation_rate else random.randint(0, 1) for gene in child]
            new_population.append(child)
        population = new_population

if __name__ == "__main__":
    main()