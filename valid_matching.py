from collections.abc import Iterable
from classes import *

# int n, k;
# vector<vector<int>> g;
# vector<int> mt;
# vector<bool> used;

# bool try_kuhn(int v) {
#     if (used[v])
#         return false;
#     used[v] = true;
#     for (int to : g[v]) {
#         if (mt[to] == -1 || try_kuhn(mt[to])) {
#             mt[to] = v;
#             return true;
#         }
#     }
#     return false;
# }

# int main() {
#     //... reading the graph ...

#     mt.assign(k, -1);
#     for (int v = 0; v < n; ++v) {
#         used.assign(n, false);
#         try_kuhn(v);
#     }

#     for (int i = 0; i < k; ++i)
#         if (mt[i] != -1)
#             printf("%d %d\n", mt[i] + 1, i + 1);
# }

# represents the course requirement as specified by the dept/prof
class CourseRequirement: 
    def __init__(self, id, attributes, requred_ta_count):
        self.id = id
        self.attributes = attributes
        self.required_ta_count = requred_ta_count

# Function to find an augmenting path in the matching graph
# If it finds an augmenting path, then it should flip the edges in the path

def try_augmenting_path(graph, node):
    if (graph.visited[node]):
        return False
    graph.visited[node] = True
    for visit in graph.adj_list[node]:
        if graph.curr_match[visit] is None or try_augmenting_path(graph, graph.curr_match[visit]):
            graph.curr_match[visit] = node
            graph.curr_match[node] = visit
            return True
    return False

def matching(graph):
    for val in graph.adj_list.keys():
        graph.visited = dict.fromkeys(graph.visited.keys(), False)
        try_augmenting_path(graph, val)
    return graph

def complete_matching(applicant_list, course_list, edge_list):
    #--------- phd applicants----------------
    phd_applicant_list = [student for student in applicant_list if student.class_level]
    edge_list = [edge for edge in edge_list if edge.ta.class_level]

    final_graph = MatchingGraph(course_list, phd_applicant_list, edge_list)
    
    final_graph = matching(final_graph)
    
    if not final_graph.check_phd_matched():
        return 'No valid matching'

    #-------------masters applicants -----------------
    masters_applicant_list = [student for student in applicant_list if student.class_level is False]
    masters_edge_list = [edge for edge in edge_list if edge.ta.class_level is False]

    for student in masters_applicant_list: 
        final_graph.add_node(student)
    
    for edge in masters_edge_list: 
        final_graph.add_edge(edge)

    final_graph = matching(final_graph)
    
    if not final_graph.check_courses_matched():
        return 'No valid matching'

    return final_graph

def get_courses_and_edges(course_requirement_list, ta_list):
    courses = []
    edges = []

    for cr in course_requirement_list:  # [("170",'', 13). (50,"", 2)]
        for i in range(cr.required_ta_count):
            new_course =Course(cr.id, cr.attributes, i + 1)
            courses.append(new_course)
            for ta in ta_list:
                if cr.id in ta.pref_courses:
                    edges.append(Edge(ta, new_course))

    dummy_ta_list = []
    if (len(courses) > len(ta_list)):
        for i in range(len(courses) - len(ta_list)):
            dummy_ta_list.append(Applicant("dummy" + str(i), 1, True, [], [], [], []))


    '''
    print ("Courses")
    for x in courses:
        print ((x.id, x.ta_req_nbr))
        
    print("Edges")
    for y in edges:
        print(y.ta.id, y.ta.courses_taken, y.course.id, y.course.ta_req_nbr)
        '''

    return courses, edges, ta_list # + dummy_ta_list        
        

ta_1 = Applicant("1", 3.5, True, ["CS 225", "CS 173", "CS173"], ["Python", "Java"], ["CS 173"], ["CS 225", "CS 173"])
ta_2 = Applicant("2", 3.8, True, ["CS 225", "CS 173"], ["Python", "Java"],  ["CS 225"], ["CS 225", "CS 173"])
ta_3 = Applicant("3", 3.6, True, ["CS 225", "CS 173"], ["Python", "Java"],  [], ["CS 225", "CS 173"])

# CourseRequirement - holds Course Information and number of TAs required for the course
# Eventually, for every TA required an instance of this Course will be created 
# Each instance of Course then qualifies as a node/vertex in the graph
course_1 = CourseRequirement("CS 225", ["Python", "Java"], 2) # will result in 1 instance of Course object
course_2 = CourseRequirement("CS 173", ["Python", "Java"], 4)  # will result in 3 instance of Course object

course_list, edge_list, ta_list_incl_dummies = get_courses_and_edges ([course_1, course_2], [ta_1, ta_2, ta_3])
#course_list, edge_list = get_courses_edges ([course_1, course_2], [edge_1, edge_2, edge_3, edge_4, edge_5, edge_6])
#print ('course list', [x for x in course_list])
#print ('edge list', edge_list)
graph = MatchingGraph(course_list, ta_list_incl_dummies, edge_list)
matching(graph)
graph.print_matches()
print('---')
final_graph = complete_matching(ta_list_incl_dummies, course_list, edge_list)

try:
    final_graph.print_matches()
except:
    print(final_graph)
