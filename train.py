import argparse
import string
from genetic import create_population, new_generation
from operator import itemgetter, attrgetter
import numpy as np
import math

parser = argparse.ArgumentParser()
parser.add_argument('--word', metavar='w', help='Word to be guessed', default='hello')
parser.add_argument('--popsize', metavar='p', help='Population size', default='961', type=int)
parser.add_argument('--mutation', metavar='m', help='Mutation rate', default='0.1', type=float)
parser.add_argument('--max_gen', metavar='g', help='Maximum generations', default=2000, type=int)
args = vars(parser.parse_args())

solved = False
solution_space = list(string.ascii_lowercase)
solution = args['word']
solution_bits = np.array([np.array(list(bin(ord(letter)).replace('0b', ''))) for letter in solution], dtype=np.int8)
population_size = args['popsize']
final_fitness = np.sum(solution_bits)

print(f'Target fitness: {final_fitness}')

population = create_population(
  population_size = population_size,
  solution_size = len(solution),
  solution_space_size = len(solution_space)
)

for generation in range(args['max_gen']):
  if solved: break
  if generation % 100 == 0:
    print(f'Starting generation: {generation}')

  # Calculating fitness
  for unit in population:
    unit.mutate(rate = args['mutation'])
    fitness = unit.calc_fitness(solution_bits)

    if np.array_equal(unit.representation, solution_bits):
      print(f'Solved! Gen #{generation}')
      solved = True
      break

  # Breeding
  population.sort(key=attrgetter('fitness'), reverse=True)
  n_best = int(math.sqrt(len(population)))

  new_population = []
  for xx_unit in population[:n_best]:
    for xy_unit in population[:n_best]:
      child = xx_unit.crossover(xy_unit)
      new_population.append(child)
  if generation % 100 == 0:
    print(f'Best gen fit: {population[0].fitness}')

  # Converting to new population
  population = new_population


if not solved: print('Solution wasnt found')