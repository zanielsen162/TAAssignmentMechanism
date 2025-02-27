#course needs 1 TA, provided 3 preferences
#course needs 2 TA, provided 5 Preferences
#course needs 3 TA, provided 7 preference
#course needs 4 TA, provided 9 preferences
#edge if the course preferred a TA and a higher ranking is assigned if the course was also in TA preferenes

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

# Print rankings with ranking number and edge
print("Rankings:")
for course, ranking_list in rankings.items():
    print(f"Course: {course.id}")
    for edge, ranking in ranking_list:
        print(f"  TA: {edge.ta.id}, Ranking: {ranking}")

# Create edges (all possible TA-course pairs)
edges = [Edge(ta, course) for course in courses for ta in tas]

# Now you can use the `courses`, `tas`, `rankings`, and `edges` in your ILP code
# For example:
# model, edge_vars = build_model(courses, rankings, edges)
# model.optimize()