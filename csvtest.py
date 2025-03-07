#course needs 1 TA, provided 3 preferences
#course needs 2 TA, provided 5 Preferences
#course needs 3 TA, provided 7 preference
#course needs 4 TA, provided 9 preferences
#edge if the course preferred a TA and a higher ranking is assigned if the course was also in TA preferenes
#in applicants TAs 1-40 are PHD
import pandas as pd
from classes import *
from valid_matching import *

# Read CSV files
courses_df = pd.read_csv('test3c.csv')
applicants_df = pd.read_csv('test3a.csv')
rankings_df = pd.read_csv('test3r.csv')

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

# Create edges (all possible TA-course pairs)
edges = []
for course in courses:
    preferred_tas = course.pref_tas  # List of preferred TA IDs for this course
    for ta in tas:
        if ta.id in preferred_tas:  # Only create an edge if the TA is preferred by the course
            edges.append(Edge(ta, course))

print("All Edges:")
for edge in edges:
    print(f"TA {edge.ta.id} -> Course {edge.course.id}")

# Create a mapping of (ta.id, course.id) to Edge objects
edge_map = {(edge.ta.id, edge.course.id): edge for edge in edges}

# Create rankings dictionary
rankings = {}
for _, row in rankings_df.iterrows():
    course_id = row['course']
    ta_id = row['ta']
    ranking = row['ranking']

    # Find the corresponding Edge object using the mapping
    edge = edge_map.get((ta_id, course_id))
    if edge:
        if edge.course not in rankings:
            rankings[edge.course] = []
        rankings[edge.course].append((edge, ranking))

print("\nRankings:")
for course, ranked_edges in rankings.items():
    print(f"Course {course.id}:")
    for edge, rank in sorted(ranked_edges, key=lambda x: x[1]):  # Sorting by ranking
        print(f"  TA {edge.ta.id} -> Rank {rank}")

# Print the number of edges created
print(f"Number of edges: {len(edges)}")


