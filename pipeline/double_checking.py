import networkx as nx
import pandas as pd
from networkx.algorithms import bipartite

# Load data
df = pd.read_csv("real-data-runs/test-sets/prof_preferences_rankings.csv")

# Build bipartite graph
B = nx.Graph()
courses = df['course'].unique()
applicants = df['ta'].unique()

B.add_nodes_from(courses, bipartite=0)
B.add_nodes_from(applicants, bipartite=1)

# Add edges (preferences)
for _, row in df.iterrows():
    B.add_edge(row['course'], row['ta'], weight=row['ranking'])

# Get bipartite node sets
course_nodes = [n for n, d in B.nodes(data=True) if d['bipartite'] == 0]
applicant_nodes = [n for n, d in B.nodes(data=True) if d['bipartite'] == 1]

# Compute maximum matching
matching = bipartite.maximum_matching(B, top_nodes=course_nodes)

# Convert matching to dictionary for easier access
matching_dict = {course: applicant for course, applicant in matching.items() if course in course_nodes}

# Count how many courses are matched
matched_courses = list(matching_dict.keys())

# Report results
print(f"Matched {len(matched_courses)} out of {len(course_nodes)} courses.")

if len(matched_courses) == len(course_nodes):
    print("✅ A perfect matching exists — every course is matched to an applicant.")
else:
    print("❌ No perfect matching — some courses could not be matched.")

# Print the matching
print("\nMatching:")
for course, applicant in matching_dict.items():
    print(f"{course} <--> {applicant}")
