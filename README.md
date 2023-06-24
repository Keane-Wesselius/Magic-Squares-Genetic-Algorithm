# Magic-Squares-Genetic-Algorithm
A Python program using genetic algorithms to generate Magic Squares. The program will not always converge on a magic square due to the randomness of the program but converges most of the time. Tested and working for square sizes 3-10 inclusive.

# Hyper Parameters
n = the size of the magic square you are trying to generate. if n = 6 it will generate a 6x6 magic square.

population_size = the number of magic squares each generation. Having more will increase the diversity of squares but will also slow down the time between generations.

num_elites = the number of the top squares(Fittest) that move on from the current generation to next generation without changing.

num_mutations = a mutation for this problem is randomly selecting two indexes from the square and swapping the values. Having num_mutations = 3 would perform this operation 3 times per mutation.

mutation_chance = to determine if a mutation occurs rolls a random number from 0 to mutation chance(inclusive), if the number is 0 we mutate

# Crossover
The crossover method used is a Two-point Partially Mapped Crossover(PMX) function.
For more information on how it works I looked at Wikipedia's section on it you can find it here https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm).
The PMX function allows crossovers to guarantee to produce a magic square with all the possible numbers with no repeats while keeping some of the order of the parents.
Keeping the order is very important for this problem because the order is what makes a square magic or not.

# Fitness
The fitness function used makes use of the fact that we can know the magic number of a square based on the size of the dimensions. So we calculate this magic number and determine the distance away for the magic number of each row, column, and diagonal then we sum these distances giving us our fitness score. This means that a fitness score of 0 is a magic square and the larger the fitness value, the worse the square is. 

# Selection
The selection function used to pick the parents for the crossover is based on the fitness proportional selection. Where everyone in the population has a chance to be selected, but the better the fitness of the individual, the greater the chance of being selected for the crossover function. Wikipedia has another great article explaining how this is done https://en.wikipedia.org/wiki/Fitness_proportionate_selection. 

# Additional Notes (Important)
This code has the hyperparameters set the way I found works best, it may be possible to achieve something better by tweaking these. 
In addition one crucial part not mentioned above is that each magic square per generation is unique. This means that if the population size is 200 that generation will contain 200 different magic squares. Without this feature, the magic squares will quickly devolve into a local minimum that they will not be able to escape from.


