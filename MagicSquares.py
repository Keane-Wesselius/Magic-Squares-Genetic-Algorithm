# -*- coding: utf-8 -*-
import math
import random
import copy
import sys
import time


#Variables to control hyperparameters
#Do to code implementation:
#num_elites and population_size must both be even
#Because the code we have converges extremely fast it is easy to get caught in a local optimum 
# so a very high mutation chance ~50% is needed to be able to escape the local optimum
n = 6
nn = n * n
n2 = nn//2
magic_number = n*(n**2 + 1)/2
population_size = 200
num_elites = 150
num_mutations = 1
mutation_chance = 1
epoch = 1000000
crossover_attempts = 20

population = []
fitness = []


#Create the initial population of squares
def generate_critters():
    pop = []
    for i in range(population_size):
        c = list(range(1, nn+1))
        random.shuffle(c)
        pop.append(c)
    return pop
        




#Get the fitness values for the entire population
#############################################################################################################################
#Need to change to try differnt fitness algorithms
def get_populations_fitness(pop):
    fit = []
    for c in pop:
        fit.append(find_fitness2(c))
    return fit
        

#New fitness function, as opposed to the the old fitness function, this one causes the genetic algorithm to converge much faster 
#We already know what the sums of rows columns diagonals should be
#We calculate how far away each row, column, diagonal is from this magic number and sum them to get the "distance" from a magic square
#A distance of 0 means we have a magic square
def find_fitness2(creature):
    fit = 0

    #check all rows
    sum = 0
    for i in range(nn):
        if (i%n == 0 and i != 0):
            fit += abs(magic_number - sum)
            sum = 0
        sum += creature[i]
    fit += abs(magic_number - sum)
    
    #check all columns
    for j in range(n):    
        sum = 0
        for i in range(j, nn, n):
            sum += creature[i]
        fit += abs(magic_number - sum)
    
    #diagonal down
    sum = 0
    for i in range(0, nn, n+1):
        sum += creature[i]
    fit += abs(magic_number - sum)
    
    #diagonal up
    sum = 0
    for i in range(n-1, nn-1, n-1):
        sum += creature[i]
    fit += abs(magic_number - sum)

    return fit


#OLD fitness function calculating the standard deviation of all the sums and how far away they are from each other
#Get the fitness value for a single square
def find_fitness(creature):
    values = []
    
    #check all rows
    sum = 0
    for i in range(nn):
        if (i%n == 0 and i != 0):
            values.append(sum)
            sum = 0
        sum += creature[i]
    values.append(sum)
    
    #check all columns
    for j in range(n):    
        sum = 0
        for i in range(j, nn, n):
            sum += creature[i]
        values.append(sum)
    
    #diagonal down
    sum = 0
    for i in range(0, nn, n+1):
        sum += creature[i]
    values.append(sum)
    
    #diagonal up
    sum = 0
    for i in range(n-1, nn-1, n-1):
        sum += creature[i]
    values.append(sum)
     
    return calculate_flatness(values)
    





#Helper function for OLD fitness finding
def calculate_flatness(square_sums):
    average = 0
    for i in range(len(square_sums)):
        average += square_sums[i]
    average = average / len(square_sums)
    
    variance = 0
    for i in range(len(square_sums)):
        variance += (square_sums[i] - average)**2
    
    variance = variance / (len(square_sums) - 1)
    deviation = math.sqrt(variance)
    
    return deviation
    





#Determines if we have found a magic square or not
def did_we_win(fit):
    if 0.0 in fit:
        return fit.index(0.0)
    return -1
        

#Old Code not used
def is_valid_square(creature):
    numbers = set(range(1, nn+1))
    possible_square = set(creature)
    
    if numbers == possible_square:
        return True
    return False
    



#Elites are members of the population that continue on to the next generation without change
#this function finds the elites of the population(best of the best)   
def get_elites(pop, fit):
    #combines each square to its fitness
    combined = list(zip(pop, fit))
    #sorts by fitness
    combined = sorted(combined, key=lambda x: x[1])
    #now uncombine them and get the population sorted by fitness
    elites, trash = zip(*combined)
    fave = 0
    for f in trash:
        fave += f
    fave = fave / len(trash)
    print(f"Best Fitness: {trash[0]}")
    print(f'Average Fitness: {fave}')
    print(f'Top Elite: {elites[0]}')

    return list(elites)





#Mutation function makes 2 random indexes and swaps the values at those indexes
def mutate(creature):
#=============================================================================
    mutation_type = random.randint(0, 0)
#=============================================================================
    
    
    if mutation_type == 0:
    #if True:
        num_mut = random.randint(1, num_mutations)
        for _ in range(num_mut):
            i = random.randint(0, nn-1)
            j = random.randint(0, nn-1)
            temp = creature[i]
            creature[i] = creature[j]
            creature[j] = temp
        return creature
    
#=============================================================================
    # if mutation_type == 1:
    #     row = random.randint(0, n - 1)
    #     row_start = row * n
    #     row_stop = row_start + n
    #     numbers = creature[row_start:row_stop]
    #     random.shuffle(numbers)
    #     creature[row_start:row_stop] = numbers
    #     return creature
        
    # if mutation_type == 2:
    #     indexes = []
    #     numbers = []
    #     column = random.randint(0, n - 1)
    #     for i in range(column, nn, n):
    #         indexes.append(i)
    #         numbers.append(creature[i])
    #     random.shuffle(numbers)

    #     j = 0
    #     for i in indexes:
    #         creature[i] = numbers[j]
    #         j += 1
    #     return creature
