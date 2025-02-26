import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
from classes import *

# Construct the model
# Input: 
#   list of courses with number of needed applicants and rankings
#   list of applicants
#   list of edges between courses and applicants
# Output:
#   solution of the optimization problem

course_a = Course('a', [], 2, []) 
course_b = Course('b', [], 1, [])

ta_1 = Applicant('1', 4.0, True, [], [], [], [])
ta_2 = Applicant('2', 3.0, True, [], [], [], [])
ta_3 = Applicant('3', 2.0, False, [], [], [], []) 

courses = [course_a, course_b]
tas = [ta_1, ta_2, ta_3]
edges = [Edge(ta, course) for course in courses for ta in tas]

rankings = {
    course_a: [(Edge(ta_1, course_a), 2), (Edge(ta_2, course_a), 1), (Edge(ta_3, course_a), 2)],
    course_b: [(Edge(ta_1, course_b), 1), (Edge(ta_2, course_b), 0), (Edge(ta_3, course_b), 1)]
} # dictionary where keys are courses and the values are lists of tuples (edge, ranking)

# have rankings be a list of tuples (TA, ranking)
def evaluation_function(course, rankings, vars):
    course_rankings = rankings[course]
    rankings = sorted(course_rankings,key=lambda x: x[1], reverse=True)
    B = rankings[course.ta_req_nbr-1][1]

    denominator = (course.ta_req_nbr * max([np.abs(x[1] - B) for x in rankings])) if (course.ta_req_nbr * max([np.abs(x[1] - B) for x in rankings])) != 0 else course.ta_req_nbr
    value = (1 / denominator) * sum([vars[entry[0]] * (entry[1] - B) for entry in course_rankings])
    return value


def eval_general(course, rankings, tas):
    sorted_val = sorted(list(rankings.values()))
    B = sorted_val[course.ta_req_nbr-1]

    denominator = (course.ta_req_nbr * max([np.abs(rankings[ta] - B) for ta in tas])) if (max([np.abs(rankings[ta] - B) for ta in tas])) != 0 else course.ta_req_nbr
    value = (1 / denominator) * sum([rankings[ta] - B for ta in tas])

    return value

print(eval_general(course_a, {ta_2: 0, ta_3: 1}, [ta_2, ta_3]))

def build_model(courses, rankings, edges):
    model = gp.Model("course_allocation")
    # model.setParam('OutputFlag', 0)

    edge_vars = {}
    for edge in edges:
        edge_vars[edge] = model.addVar(vtype=GRB.BINARY, name=f'assign_{edge.course.id}_{edge.ta.id}')

    m = model.addVar(vtype=GRB.CONTINUOUS, name='m')
    M = model.addVar(vtype=GRB.CONTINUOUS, name='M')
        
    model.addConstrs(gp.quicksum(edge_vars[edge] for edge in edges if edge.ta == ta) == 1 for ta in tas if ta.class_level)
    model.addConstrs(gp.quicksum(edge_vars[edge] for edge in edges if edge.ta == ta) <= 1 for ta in tas if not ta.class_level)
    model.addConstrs(gp.quicksum(edge_vars[edge] for edge in edges if edge.course == course) == course.ta_req_nbr for course in courses)
    model.addConstrs(m <= evaluation_function(course, rankings, edge_vars) for course in courses)
    model.addConstrs(M >= evaluation_function(course, rankings, edge_vars) for course in courses)
    # model.addConstr(M >= m)

    model.setObjective(sum([evaluation_function(course, rankings, edge_vars) for course in courses]), GRB.MAXIMIZE)

    return model, edge_vars

model, edge_vars = build_model(courses, rankings, edges)
model.optimize()

# for v in model.getVars():
#     print(v.varName, v.x)

# print('Optimal objective function value', model.objVal)