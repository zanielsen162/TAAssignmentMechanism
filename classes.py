class Course:
    def __init__(self, id, attributes):
        self.id = id
        self.attributes = attributes

class Applicant:
    def __init__(self, id, gpa, class_level, courses_taken, skills, prev_exp, pref_courses):
        self.id = id
        self.gpa = gpa
        self.class_level = class_level
        self.courses_taken = courses_taken
        self.skills = skills
        self.prev_exp = prev_exp
        self.pref_courses = pref_courses

class Edge:
    def __init__(self, ta_app, course):
        self.ta = ta_app
        self.course = course

class Graph:
    def __init__(self, courses, tas, edges):
        self.adj_list = dict.fromkeys(tas + courses, [])
        for e in edges:
            self.add_edge(e)
    
    def add_edge(self, e):
        if e.course not in self.adj_list[e.ta.id] and e.ta not in self.adj_list[e.course.id]:
            self.adj_list[e.ta.id].append(e.course)
            self.adj_list[e.course.id].append(e.ta)
     
    def remove_edge(self, edge):
        if edge.course in self.ta_adj_list[edge.ta.id] and edge.ta in self.course_adj_list[edge.course.id]:
            self.adj_list[edge.ta.id].remove(edge.course)  
            self.adj_list[edge.course.id].remove(edge.ta)

class Matching(Graph):
    def __init__(self, courses, tas, edges):
        super().__init__(courses, tas, edges)
        self.curr_match = dict.fromkeys(tas + courses, None)
        self.matched = 0
        self.visited = dict.fromkeys(tas + courses, False)