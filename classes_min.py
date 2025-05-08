class Graph_Vertex:
    def __init__(self):
        pass

    def key_str(self):
        return "dummy"
    
class Course(Graph_Vertex):
    def __init__(self, id, attributes,  ta_req_nbr, pref_tas = []):
        self.id = id
        self.attributes = attributes
        self.ta_req_nbr = ta_req_nbr
        self.pref_tas = pref_tas

    def unique_id(self):
        return str(self.id) + "-" + str(self.ta_req_nbr)

    def key_str(self):
        return f"Course={self.id}, Instance={self.ta_req_nbr}"

    def __hash__(self):
        return hash(self.id + str(self.ta_req_nbr))

    def __eq__(self, other):
        return isinstance(other, Course) and self.id == other.id and self.ta_req_nbr == other.ta_req_nbr 

class Applicant(Graph_Vertex):
    def __init__(self, id, gpa, class_level, courses_taken, skills, prev_exp, pref_courses):
        self.id = id
        self.gpa = gpa
        self.class_level = class_level
        self.courses_taken = courses_taken
        self.skills = skills
        self.prev_exp = prev_exp
        self.pref_courses = pref_courses
    
    def unique_id(self):
        return str(self.id)
    
    def key_str(self):
        return f"TA={self.id}"
    
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Applicant) and self.id == other.id


class Edge:
    def __init__(self, ta_app, course: Course):
        self.ta = ta_app
        self.course = course

    def edge_course(self):
        return self.course
    
    def edge_ta(self):
        return self.ta
