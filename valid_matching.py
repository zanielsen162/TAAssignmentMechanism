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
    phd_applicant_list = [student for student in applicant_list if student.class_level]
    edge_list = [edge for edge in edge_list if edge.ta.class_level]

    final_graph = MatchingGraph(course_list, phd_applicant_list, edge_list)
    
    matching(final_graph)
    
    if not final_graph.check_phd_matched():
        return 'No valid matching'

    masters_applicant_list = [student for student in applicant_list if student.class_level is False]
    masters_edge_list = [edge for edge in edge_list if edge.ta.class_level is False]

    for student in masters_applicant_list: 
        final_graph.add_node(student)
    
    for edge in masters_edge_list: 
        final_graph.add_edge(edge)

    matching(final_graph)
    
    if not final_graph.check_courses_matched():
        return 'No valid matching'

    return final_graph

def get_courses_and_edges(course_req_list: Iterable[CourseReq], course_ta_edge_list: Iterable[CourseTAEdge]):
    courses = []
    edges = []

    course_ta_dict = {}
    for cte in course_ta_edge_list:
        if cte.course_req in course_ta_dict:
            course_ta_dict[cte.course_req].append(cte.ta)
        else:
            course_ta_dict[cte.course_req] = [cte.ta]

    for c in course_req_list:
        for seq in range(c.required_ta_count):
            course = Course(c.id, seq + 1, c.attributes)
            courses.append(course)
            if c in course_ta_dict:
                for ta in course_ta_dict[c]:
                    edges.append(Edge(ta, course))
                    
    return courses, edges

ta_1 = Applicant("1", 3.5, True, ["CS 225", "CS 173", "CS173"], ["Python", "Java"], ["CS 173"], ["CS 225", "CS 173"])
ta_2 = Applicant("2", 3.8, True, ["CS 225", "CS 173"], ["Python", "Java"],  ["CS 225"], ["CS 225", "CS 173"])
ta_3 = Applicant("3", 3.6, True, ["CS 225", "CS 173"], ["Python", "Java"],  [], ["CS 225", "CS 173"])

course_1 = CourseReq("CS 225", ["Python", "Java"], 1) 
course_2 = CourseReq("CS 173", ["Python", "Java"], 3) 

edge_1 = CourseTAEdge(ta_1, course_1)
edge_2 = CourseTAEdge(ta_1, course_2)
edge_3 = CourseTAEdge(ta_2, course_1)
edge_4 = CourseTAEdge(ta_2, course_2)
edge_5 = CourseTAEdge(ta_3, course_1)
edge_6 = CourseTAEdge(ta_3, course_2)

course_list, edge_list = get_courses_and_edges ([course_1, course_2], [edge_1, edge_2, edge_3, edge_4, edge_5, edge_6])
#print ('course list', [x for x in course_list])
#print ('edge list', edge_list)
graph = MatchingGraph(course_list, [ta_1, ta_2, ta_3], edge_list)
matching(graph)
graph.print_matches()
print('---')
final_graph = complete_matching([ta_1, ta_2, ta_3], course_list, edge_list)

try:
    final_graph.print_matches()
except:
    print(final_graph)