import random

POPULATION_SIZE = 16
TERMINATE_COUNT = 50
GAP_COST = 3
MISMATCH_COST = 5
MAX_GAP = 1             
CROSSOVER_PROBABILITY = 0.6
MUTATION_PROBABILITY = 0.2
MUTATION_RANGE = 1

class GeneticSolver_3:
    def __init__(self, seq):
        self.seq = seq
        self.population = [Individual(seq) for _ in range(POPULATION_SIZE)]
        self.fitness = [individual.fitness for individual in self.population]
        self.best_individual = None

    def selection(self):
        """Randomly select a subset of the individuals based on their fitness"""
        individual_pool = []
        for individual in self.population:
            for _ in self.fitness:
                individual_pool.append(individual)
        for i in range(len(self.population)):
            self.population[i] = random.choice(individual_pool)
        # debug
        """print('after selection:')
        for individual in self.population:
            print(individual.gap_for_seq1)
            print(individual.gap_for_seq2)"""
        # debug

    def crossover(self):
        """Mate strings for crossover"""
        # e.g. 8个数，0号与4号配对，1与5配对，2与6配对，3与7配对
        # 2k个数，0号与k号配对
        for i in range(int(POPULATION_SIZE/2)):
            couple_1_index = i
            couple_2_index = i + int(POPULATION_SIZE/2)
            if random.random() < CROSSOVER_PROBABILITY:
                # debug
                # print(f'doing crossover of index {couple_1_index} and index {couple_2_index}')
                # debug
                # 对 gap_for_seq1 进行 crossover
                crossover_ceiling = len(self.seq[0]) + 1
                point_1 = random.randrange(0, crossover_ceiling)
                point_2 = random.randrange(0, crossover_ceiling)
                begin_point = min(point_1, point_2)
                end_point = max(point_1, point_2) + 1
                for j in range(begin_point, end_point):
                    tmp = self.population[couple_1_index].gap_for_seq1[j]
                    self.population[couple_1_index].gap_for_seq1[j] = self.population[couple_2_index].gap_for_seq1[j]
                    self.population[couple_2_index].gap_for_seq1[j] = tmp
                # debug
                #print('doing crossover for gap_for_seq1')
                #print(f'crossover ceiling is {crossover_ceiling}, begin at {begin_point}, end at {end_point}')
                # debug
                # 对 gap_for_seq2 进行 crossover
                crossover_ceiling = len(self.seq[1]) + 1
                point_1 = random.randrange(0, crossover_ceiling)
                point_2 = random.randrange(0, crossover_ceiling)
                begin_point = min(point_1, point_2)
                end_point = max(point_1, point_2) + 1
                for j in range(begin_point, end_point):
                    tmp = self.population[couple_1_index].gap_for_seq2[j]
                    self.population[couple_1_index].gap_for_seq2[j] = self.population[couple_2_index].gap_for_seq2[j]
                    self.population[couple_2_index].gap_for_seq2[j] = tmp
                # 对 gap_for_seq3 进行 crossover
                crossover_ceiling = len(self.seq[2]) + 1
                point_1 = random.randrange(0, crossover_ceiling)
                point_2 = random.randrange(0, crossover_ceiling)
                begin_point = min(point_1, point_2)
                end_point = max(point_1, point_2) + 1
                for j in range(begin_point, end_point):
                    tmp = self.population[couple_1_index].gap_for_seq3[j]
                    self.population[couple_1_index].gap_for_seq3[j] = self.population[couple_2_index].gap_for_seq3[j]
                    self.population[couple_2_index].gap_for_seq3[j] = tmp
                # debug
                """print('doing crossover for gap_for_seq2')
                print(f'crossover ceiling is {crossover_ceiling}, begin at {begin_point}, end at {end_point}')
                print('After crossover:')
                print(f'index {couple_1_index}:')
                print(self.population[couple_1_index].gap_for_seq1)
                print(self.population[couple_1_index].gap_for_seq2)
                print(f'index {couple_2_index}:')
                print(self.population[couple_2_index].gap_for_seq1)
                print(self.population[couple_2_index].gap_for_seq2)"""
                # debug



    def mutation(self):
        """Apply random mutation"""
        for i in range(len(self.population)):
            # 对 gap_for_seq1 进行 mutation
            for j in range(len(self.population[i].gap_for_seq1)):
                if random.random() < MUTATION_PROBABILITY:
                    self.population[i].gap_for_seq1[j] += random.randint(-MUTATION_RANGE, MUTATION_RANGE)
                    if self.population[i].gap_for_seq1[j] < 0:
                        self.population[i].gap_for_seq1[j] = 0
            # 对 gap_for_seq2 进行 mutation
            for j in range(len(self.population[i].gap_for_seq2)):
                if random.random() < MUTATION_PROBABILITY:
                    self.population[i].gap_for_seq2[j] += random.randint(-MUTATION_RANGE, MUTATION_RANGE)
                    if self.population[i].gap_for_seq2[j] < 0:
                        self.population[i].gap_for_seq2[j] = 0
            # 对 gap_for_seq3 进行 mutation
            for j in range(len(self.population[i].gap_for_seq3)):
                if random.random() < MUTATION_PROBABILITY:
                    self.population[i].gap_for_seq3[j] += random.randint(-MUTATION_RANGE, MUTATION_RANGE)
                    if self.population[i].gap_for_seq3[j] < 0:
                        self.population[i].gap_for_seq3[j] = 0
        # debug
        """print('After mutation:')
        for individual in self.population:
            seqs = individual.get_seq()
            print(f'{seqs[0]}\n{seqs[1]}\n')"""
        # debug

    def solve(self):
        """Return the minimum match cost between two sequences"""
        best_population = None
        no_better_count = 0
        last_fitness = float('inf')
        new_fitness = 0
        while no_better_count < TERMINATE_COUNT:
            self.selection()
            self.crossover()
            self.mutation()
            # debug
            """print('after selection, crossover and mutation:')
            for individual in self.population:
                print(individual.gap_for_seq1)
                print(individual.gap_for_seq2)"""
            # debug
            # compute new fitness and update
            for i in range(POPULATION_SIZE):
                self.population[i].fitness = self.population[i].get_fitness()
                self.fitness = [individual.fitness for individual in self.population]
            new_fitness = sum(self.fitness)
            if new_fitness < last_fitness:
                # debug
                #print(f'fitness of this round is {new_fitness}, which is better than last round')
                # debug
                best_population = self.population
                no_better_count = 0
            else:
                no_better_count += 1
                # debug
                #print(f'fitness of this round is {new_fitness}, which is not better')
                #print(f'current no_better_count is {no_better_count}')
                # debug
            last_fitness = new_fitness
        self.best_individual = self.find_best_individual(best_population)
        return self.best_individual.fitness
    
    def align_seq(self):
        """Return the string of two matched sequences"""
        return self.best_individual.get_seq()

    def find_best_individual(self, population):
        """Return the individual with best fitness"""
        lowest_fitness = float('inf')
        lowest_index = 0
        for (index, individual) in enumerate(population):
            if individual.fitness < lowest_fitness:
                lowest_index = index
        return population[lowest_index]


