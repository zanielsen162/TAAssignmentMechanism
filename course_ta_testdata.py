import random

class TestData:

    def __init__(self, courses, extra_tas, extra_ta_per_course = 2):
        self._courses = courses # nbr of courses 
        self._extra_tas = extra_tas # nbr of extra tas (more tas then data)
        self._tas_requred_count = 0 # this is initally 0 but will hold the total counts of TA's required based on course data
        self._extra_ta_per_course = 2
        self._course_list = []
        self._ta_list = []
        self._course_instance_list = []

    def _generate_courses(self):

        self._tas_requred_count = 0
        course_list =[]
        nbr_ta_req = 0
        course_ta_pref_list = None
        for i in range(self._courses):
            nbr_ta_req = random.randrange(1, 7)
            self._tas_requred_count += nbr_ta_req
            course_ta_pref_list = []
            #for j in range(nbr_ta_req):
            #    course_ta_pref_list.append("TA" + str(random.randrange(1, 100)))
            course_list.append(("C" + str((i + 1) * 5), nbr_ta_req, course_ta_pref_list))
        
        self._tas_requred_count += self._extra_tas
        self._course_list = course_list
        return course_list

    def _generate_tas(self):
        
        ta_list =[]
        nbr_pref_courses = 0
        ta_course_pref_list = None
        for i in range(self._tas_requred_count):
            nbr_pref_courses = random.randrange(3, 7)
            ta_course_pref_list = []
            for j in range(nbr_pref_courses):
                random_course_index = random.randrange(len(self._course_list))
                random_course = self._course_list[random_course_index][0]
                if random_course not in ta_course_pref_list:
                    ta_course_pref_list.append(random_course)
            ta_list.append(("TA" + str(i), ta_course_pref_list))
        
        self._ta_list = ta_list

        for i in range(self._courses):
            nbr_ta_req = self._course_list[i][1]
            course_ta_pref_list = []
            for j in range(nbr_ta_req+ self._extra_ta_per_course):
                random_ta = "TA" + str(random.randrange(1, self._tas_requred_count))
                while random_ta in course_ta_pref_list:
                    random_ta = "TA" + str(random.randrange(1, self._tas_requred_count))
                course_ta_pref_list.append(random_ta)
            self._course_list[i] = (self._course_list[i][0], self._course_list[i][1], course_ta_pref_list)


    def _generate_course_instances(self):
        self._course_instance_list = []
        
        for i in range(self._courses):
            course = self._course_list[i][0]
            nbr_ta_req = self._course_list[i][1]
            course_ta_pref_list = self._course_list[i][2]
            for j in range(nbr_ta_req):
                course_instance = (course, j + 1, course_ta_pref_list)
                self._course_instance_list.append(course_instance)

    def get_test_data(self):
        self._generate_courses()
        self._generate_tas()
        self._generate_course_instances()
        return self._course_list, self._course_instance_list, self._ta_list

td = TestData(12, 4)
course_list, course_instances, ta_list = td.get_test_data()

print("---test course data---")
print (course_list)
print ("-----------------")
print("---test course instances---")
print (course_instances)
print ("-----------------")
print("---test ta data---")
print (ta_list)
print ("-----------------")