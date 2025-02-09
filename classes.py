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
        self.ta_adj_list = dict.fromkeys(tas, [])
        self.course_adj_list = dict.fromkeys(courses, [])
        for e in edges:
            if e.course not in self.ta_adj_list[e.ta]:
                self.ta_adj_list[e.ta].append(e.course)
            if e.ta not in self.course_adj_list[e.course]:
                self.course_adj_list[e.course].append(e.ta)
    
    def add_edge(self, new_edge):
        if new_edge.course not in self.ta_adj_list[new_edge.ta]:
            self.ta_adj_list[new_edge.ta].append(new_edge.course)
        if new_edge.ta not in self.course_adj_list[new_edge.course]:
            self.course_adj_list[new_edge.course].append(new_edge.ta)
     
    def remove_edge(self, edge):
        if edge.course in self.ta_adj_list[edge.ta]:
            self.ta_adj_list[edge.ta].remove(edge.course)  
        if edge.ta in self.course_adj_list[edge.course]:
            self.course_adj_list[edge.course].remove(edge.ta)