#=============================================================================

            
            
            
            

#The crossover function implemented is the PMX algorithm
def crossover(p1, p2):
    # for _ in range(crossover_attempts):
    #     i = random.randint(1, nn-1)
    #     baby = c1[:i] + c2[i:]
    #     if is_valid_square(baby):
    #         return baby
    # return -1
    
    index1 = random.randint(0,n2)
    index2 = random.randint(n2+1,nn)
    c1 = [0 for _ in range(nn)]
    c2 = [0 for _ in range(nn)]
    c1[index1:index2] = p2[index1:index2]
    c2[index1:index2] = p1[index1:index2]

    for i in range(nn):
        if (not p1[i] in c1) and (i < index1 or i > index2 - 1):
            c1[i] = p1[i]
        if (not p2[i] in c2) and (i < index1 or i > index2 - 1):
            c2[i] = p2[i]

    while(0 in c1):
        i0 = c1.index(0)
        i = i0
        num = p1[i]
        while num in c1:
            i = c1.index(num)
            num = p1[i]
        c1[i0] = num


    while(0 in c2):
        i0 = c2.index(0)
        i = i0
        num = p2[i]
        while num in c2:
            i = c2.index(num)
            num = p2[i]
        c2[i0] = num

    return c1, c2
        
        
        
        
#Used to take the current population and make the next generation
#In order to preserve genetic diversity NO duplicates of squares are allowed to go into the next generation
#A roulette selection is used to find parents for the crossover function
def breed(pop, fit):
    popc = copy.deepcopy(pop)
    mating_pool = []
    next_gen = []
    
    #number_left_to_make = population_size

    number_left_to_make = population_size - num_elites
        
    #sort the population based off of fitness values
    elites = get_elites(pop, fit)


    # temp = elites[0:num_elites - 1]
    # mut_elite = mutate(copy.copy(elites[0]))
    # top_elites = copy.deepcopy(temp)
    # top_elites.append(mut_elite)

    #Not just offspring but the elites must also be unique going into the next generation
    unique_elites = []
    for e in elites:
        if not e in unique_elites:
            unique_elites.append(e)
    print(len(unique_elites))

    if len(unique_elites) < num_elites:
        print("ERROR")
        sys.exit()
    next_gen = unique_elites[0:num_elites]


#This is used to convert the fitness scores into proportional values so we may do the roulette selection
#=======================================================================================================================
    fitsum = 0
    bigfit = []
    for i in fitness:
        bigfit.append(10000 - i)
    
    for i in bigfit:
        fitsum += i
   
    
    mating_pool.append(bigfit[0]/fitsum)
    for i in range(1, len(bigfit)):
        prob = bigfit[i]/fitsum
        mating_pool.append(prob + mating_pool[i-1])
#=========================================================================================================================     
        
#This is where we pick the parents to make the "babys" for the next generation
    while number_left_to_make > 0:
        choice1 = random.random()
        choice2 = random.random()
        index1 = 0
        index2 = 0
        for i in range(len(mating_pool)):
            if choice1 <= mating_pool[i]:
                index1 = i
                break
        for i in range(len(mating_pool)):
            if choice2 <= mating_pool[i]:
                index2 = i
                break
    
            
            
        candidate1 = copy.copy(popc[index1])  
        candidate2 = copy.copy(popc[index2])
        #candidate = mating_pool[random.randint(0,len(mating_pool)-1)]


        baby1, baby2 = crossover(candidate1, candidate2)
        #If we mutate the babys or not
        if random.randint(0, mutation_chance) == 0:
            baby1 = mutate(baby1)
            baby2 = mutate(baby2)
        # next_gen.append(baby1)
        # next_gen.append(baby2)
        # number_left_to_make -= 2

        #ALL offspring must be unique, duplicate magic squares are NOT accepted into the next generation
        if (not baby1 in next_gen):
            next_gen.append(baby1)
            number_left_to_make -= 1
        if ((not baby2 in next_gen) and number_left_to_make > 0):
            next_gen.append(baby2)
            number_left_to_make -= 1


# =============================================================================
        # if random.randint(0, 1) == 0:
        #     candidate1 = mutate(candidate1)
        #     next_gen.append(candidate1)
        #     number_left_to_make -= 1
        # else:
        #     #candidate2 = mating_pool[random.randint(0,len(mating_pool)-1)]
        #     baby = crossover(candidate1, candidate2)
        #     if baby != -1:
        #         next_gen.append(baby)
        #         number_left_to_make -= 1
# =============================================================================
                

    #next_gen = top_elites + next_gen
    print()
    return next_gen
        
        
        






#ACTUALLY RUN THE PROGRAM
#inital setup, create the initial population
population = generate_critters()

#Loop though until the epoch is met or we find a magic square
for i in range(epoch):
    print(f"Current generation: {i}")
    
    fitness = get_populations_fitness(population)

    if i % 500 == 0 and i != 0:
        for i in range(len(population)):
            print(f'Square: {population[i]}  Fitness: {fitness[i]}')
        time.sleep(5)

    index = did_we_win(fitness)
    if index != -1:
        print(f"Magic Square: {population[index]}")
        break
    population = breed(population, fitness)
