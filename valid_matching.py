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
        if graph.curr_match[visit] == None or try_augmenting_path(graph, visit):
            graph.curr_match[visit] = node
            graph.curr_match[node] = visit
            return True
    return False

def matching(graph):
    for val in graph.adj_list.keys():
        graph.visited = dict.fromkeys(graph.visited.keys(), False)
        try_augmenting_path(graph, val)
    return graph

ta_1 = Applicant("1", 3.5, "Junior", ["CS 225", "CS 173"], ["Python", "Java"], ["CS 173"], ["CS 225", "CS 173"])
ta_2 = Applicant("2", 3.8, "Senior", ["CS 225", "CS 173"], ["Python", "Java"],  ["CS 225"], ["CS 225", "CS 173"])
ta_3 = Applicant("3", 3.6, "Junior", ["CS 225", "CS 173"], ["Python", "Java"],  [], ["CS 225", "CS 173"])

course_1 = Course("CS 225", ["Python", "Java"])
course_2 = Course("CS 173", ["Python", "Java"])

edge_1 = Edge(ta_1, course_1)
edge_2 = Edge(ta_1, course_2)
edge_3 = Edge(ta_2, course_1)
edge_4 = Edge(ta_2, course_2)
edge_5 = Edge(ta_3, course_1)
edge_6 = Edge(ta_3, course_2)

graph = Matching([course_1, course_2], [ta_1, ta_2, ta_3], [edge_1, edge_2, edge_3, edge_4, edge_5, edge_6])
matching(graph)
graph.print_matches()

# issue: courses can get matched to courses