import numpy as np
import re
from functools import reduce
import operator

def create_population(population_size = None, solution_size = None, solution_space_size = None):
  bin_len = len(bin(solution_space_size))
  pre_binary = np.random.rand(population_size, solution_size, bin_len)
  binary_population = np.where(pre_binary < 0.5, 0, 1)
  return [Unit(binary_population[i]) for i in range(population_size)]

def new_generation(parameter_list):
  pass

class Unit(object):
  def __init__(self, representation):
    self.representation = representation
    self.fitness = 0

  def calc_fitness(self, target):
    self.fitness = -1 * np.sum(target - self.representation)
    return self.fitness

  def to_word(self):
    word = ''
    for bin_letter in self.representation[:]:
      letter = ''
      for bit in list(bin_letter):
        letter += str(bit)
      word += chr(int(f'0b{letter}', 2) + 97)
    return re.sub('[^a-z]', ' ', word)

  def mutate(self, rate = 0.2):
    shape = self.representation.shape
    line_shape = reduce(operator.mul, shape, 1)
    line = self.representation.reshape(line_shape)
    mutation = np.random.rand(line_shape)
    diff_line = np.where(mutation < rate, 0, 1)
    new_line = (line + diff_line)
    new_line = np.where(new_line > 0, 1, 0)
    self.representation = new_line.reshape(shape)


  def crossover(self, other_unit):
    other_representation = other_unit.representation
    cross_point = other_representation.shape[1] // 2
    parent_genes = [self.representation[:, :cross_point], other_representation[:, cross_point:]]
    child = np.concatenate(parent_genes, axis=1)
    return Unit(child)