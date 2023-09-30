from tools_2 import AStarSolver_2
from time import time

class Tester:
    def __init__(self):
        self.target_seq = None
        self.target_solution = None
        self.target_match_cost = float('inf')
        self.matchSeq = str(input('Please input the sequence to match: '))
        databaseName = str(input('Please input the file name of database: '))
        with open(databaseName, 'r') as dataFile:
            self.dataSeq = dataFile.read().splitlines()
    
    def run_test(self):
        target_index = 0
        begin_time = time()
        solver_array = list(range(len(self.dataSeq)))
        for (index, seq) in enumerate(self.dataSeq):
            solver_array[index] = AStarSolver_2((self.matchSeq, seq))
            match_cost = solver_array[index].solve()
            if match_cost < self.target_match_cost:
                target_index = index
                self.target_match_cost = match_cost
        self.target_seq = self.dataSeq[target_index]
        self.target_solution = solver_array[target_index].align_seq()
        end_time = time()
        time_used = end_time - begin_time

        print('\n')
        print('The sequence that matches the input sequence most is:')
        print(self.target_seq)
        print('The two sequences after matching:')
        print(self.target_solution[0])
        print(self.target_solution[1])
        print(f'The cost of matching is: {self.target_match_cost}')

        print('\n')
        print(f'Total time used: {time_used}')


if __name__ == "__main__":
    Tester().run_test()