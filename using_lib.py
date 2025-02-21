import networkx as nx
from classes import *
#from valid_matching import *

# Build bipartite graph
def build_bipartite_graph(courses, tas, edges):
    B = nx.Graph()
    
    # Add nodes with the bipartite attribute
    for course in courses:
        B.add_node(course.unique_id(), bipartite=0)  # Courses belong to partition 0
    
    for ta in tas:
        if ta.class_level:
            B.add_node(ta.unique_id(), bipartite=1)  # TAs belong to partition 1

    for edge in edges:
        if edge.edge_ta().class_level:
            B.add_edge(edge.edge_course().unique_id(), edge.edge_ta().unique_id())
    
    return B

def exec_bipartite_matching(courses, tas, edges):
    # Build the bipartite graph
    B = build_bipartite_graph(courses, tas, edges)

    # Perform bipartite matching using NetworkX
    matching = nx.bipartite.maximum_matching(B, top_nodes=[course.unique_id() for course in courses])

    # Print the matching
    print("Initial Matching:")
    for course_id, ta_id in matching.items():
        if isinstance(course_id, str):  # Ensure we only print course-to-TA assignments
            print(f"{course_id} is assigned to {ta_id}")
    
    for ta in tas:
        if not ta.class_level:
            B.add_node(ta.unique_id(), bipartite=1)  # TAs belong to partition 1

    for edge in edges:
        if not edge.edge_ta().class_level:
            B.add_edge(edge.edge_course().unique_id(), edge.edge_ta().unique_id())

    # Perform bipartite matching using NetworkX
    matching = nx.bipartite.maximum_matching(B, top_nodes=[course.unique_id() for course in courses])

    # Print the matching
    print("Final Matching:")
    for course_id, ta_id in matching.items():
        if isinstance(course_id, str):  # Ensure we only print course-to-TA assignments
            print(f"{course_id} is assigned to {ta_id}")