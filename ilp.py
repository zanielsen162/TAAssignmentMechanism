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

model = gp.Model("course_allocation")
model.setParam('OutputFlag', 0)

courses = []
tas = []
edges = [Edge(course, ta) for course in courses for ta in tas]

vars = model.addVars(edges, vtype=GRB.BINARY, name='assign')
m = model.addVars(vtype=GRB.CONTINUOUS, name='m')
M = model.addVars(vtype=GRB.CONTINUOUS, name='M')


def evaluation_function(course, rankings, vars):
    course_rankings = [(edge.ta, rankings[edge]) for edge in rankings if edge.course == course]
    course_rankings = sorted(course_rankings, key=lambda x: x[1], reverse=True)
    B = course_rankings[course.ta_req_nbr - 1][1]
    value = sum([vars[edge] * (x[1] - B) for edge, x in zip(rankings.keys(), course_rankings) if edge.course == course])
    return value

rankings = {} # dictionary where keys are courses and the values are lists of tuples (edge, ranking)

# have rankings be a list of tuples (TA, ranking)
def evaluation_function(course, rankings, vars):
    course_rankings = rankings[course]
    rankings = sorted(course_rankings,key=lambda x: x[1], reverse=True)
    B = rankings[course.num_needed-1][1]

    denominator = (course.num_needed * max([np.abs(x[1] - B) for x in rankings])) if (course.num_needed * max([np.abs(x[1] - B) for x in rankings])) != 0 else course.num_needed
    value = (1 / denominator) * sum([vars[entry[0]] * (entry[1] - B) for entry in course_rankings])
    return value

model.addConstraint(gp.quicksum(vars[edge] for edge in edges if edge.ta == ta) == 1 for ta in tas if ta.class_level)
model.addConstraint(gp.quicksum(vars[edge] for edge in edges if edge.ta == ta) <= 1 for ta in tas if not ta.class_level)
model.addConstraint(gp.quicksum(vars[edge] for edge in edges if edge.course == course) == course.num_needed for course in courses)
model.addConstraint(m <= evaluation_function(course, rankings, vars) for course in courses)
model.addConstraint(M >= evaluation_function(course, rankings, vars) for course in courses)
model.addConstraint(M >= m)


model.setObjective(sum([evaluation_function(course, rankings, vars) for course in courses]) - (M - m), GRB.MAXIMIZE)