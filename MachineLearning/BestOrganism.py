import random

# Define the traits
traits = "SRIEFX"

# Parameters
population_size = 100
mutation_rate = 0.05
generations = 1000
organism_length = 10  # Length of the trait string for each organism

# Function to create a random organism
def create_organism():
    return ''.join(random.choice(traits) for _ in range(organism_length))

# Fitness function: Sum of S, R, I, E (positive traits), minus number of X (negative trait)
def calculate_fitness(organism):
    fitness = 0
    for trait in organism:
        if trait in "SRIE":
            fitness += 1
        elif trait == "X":
            fitness -= 1
    return fitness

# Function to perform crossover between two parents
def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    return parent1[:crossover_point] + parent2[crossover_point:]

# Function to perform mutation on an organism
def mutate(organism):
    organism = list(organism)
    for i in range(len(organism)):
        if random.random() < mutation_rate:
            organism[i] = random.choice(traits)
    return ''.join(organism)

# Initialize population
population = [create_organism() for _ in range(population_size)]

# Evolution process
for generation in range(generations):
    # Calculate fitness for each organism
    fitness_scores = [calculate_fitness(organism) for organism in population]

    # Find and print the best organism in the current generation
    best_organism = population[fitness_scores.index(max(fitness_scores))]
    print(f"Generation {generation}: Best organism so far - '{best_organism}' with fitness {max(fitness_scores)}")

    # Selection: Select the top organisms to be parents
    parents = random.choices(population, weights=fitness_scores, k=population_size // 2)

    # Crossover and Mutation: Create a new population
    new_population = []
    for i in range(population_size):
        parent1, parent2 = random.sample(parents, 2)
        child = mutate(crossover(parent1, parent2))
        new_population.append(child)
    
    # Replace the old population with the new one
    population = new_population

# Final best organism
final_best = max(population, key=lambda org: calculate_fitness(org))
print(f"Final best organism: '{final_best}' with fitness {calculate_fitness(final_best)}")
