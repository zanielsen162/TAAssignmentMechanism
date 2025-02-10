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
    if (graph.visited[node.id]):
        return False
    graph.visited[node.id] = True
    for visit in graph.ta_adj_list[node.id]:
        if graph.curr_match[visit.id] == None or try_augmenting_path(visit):
            graph.curr_match[visit.id] = node
            graph.curr_match[node.id] = visit
            return True
    return False

def matching(graph):
    for 