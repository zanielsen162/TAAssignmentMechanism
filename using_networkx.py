import networkx as nx

# Define the data structures
class CourseRequirement:
    def __init__(self, course_id, TAreqd, preferred_tas):
        self.course_id = course_id
        self.TAreqd = TAreqd
        self.preferred_tas = preferred_tas

class TeachAssistant:
    def __init__(self, Id, pref_courses):
        self.Id = Id
        self.pref_courses = pref_courses

# Example data
ta_1 = TeachAssistant(Id=1, pref_courses=["BIO1", "BIO32", "CHEM2"])
ta_2 = TeachAssistant(Id=2, pref_courses=["BIO1", "PHY21", "MATH91"])
ta_3 = TeachAssistant(Id=3, pref_courses=["BIO1", "PHY21", "CHEM2"])
ta_4 = TeachAssistant(Id=4, pref_courses=["BIO1", "PHY21", "MATH91"])
ta_5 = TeachAssistant(Id=5, pref_courses=["PHY21", "CHEM2", "MATH91"])
ta_21 = TeachAssistant(Id=21, pref_courses=["PHY21", "BIO1", "CHEM2"])

course_1 = CourseRequirement(course_id="BIO1", TAreqd=2, preferred_tas=[ta_1, ta_3, ta_4])
course_2 = CourseRequirement(course_id="PHY21", TAreqd=4, preferred_tas=[ta_1, ta_3, ta_4, ta_5, ta_21])

# List of courses and TAs
courses = [course_1, course_2]
tas = [ta_1, ta_2, ta_3, ta_4, ta_5, ta_21]

# Build bipartite graph
def build_bipartite_graph(courses, tas):
    B = nx.Graph()
    
    # Add nodes with the bipartite attribute
    for course in courses:
        B.add_node(course.course_id, bipartite=0)  # Courses belong to partition 0
    
    for ta in tas:
        B.add_node(ta.Id, bipartite=1)  # TAs belong to partition 1
    
    # Add edges between courses and TAs if they mutually prefer each other
    for course in courses:
        for ta in course.preferred_tas:
            if course.course_id in ta.pref_courses:
                B.add_edge(course.course_id, ta.Id)
    
    return B

# Build the bipartite graph
B = build_bipartite_graph(courses, tas)

# Perform bipartite matching using NetworkX
matching = nx.bipartite.maximum_matching(B, top_nodes=[course.course_id for course in courses])

# Print the matching
print("Initial Matching:")
for course_id, ta_id in matching.items():
    if isinstance(course_id, str):  # Ensure we only print course-to-TA assignments
        print(f"Course {course_id} is assigned to TA {ta_id}")
