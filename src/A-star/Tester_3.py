from tools_2 import AStarSolver_2
from time import time
from queue import PriorityQueue

class Tester:
    def __init__(self):
        self.target_seq_1 = None
        self.target_seq_2 = None
        self.target_solution_1 = None
        self.target_solution_2 = None
        self.target_match_cost_1 = float('inf')
        self.target_match_cost_2 = float('inf')
        self.matchSeq = str(input('Please input the sequence to match: '))
        databaseName = str(input('Please input the file name of database: '))
        with open(databaseName, 'r') as dataFile:
            self.dataSeq = dataFile.read().splitlines()
    
    def run_test(self):
        # 要存前两个最大的，使用 PriorityQueue
        target_index = 0
        begin_time = time()
        solver_array = list(range(len(self.dataSeq)))
        cost_of_all = PriorityQueue()

        for (index, seq) in enumerate(self.dataSeq):
            solver_array[index] = AStarSolver_2((self.matchSeq, seq))
            match_cost = solver_array[index].solve()
            cost_of_all.put((match_cost, index))

        biggest_match = cost_of_all.get()
        target_index = biggest_match[1]
        self.target_seq_1 = self.dataSeq[target_index]
        self.target_solution_1 = solver_array[target_index].align_seq()
        self.target_match_cost_1 = biggest_match[0]

        second_biggest_match = cost_of_all.get()
        target_index = second_biggest_match[1]
        self.target_seq_2 = self.dataSeq[target_index]
        self.target_solution_2 = solver_array[target_index].align_seq()
        self.target_match_cost_2 = second_biggest_match[0]

        end_time = time()
        time_used = end_time - begin_time

        print('\n')
        print('The sequence that matches the input sequence most is:')
        print(self.target_seq_1)
        print('The two sequences after matching:')
        print(self.target_solution_1[0])
        print(self.target_solution_1[1])
        print(f'The cost of matching is: {self.target_match_cost_1}')

        print('\n')
        print('The sequence that matches the input sequence second most is:')
        print(self.target_seq_2)
        print('The two sequences after matching:')
        print(self.target_solution_2[0])
        print(self.target_solution_2[1])
        print(f'The cost of matching is: {self.target_match_cost_2}')

        print('\n')
        print(f'Total time used: {time_used}')


if __name__ == "__main__":
    Tester().run_test()