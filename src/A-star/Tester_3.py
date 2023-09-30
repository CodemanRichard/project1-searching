from tools_2 import AStarSolver_2
from tools_3 import AStarSolver_3
from time import time
from queue import PriorityQueue

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
        dataPairSeq = []
        for (index, seq1) in enumerate(self.dataSeq):
            for seq2 in self.dataSeq[(index+1):]:
                dataPairSeq.append((self.matchSeq, seq1, seq2))
        solver_array = list(range(len(dataPairSeq)))

        for (index, seq) in enumerate(dataPairSeq):
            # 使用下界估计判断是否需要进行匹配
            lower_bound = (AStarSolver_2((seq[0], seq[1])).solve()+
                           AStarSolver_2((seq[0], seq[2])).solve()+
                           AStarSolver_2((seq[1], seq[2])).solve())
            if lower_bound < self.target_match_cost:
                solver_array[index] = AStarSolver_3(seq)
                match_cost = solver_array[index].solve()
                if match_cost < self.target_match_cost:
                    target_index = index
                    self.target_match_cost = match_cost
        self.target_seq = dataPairSeq[target_index]
        self.target_solution = solver_array[target_index].align_seq()
        end_time = time()
        time_used = end_time - begin_time

        print('\n')
        print('The sequences that match the input sequence most are:')
        print(self.target_seq[1])
        print(self.target_seq[2])
        print('The three sequences after matching:')
        print(self.target_solution[0])
        print(self.target_solution[1])
        print(self.target_solution[2])
        print(f'The cost of matching is: {self.target_match_cost}')

        print('\n')
        print(f'Total time used: {time_used}')


if __name__ == "__main__":
    Tester().run_test()