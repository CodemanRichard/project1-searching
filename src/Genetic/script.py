from tools_2 import GeneticSolver_2
from tools_2 import Individual

if __name__ == "__main__":

    # Global Test
    test_solver = GeneticSolver_2(('ABCDE','BCDEF'))
    cost = test_solver.solve()
    aligned = test_solver.align_seq()
    print(f'cost is: {cost}')
    print(f'aligned sequences are:\n{aligned[0]}\n{aligned[1]}')

    # crossover test
    """test_solver = GeneticSolver_2(('ABCDE','BCDEF'))
    for i in range(10):
        print(f'round {i}')
        test_solver.crossover()"""
    
    # get_seq test
    """indi = Individual(('ABCDE', 'BCDEF'))
    seq = indi.get_seq()
    print(seq)"""