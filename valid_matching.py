from collections.abc import Iterable
from classes import *
import queue

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
    for val in graph.courses:
        graph.visited = dict.fromkeys(graph.visited.keys(), False)
        try_augmenting_path(graph, val)
    return graph

def complete_matching(applicant_list, course_list, edge_list):
    #--------- phd applicants----------------
    phd_applicant_list = [student for student in applicant_list if student.class_level]
    edge_list_temp = [edge for edge in edge_list if edge.ta.class_level]

    final_graph = MatchingGraph(course_list, phd_applicant_list, edge_list_temp)
    
    final_graph = matching(final_graph)
    
    if not final_graph.check_phd_matched():
        print('No valid matching, phd')
        return None

    #-------------masters applicants -----------------
    masters_applicant_list = [student for student in applicant_list if student.class_level is False]
    masters_edge_list = [edge for edge in edge_list if edge.ta.class_level is False]


    for student in masters_applicant_list: 
        final_graph.add_node(student)
    
    for edge in masters_edge_list: 
        final_graph.add_edge(edge)

    for edge in final_graph.adj_list.keys():
        print(edge.id, ':')
        for val in final_graph.adj_list[edge]:
            print('     ',val.id)

    final_graph.visited = dict.fromkeys(final_graph.visited.keys(), False)

    comp_graph = MatchingGraph(course_list, applicant_list, edge_list)
    
    print('adj_list same?', comp_graph.adj_list == final_graph.adj_list)
    print('curr_match same?', comp_graph.curr_match == final_graph.curr_match)
    print('curr_match keys same?', comp_graph.curr_match.keys() == final_graph.curr_match.keys())
    print('visited same?', comp_graph.visited == final_graph.visited) # visited should be the same

    print('---POST MASTERS---')
    final_graph = matching(final_graph)
    final_graph.print_matches()
    print('-------------------')

    
    if not final_graph.check_courses_matched():
        print('No valid matching, courses')
        return None

    return final_graph

def get_courses_and_edges(course_requirement_list, ta_list):
    courses = []
    edges = []

    for cr in course_requirement_list:  # [("170",'', 13). (50,"", 2)]
        for i in range(cr.required_ta_count):
            new_course = Course(cr.id + ' ' + str(i), cr.attributes, i + 1)
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


def get_processed_data(course_requirement_list, ta_list):
    courses = []
    edges = []
    
    for cr in course_requirement_list:  # [("170",'', 13). (50,"", 2)]
        for i in range(cr.required_ta_count):
            new_course =Course(cr.id, cr.attributes, i + 1)
            courses.append(new_course)
            for ta in ta_list:
                if cr.id in ta.pref_courses and ta.id in cr.pref_tas:
                    edges.append(Edge(ta, new_course))

def flip_edges(graph, v, first_node = False):
    iter_v = v 
    while first_node or hasattr(iter_v, 'parent') and iter_v.parent is not None: 
        if graph.curr_match[iter_v.parent] != iter_v:
            graph.curr_match[iter_v.parent] = iter_v
            graph.curr_match[iter_v] = iter_v.parent
        iter_v = iter_v.parent

def try_augmenting_path_bfs(graph, v):
    queue = [v]
    graph.visited[v] = True
    first_node = True
    while queue:
        u = queue.pop(0)
        if u in graph.courses:
            if graph.curr_match[u] is not None:
                w = graph.curr_match[u]
                if not graph.visited[w]:
                    graph.visited[w] = True
                    queue.append(w)
                    w.parent = u
            else:
                flip_edges(graph, u, first_node)
                first_node = False
                return True

        elif u in graph.tas:
            if graph.curr_match[u] is not None:
                for w in graph.adj_list[u]:
                    if w not in graph.curr_match[u] and not graph.visited[w]:
                        graph.visited[w] = True
                        queue.append(w)
            else:
                for w in graph.adj_list[u]:
                    if not graph.visited[w]:
                        graph.visited[w] = True
                        queue.append(w)
                        w.parent = u
    return graph





# ta_1 = Applicant("1", 3.5, True, ["CS 225", "CS 173", "CS173"], ["Python", "Java"], ["CS 173"], ["CS 225", "CS 173"])
# ta_2 = Applicant("2", 3.8, True, ["CS 225", "CS 173"], ["Python", "Java"],  ["CS 225"], ["CS 225", "CS 173"])
# ta_3 = Applicant("3", 3.6, True, ["CS 225", "CS 173"], ["Python", "Java"],  [], ["CS 225", "CS 173"])

# CourseRequirement - holds Course Information and number of TAs required for the course
# Eventually, for every TA required an instance of this Course will be created 
# Each instance of Course then qualifies as a node/vertex in the graph
# course_1 = CourseRequirement("CS 225", ["Python", "Java"], 2) # will result in 1 instance of Course object
# course_2 = CourseRequirement("CS 173", ["Python", "Java"], 4)  # will result in 3 instance of Course object

# course_list, edge_list, ta_list_incl_dummies = get_courses_and_edges ([course_1, course_2], [ta_1, ta_2, ta_3])


#course_list, edge_list = get_courses_edges ([course_1, course_2], [edge_1, edge_2, edge_3, edge_4, edge_5, edge_6])
#print ('course list', [x for x in course_list])
#print ('edge list', edge_list)



# graph = MatchingGraph(course_list, ta_list_incl_dummies, edge_list)
# matching(graph)
# graph.print_matches()
# print('---')
# final_graph = complete_matching(ta_list_incl_dummies, course_list, edge_list)

# try:
#     final_graph.print_matches()
# except:
#     print(final_graph)
