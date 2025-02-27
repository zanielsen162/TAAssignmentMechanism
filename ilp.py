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

# Read CSV files
import pandas as pd
from classes import Course, Applicant, Edge

# Read CSV files
courses_df = pd.read_csv('course test - courses.csv')
applicants_df = pd.read_csv('course test - applicants.csv')
rankings_df = pd.read_csv('course test - ranking.csv')

# Create Course objects
courses = []
for _, row in courses_df.iterrows():
    course_id = row['course']
    skills = row['skills'].split(',') if pd.notna(row['skills']) else []
    ta_req_nbr = row['TAs_req']
    preferred_tas = row['pref'].split(',') if pd.notna(row['pref']) else []
    courses.append(Course(course_id, skills, ta_req_nbr, preferred_tas))

# Create Applicant objects
tas = []
for _, row in applicants_df.iterrows():
    ta_id = row['id']
    gpa = row['gpa']
    class_level = row['class']
    courses_taken = row['courses_taken'].split(',') if pd.notna(row['courses_taken']) else []
    skills = row['skills'].split(',') if pd.notna(row['skills']) else []
    prev_exp = row['prev_exp'].split(',') if pd.notna(row['prev_exp']) else []
    pref_courses = row['pref_courses'].split(',') if pd.notna(row['pref_courses']) else []
    tas.append(Applicant(ta_id, gpa, class_level, courses_taken, skills, prev_exp, pref_courses))

# Create rankings dictionary
rankings = {}
for _, row in rankings_df.iterrows():
    course_id = row['course']
    ta_id = row['ta']
    ranking = row['ranking']

    # Find the corresponding Course and Applicant objects
    course = next((c for c in courses if c.id == course_id), None)
    ta = next((t for t in tas if t.id == ta_id), None)

    if course and ta:
        edge = Edge(ta, course)
        if course not in rankings:
            rankings[course] = []
        rankings[course].append((edge, ranking))

# Create edges (all possible TA-course pairs)
edges = [Edge(ta, course) for course in courses for ta in tas]

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

#print(eval_general(course_a, {ta_2: 0, ta_3: 1}, [ta_2, ta_3]))

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
if model.status == GRB.OPTIMAL:
    print("Final Matchings:")
    for edge, var in edge_vars.items():
        if var.X > 0.5:  # Check if the variable is set to 1 (assigned)
            print(f"TA {edge.ta.id} is assigned to Course {edge.course.id}")
    print('Optimal objective function value:', model.objVal)
else:
    print("No optimal solution found.")

final_matchings = []
for edge, var in edge_vars.items():
    if var.X > 0.5:  # Check if the variable is set to 1 (assigned)
        final_matchings.append((edge.ta.id, edge.course.id))

# Define the range of TAs to check (TA_1 to TA_..)
tas_to_check = [f"TA_{i}" for i in range(1, 66)]

# Check which TAs in the range are matched
matched_tas = [ta for ta, course in final_matchings if ta in tas_to_check]
unmatched_tas = [ta for ta in tas_to_check if ta not in matched_tas]

# Print results
print("Matched TAs (TA_1 to TA_65):")
for ta in matched_tas:
    print(ta)

print("\nUnmatched TAs (TA_1 to TA_65):")
for ta in unmatched_tas:
    print(ta)