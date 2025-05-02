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
courses_df = pd.read_csv('ACourse2.csv')
applicants_df = pd.read_csv('ATA2.csv')
rankings_df = pd.read_csv('AEdges.csv')

print("\nDebugging Information:")
print("Courses CSV columns:", courses_df.columns.tolist())
print("Applicants CSV columns:", applicants_df.columns.tolist())
print("Rankings CSV columns:", rankings_df.columns.tolist())

# Create Course objects
courses = []
for _, row in courses_df.iterrows():
    course_id = row['course']
    skills = row['skills'].split(',') if pd.notna(row['skills']) else []
    ta_req_nbr = row['TAs_req']
    courses.append(Course(course_id, skills, ta_req_nbr, []))

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

# Create edges and rankings from the rankings file
edges = []
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
        edges.append(edge)
        if course not in rankings:
            rankings[course] = []
        rankings[course].append((edge, ranking))
    else:
        print(f"Warning: Could not find match for course_id={course_id} or ta_id={ta_id}")

print("\nAll Edges:")
for edge in edges:
    print(f"TA {edge.ta.id} -> Course {edge.course.id}")

print("\nRankings:")
for course, ranked_edges in rankings.items():
    print(f"Course {course.id}:")
    for edge, rank in sorted(ranked_edges, key=lambda x: x[1]):  # Sorting by ranking
        print(f"  TA {edge.ta.id} -> Rank {rank}")

# Print the number of edges created
print(f"Number of edges: {len(edges)}")

# Print courses that don't have any rankings
print("\nCourses without rankings:")
for course in courses:
    if course not in rankings:
        print(f"Course {course.id} has no rankings")
    else:
        print(f"Course {course.id} has {len(rankings[course])} rankings")

# Print courses that have rankings
print("\nCourses with rankings:")
for course in rankings:
    print(f"Course {course.id} has {len(rankings[course])} rankings")


