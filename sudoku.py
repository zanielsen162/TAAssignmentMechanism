import gurobipy as gp
from gurobipy import GRB
import numpy as np

def find_solution(initial_board, n=9):
    model = gp.Model('ConstraintOptimization')
    model.setParam('OutputFlag', 0)

    # Variables b[i]
    vars = model.addVars(n, n, n, vtype=GRB.BINARY, name='board')
    x,y = np.nonzero(initial_board)

    for i,j in zip(x,y):
        vars[i,j, initial_board[i][j] - 1] = 1

    # constrains the rows
    model.addConstrs((vars.sum(i,'*',k) == 1 for i in range(n) for k in range(n)), name='rows')

    # constrains the columns
    model.addConstrs((vars.sum('*',j,k) == 1 for j in range(n) for k in range(n)), name='cols')

    # each square has a value
    model.addConstrs((vars.sum(i,j,'*') == 1 for i in range(n) for j in range(n)), name='filled_in')

    # constrains the boxes
    box_indices = [ i for i in range(n) if i % int(np.sqrt(n)) == 0 ]
    model.addConstrs((gp.quicksum(vars[i,j,k] for j in range(a, a+int(np.sqrt(n))) for i in range(b, b+int(np.sqrt(n)))) == 1 for k in range(n) for a in box_indices for b in box_indices))

    # Verify model formulation
    model.write('OptimizeConstraint.lp')

    # Run optimization engine
    model.optimize()

    for i in range(n):
        for j in range(n):
            for k in range(n):
                try:
                    if vars[i,j,k].X != 0:
                        initial_board[i][j] = k+1
                except:
                    pass
    return initial_board

quizzes = np.zeros((1000000, 81), np.int32)
solutions = np.zeros((1000000, 81), np.int32)
for i, line in enumerate(open('sudoku_subset.csv', 'r').read().splitlines()[1:]):
    quiz, solution = line.split(",")
    for j, (q,s) in enumerate(zip(quiz, solution)):
        quizzes[i, j] = int(q)
        solutions[i, j] = int(s)
quizzes = quizzes.reshape((-1, 9, 9))
solutions = solutions.reshape((-1, 9, 9))

failures = 0
sucesses = 0

for i in range(10):
    problem = quizzes[i]
    proposed_solution = find_solution(problem)

    if (np.all(proposed_solution == solutions[i])):
        print('--SUCCESS--')
        sucesses += 1
    else:
        print('--FAILURE--')
        print('problem')
        print(problem)
        print('difference')
        print(proposed_solution - solutions[i])
        print('wrong')
        print(proposed_solution)
        print('right')
        print(solutions[i])
        print('------------')
        failures += 1

print("Failures:", failures)
print("Successes:", sucesses)