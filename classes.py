class Course:
    def __init__(self, id, attributes):
        self.id = id
        self.attributes = attributes

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Course) and self.id == other.id

class Applicant:
    def __init__(self, id, gpa, class_level, courses_taken, skills, prev_exp, pref_courses):
        self.id = id
        self.gpa = gpa
        self.class_level = class_level
        self.courses_taken = courses_taken
        self.skills = skills
        self.prev_exp = prev_exp
        self.pref_courses = pref_courses
    
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Applicant) and self.id == other.id

class Edge:
    def __init__(self, ta_app, course):
        self.ta = ta_app
        self.course = course

class Graph:
    def __init__(self, courses, tas, edges):
        self.adj_list = {course: [] for course in courses}
        self.adj_list.update({ta: [] for ta in tas})
        for e in edges:
            self.add_edge(e)
    
    def add_edge(self, e):
        if e.course not in self.adj_list[e.ta] and e.ta not in self.adj_list[e.course]:
            self.adj_list[e.ta].append(e.course)
            self.adj_list[e.course].append(e.ta)
            print('ta', self.adj_list[e.ta])
            print('course', self.adj_list[e.course])
     
    def remove_edge(self, edge):
        if edge.course in self.ta_adj_list[edge.ta] and edge.ta in self.course_adj_list[edge.course]:
            self.adj_list[edge.ta].remove(edge.course)  
            self.adj_list[edge.course].remove(edge.ta)


class MatchingGraph(Graph):
    def __init__(self, courses, tas, edges):
        super().__init__(courses, tas, edges)
        self.curr_match = dict.fromkeys(self.adj_list.keys(), None)
        self.visited = dict.fromkeys(self.adj_list.keys(), False)
    
    def print_matches(self):
        print("-- Matches --")
        for key in self.curr_match.keys():
            if self.curr_match[key] != None:
                print(key.id + " " + self.curr_match[key].id)
        print("-- Unmatched --")
        for key in self.curr_match.keys():
            if self.curr_match[key] == None:
                print(key.id)

    def add_node(self, node):
        self.adj_list.update({node: []})
        self.curr_match.update({node: None})
        self.visited.update({node: False})