class Individual:
    def __init__(self, seq):
        self.seq = seq
        self.gap_for_seq1 = [random.randint(0,MAX_GAP) for _ in range(len(seq[0])+1)]
        self.gap_for_seq2 = [random.randint(0,MAX_GAP) for _ in range(len(seq[1])+1)]
        self.gap_for_seq3 = [random.randint(0,MAX_GAP) for _ in range(len(seq[1])+1)]
        self.fitness = self.get_fitness()
        # debug
        """print(f'for this individual, sequences after initialization:')
        print(self.gap_for_seq1)
        print(self.gap_for_seq2)"""
        # debug

    def get_seq(self):
        """Return the sequences with same length after adding GAP and eliminating unnecessary GAP"""
        seq1 = []
        seq2 = []
        seq3 = []
        seq1_str = ""
        seq2_str = ""
        seq3_str = ""

        # 加上所有的 GAP
        for (index, chr) in enumerate(self.seq[0]):
            for _ in range(self.gap_for_seq1[index]):
                seq1.append('*')
            seq1.append(chr)
        for _ in range(self.gap_for_seq1[index+1]):
            seq1.append('*')
        for (index, chr) in enumerate(self.seq[1]):
            for _ in range(self.gap_for_seq2[index]):
                seq2.append('*')
            seq2.append(chr)
        for _ in range(self.gap_for_seq2[index+1]):
            seq2.append('*')
        for (index, chr) in enumerate(self.seq[2]):
            for _ in range(self.gap_for_seq3[index]):
                seq3.append('*')
            seq3.append(chr)
        for _ in range(self.gap_for_seq3[index+1]):
            seq3.append('*')

        # 去掉重复的 GAP
        for index in list(range(min(len(seq1),len(seq2),len(seq3))))[::-1]:
            if seq1[index]=='*' and seq2[index]=='*' and seq3[index]=='*':
                seq1.pop(index)
                seq2.pop(index)
                seq3.pop(index)

        # 去掉多余的 GAP
        if len(seq1) > len(seq2):
            if len(seq1) > len(seq3):
                for index in list(range(len(seq1)))[::-1]:
                    if index < len(seq2) or index < len(seq3):
                        break
                    if seq1[index]=='*':
                        seq1.pop(index)
            elif len(seq1) < len(seq3):
                for index in list(range(len(seq3)))[::-1]:
                    if index < len(seq1) or index < len(seq2):
                        break
                    if seq3[index]=='*':
                        seq3.pop(index)
        elif len(seq1) < len(seq2):
            if len(seq2) > len(seq3):
                for index in list(range(len(seq2)))[::-1]:
                    if index < len(seq1) or index < len(seq3):
                        break
                    if seq2[index]=='*':
                        seq2.pop(index)
            elif len(seq2) < len(seq3):
                for index in list(range(len(seq3)))[::-1]:
                    if index < len(seq1) or index < len(seq2):
                        break
                    if seq3[index]=='*':
                        seq3.pop(index)


        # 补上 GAP 使得两个序列长度一致
        if len(seq1) >= len(seq2) and len(seq1) >= len(seq3):
            for _ in range(len(seq1)-len(seq2)):
                seq2.append('*')
            for _ in range(len(seq1)-len(seq3)):
                seq3.append('*')
        elif len(seq2) >= len(seq1) and len(seq2) >= len(seq3):
            for _ in range(len(seq1)-len(seq2)):
                seq1.append('*')
            for _ in range(len(seq2)-len(seq3)):
                seq3.append('*')
        elif len(seq3) >= len(seq2) and len(seq3) >= len(seq1):
            for _ in range(len(seq1)-len(seq3)):
                seq1.append('*')
            for _ in range(len(seq2)-len(seq3)):
                seq2.append('*')
                
        for chr in seq1:
            seq1_str += chr
        for chr in seq2:
            seq2_str += chr
        for chr in seq3:
            seq3_str += chr

        return (seq1_str, seq2_str, seq3_str)

    def get_fitness(self):
        """Return the fitness(cost) of an individual"""
        cost = 0
        seq1, seq2, seq3 = self.get_seq()
        mismatch_count = 0
        star_count = 0

        for index in range(len(seq1)):
            mismatch_count = 0
            star_count = 0
            if seq1[index]=='*':
                star_count += 1
            if seq2[index]=='*':
                star_count += 1
            if seq3[index]=='*':
                star_count += 1

            if star_count == 2:
                cost += 2*GAP_COST
            elif star_count == 1:
                if seq1[index]=='*':
                    if seq2[index]==seq3[index]:
                        cost += 2*GAP_COST
                    else:
                        cost += 2*GAP_COST + MISMATCH_COST
                elif seq2[index]=='*':
                    if seq1[index]==seq3[index]:
                        cost += 2*GAP_COST
                    else:
                        cost += 2*GAP_COST + MISMATCH_COST
                else:
                    if seq1[index]==seq2[index]:
                        cost += 2*GAP_COST
                    else:
                        cost == 2*GAP_COST + MISMATCH_COST
            else:
                if seq1[index] != seq2[index]:
                    mismatch_count += 1
                if seq1[index] != seq3[index]:
                    mismatch_count += 1
                if seq2[index] != seq3[index]:
                    mismatch_count += 1
                cost += mismatch_count*MISMATCH_COST
        return cost