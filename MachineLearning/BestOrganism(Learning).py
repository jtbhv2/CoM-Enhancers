import random

# Define traits and environment parameters
traits = "SRIEFX"  # Speed, Strength, Intelligence, Endurance, Inefficient Trait
population_size = 100
mutation_rate = 0.05
generations = 1000
organism_length = 10
initial_food_supply = 100
predator_aggression = 0.05  # Base probability of predators attacking an organism

# Function to create a random organism
def create_organism():
    return ''.join(random.choice(traits) for _ in range(organism_length))

# Decode traits from the organism string
def decode_traits(organism):
    traits_count = {trait: organism.count(trait) for trait in traits}
    return traits_count

# Fitness function
def calculate_fitness(organism, food, predators):
    traits_count = decode_traits(organism)
    
    # Base fitness score based on positive traits
    fitness = (traits_count['S'] * 2 +  # Strength
               traits_count['R'] * 1 +  # Endurance
               traits_count['I'] * 1 +  # Intelligence
               traits_count['E'] * 1)   # Speed

    # Adjust fitness based on traits
    if traits_count['X'] > 0:
        fitness -= traits_count['X'] * 2  # Penalize for inefficient traits

    # Adjust fitness based on food supply (affected by Intelligence)
    food_requirement = (traits_count['S'] * 0.5) + 1  # Increase food requirement based on Strength
    if food < food_requirement:
        fitness -= (food_requirement - food) * 2  # Penalize if not enough food
    
    # Adjust fitness based on food supply and Intelligence
    fitness += (food * 0.1) + (traits_count['I'] * 0.5)  # Intelligence increases food gathering
    
    # Adjust fitness based on predators
    predator_chance = predator_aggression - (traits_count['E'] * 0.01)  # Endurance reduces predator chance
    if random.random() < predator_chance:
        fitness -= (10 - traits_count['S'])  # Strength increases survival chance

    return max(fitness, 0)  # Ensure fitness is non-negative

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
def initialize_population():
    return [create_organism() for _ in range(population_size)]

# Main evolution process
food_supply = initial_food_supply
population = initialize_population()  # Initialize population here

for generation in range(generations):
    # Calculate fitness for each organism
    fitness_scores = [calculate_fitness(organism, food_supply, predator_aggression) for organism in population]

    # Find and print the best organism in the current generation
    best_in_generation = population[fitness_scores.index(max(fitness_scores))]
    print(f"Generation {generation}: Best organism so far - '{best_in_generation}' with fitness {max(fitness_scores)}")

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

    # Update food supply and predator aggression over generations
    food_supply *= 0.99  # Decrease food supply slightly each generation
    predator_aggression *= 1.01  # Increase predator aggression slightly each generation

    # Ensure food supply and predator aggression stay within reasonable bounds
    food_supply = max(food_supply, 10)
    predator_aggression = min(predator_aggression, 1)

# Final best organism
final_best = max(population, key=lambda org: calculate_fitness(org, food_supply, predator_aggression))
print(f"Final best organism: '{final_best}' with fitness {calculate_fitness(final_best, food_supply, predator_aggression)}")
