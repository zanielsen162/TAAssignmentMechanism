import pandas as pd
from classes import *
import gurobipy as gp
from gurobipy import GRB

def format_dfs(courses_df, applicants_df, rankings_df):
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

    return courses, tas, rankings, edges

def print_output(model, edge_vars, tas):
    if model.status == GRB.OPTIMAL:
        final_matchings = []
        print("Final Matchings:")
        for edge, var in edge_vars.items():
            if var.X == 1:  # Check if the variable is set to 1 (assigned)
                final_matchings.append(edge)
                print(f"TA {edge.ta.id} is assigned to Course {edge.course.id}")
        print('Optimal objective function value:', model.objVal)

        # Check which TAs in the range are matched
        matched_tas = [ match.ta for match in final_matchings ]
        unmatched_tas = [ ta for ta in tas if ta not in matched_tas ]
    else:
        print("No optimal solution found.")