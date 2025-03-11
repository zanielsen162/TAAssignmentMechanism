import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
from classes import *
from loading_data_ilp import *

# Construct the model
# Input: 
#   list of courses with number of needed applicants and rankings
#   list of applicants
#   list of edges between courses and applicants
# Output:
#   solution of the optimization problem

# have rankings be a list of tuples (TA, ranking)
def evaluation_function(course, rankings, vars):
    course_rankings = rankings[course]
    rankings = sorted(course_rankings,key=lambda x: x[1], reverse=True)
    B = rankings[course.ta_req_nbr-1][1]

    denominator = (course.ta_req_nbr * max([np.abs(x[1] - B) for x in rankings])) if (course.ta_req_nbr * max([np.abs(x[1] - B) for x in rankings])) != 0 else course.ta_req_nbr
    value = (1 / denominator) * sum([vars[entry[0]] * (entry[1] - B) for entry in course_rankings])
    return value

# for my own testing
def eval_general(course, rankings, tas):
    sorted_val = sorted(rankings[course],key=lambda x: x[1], reverse=True)
    B = sorted_val[course.ta_req_nbr-1]

    denominator = (course.ta_req_nbr * max([np.abs(rankings[ta] - B) for ta in tas])) if (max([np.abs(rankings[ta] - B) for ta in tas])) != 0 else course.ta_req_nbr
    value = (1 / denominator) * sum([rankings[ta] - B for ta in tas])

    return value

# function that given the courses, rankings, and available matching constructs the ILP
def build_model(courses, rankings, edges, tas):
    model = gp.Model("course_allocation")
    model.setParam('OutputFlag', 0)

    edge_vars = {}
    for edge in edges:
        edge_vars[edge] = model.addVar(vtype=GRB.BINARY, name=f'assign_{edge.course.id}_{edge.ta.id}')

    # m = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name='m')
    # M = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name='M')
        
    model.addConstrs(gp.quicksum(edge_vars[edge] for edge in edges if edge.ta == ta) == 1 for ta in tas if ta.class_level)
    model.addConstrs(gp.quicksum(edge_vars[edge] for edge in edges if edge.ta == ta) <= 1 for ta in tas if not ta.class_level)
    model.addConstrs(gp.quicksum(edge_vars[edge] for edge in edges if edge.course == course) == course.ta_req_nbr for course in courses)
    # model.addConstrs(m <= evaluation_function(course, rankings, edge_vars) for course in courses)
    # model.addConstrs(M >= evaluation_function(course, rankings, edge_vars) for course in courses)

    model.setObjective(sum([evaluation_function(course, rankings, edge_vars) for course in courses]), GRB.MAXIMIZE)

    return model, edge_vars

# version with 1-norm minimized by threshold, function that given the courses, rankings, and available matching constructs the ILP
def build_model_min_var(courses, rankings, edges, threshold, tas):
    model = gp.Model("course_allocation")
    model.setParam('OutputFlag', 0)

    edge_vars = {}
    for edge in edges:
        edge_vars[edge] = model.addVar(vtype=GRB.BINARY, name=f'assign_{edge.course.id}_{edge.ta.id}')
        
    model.addConstrs(gp.quicksum(edge_vars[edge] for edge in edges if edge.ta == ta) == 1 for ta in tas if ta.class_level)
    model.addConstrs(gp.quicksum(edge_vars[edge] for edge in edges if edge.ta == ta) <= 1 for ta in tas if not ta.class_level)
    model.addConstrs(gp.quicksum(edge_vars[edge] for edge in edges if edge.course == course) == course.ta_req_nbr for course in courses)

    model.addConstrs(gp.quicksum(evaluation_function(course, rankings, edge_vars) for course in courses) - edge_vars[edge] <= threshold for edge in edges)
    model.addConstrs(edge_vars[edge] - gp.quicksum(evaluation_function(course, rankings, edge_vars) for course in courses) <= threshold for edge in edges)
    model.setObjective(sum([evaluation_function(course, rankings, edge_vars) for course in courses]), GRB.MAXIMIZE)

    return model, edge_vars


# Sample of how to run
#
courses_df = pd.read_csv('/Users/zoeynielsen/Desktop/CMPTGCS/CMPSC 110/TAAssignmentMechanism/testing-data/course test - courses.csv')
applicants_df = pd.read_csv('/Users/zoeynielsen/Desktop/CMPTGCS/CMPSC 110/TAAssignmentMechanism/testing-data/course test - applicants.csv')
rankings_df = pd.read_csv('/Users/zoeynielsen/Desktop/CMPTGCS/CMPSC 110/TAAssignmentMechanism/testing-data/course test - ranking.csv')

courses, tas, rankings, edges = format_dfs(courses_df, applicants_df, rankings_df)

# model, edge_vars = build_model_min_var(courses, rankings, edges, 0.8, tas)
# model.optimize()
# print_output(model, edge_vars, tas)
# print('----')
model, edge_vars = build_model(courses, rankings, edges, tas)
model.optimize()
print_output(model, edge_vars, tas)
