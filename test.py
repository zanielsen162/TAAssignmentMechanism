from classes import *
from valid_matching import *
from ilptesting import *


#example classes and number of required TAs
course_requirements = [
    CourseRequirement("CMPSC 16", ["Problem Solving", "Algorithms"], 2),
    CourseRequirement("CMPSC 24", ["Algorithms", "Data Structures"], 1),
    CourseRequirement("CMPSC 32", ["Object-Oriented Design", "C++"], 1),
    CourseRequirement("CMPSC 40", ["Compilers", "Computer Organization"], 3),
    CourseRequirement("CMPSC 64", ["Computer Organization", "Assembly"], 2),
    CourseRequirement("CMPSC 111", ["Computational Science", "Numerical Methods"], 1),
    CourseRequirement("CMPSC 130A", ["Data Structures", "Algorithms"], 3),
    CourseRequirement("CMPSC 130B", ["Advanced Algorithms", "Data Structures"], 2),
    CourseRequirement("CMPSC 134", ["Randomized Algorithms"], 1)
] #16 TAs needed total

#all phds are matched and some of the masters are matched, leaving some masters unmatched
def phds_matched_some_masters_graph():
    # Defining TA applicants
    ta_1 = Applicant("1", 3.9, True, ["Algorithms", "Problem Solving"], ["C++", "Java"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 32", "CMPSC 40"])
    ta_2 = Applicant("2", 4.0, True, ["Algorithms", "Data Structures"], ["Python", "Java"], ["Research Assistant"], ["CMPSC 16", "CMPSC 32", "CMPSC 40", "CMPSC 130A"])
    ta_3 = Applicant("3", 3.7, True, ["Object-Oriented Design", "C++"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 40", "CMPSC 64", "CMPSC 130B"])
    ta_4 = Applicant("4", 3.8, True, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 40", "CMPSC 64", "CMPSC 130B", "CMPSC 130A"])
    ta_5 = Applicant("5", 3.6, True, ["Data Structures", "Algorithms"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 16", "CMPSC 24"])
    ta_6 = Applicant("6", 3.7, True, ["Advanced Algorithms", "Data Structures"], ["C++", "Python"], ["Research Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 40", "CMPSC 111"])
    ta_7 = Applicant("7", 3.8, True, ["Randomized Algorithms", "Data Structures"], ["Python", "C"], ["Teaching Assistant"], ["CMPSC 134", "CMPSC 111", "CMPSC 40", "CMPSC 16"])
    ta_8 = Applicant("8", 3.6, True, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 134", "CMPSC 40", "CMPSC 130A"])
    ta_9 = Applicant("9", 3.5, True, ["Problem Solving", "Algorithms"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 130A", "CMPSC 130B"])
    ta_10 = Applicant("10", 3.6, True, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 134", "CMPSC 130B", "CMPSC 130A"])
    ta_11 = Applicant("11", 3.5, True, ["Problem Solving", "Algorithms"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 130B", "CMPSC 130A"])

    # Additional Master's applicants
    ta_12 = Applicant("12", 3.9, False, ["Data Structures", "Algorithms"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 16", "CMPSC 24"])
    ta_13 = Applicant("13", 3.7, False, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 40", "CMPSC 64", "CMPSC 130B", "CMPSC 130A"])
    ta_14 = Applicant("14", 3.8, False, ["Algorithms", "Randomized Algorithms"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 134", "CMPSC 40", "CMPSC 16", "CMPSC 130B"])
    ta_15 = Applicant("15", 3.6, False, ["Object-Oriented Design", "C++"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 40", "CMPSC 130B", "CMPSC 130A"])
    ta_16 = Applicant("16", 3.7, False, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 130B", "CMPSC 130A", "CMPSC 134"])
    ta_17 = Applicant("17", 3.6, False, ["Object-Oriented Design", "C++"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 64", "CMPSC 16", "CMPSC 130A"])
    ta_18 = Applicant("18", 3.7, False, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 24", "CMPSC 130B", "CMPSC 134"])

    # Add all TAs to the list
    ta_list = [ta_1, ta_2, ta_3, ta_4, ta_5, ta_6, ta_7, ta_8, ta_9, ta_10, ta_11, ta_12, ta_13, ta_14, ta_15, ta_16, ta_17, ta_18]
    course_list, edge_list, ta_list_incl_dummies = get_courses_and_edges(course_requirements, ta_list)
    
    graph = MatchingGraph(course_list, ta_list_incl_dummies, edge_list)
    matching(graph)
    graph.print_matches()
    print('---')
    final_graph = complete_matching(ta_list_incl_dummies, course_list, edge_list)
    print(final_graph)

print("all phds some masters")
phds_matched_some_masters_graph()

#exact amount of TAs as number of required TAs and each is matched to a course
def every_filled():
    # Defining TA applicants
    ta_1 = Applicant("1", 3.9, True, ["Algorithms", "Problem Solving"], ["C++", "Java"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 32", "CMPSC 40"])
    ta_2 = Applicant("2", 4.0, True, ["Algorithms", "Data Structures"], ["Python", "Java"], ["Research Assistant"], ["CMPSC 16", "CMPSC 32", "CMPSC 40", "CMPSC 130A"])
    ta_3 = Applicant("3", 3.7, True, ["Object-Oriented Design", "C++"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 40", "CMPSC 64", "CMPSC 130B"])
    ta_4 = Applicant("4", 3.8, True, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 40", "CMPSC 64", "CMPSC 130B", "CMPSC 130A"])
    ta_5 = Applicant("5", 3.6, True, ["Data Structures", "Algorithms"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 16", "CMPSC 24"])
    ta_6 = Applicant("6", 3.7, True, ["Advanced Algorithms", "Data Structures"], ["C++", "Python"], ["Research Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 40", "CMPSC 111"])
    ta_7 = Applicant("7", 3.8, True, ["Randomized Algorithms", "Data Structures"], ["Python", "C"], ["Teaching Assistant"], ["CMPSC 134", "CMPSC 111", "CMPSC 40", "CMPSC 16"])
    ta_8 = Applicant("8", 3.6, True, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 134", "CMPSC 40", "CMPSC 130A"])
    ta_9 = Applicant("9", 3.5, True, ["Problem Solving", "Algorithms"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 130A", "CMPSC 130B"])
    ta_10 = Applicant("10", 3.6, True, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 134", "CMPSC 130B", "CMPSC 130A"])
    ta_11 = Applicant("11", 3.5, True, ["Problem Solving", "Algorithms"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 130B", "CMPSC 130A"])

    # Additional Master's applicants
    ta_12 = Applicant("12", 3.9, False, ["Data Structures", "Algorithms"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 16", "CMPSC 24"])
    ta_13 = Applicant("13", 3.7, False, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 40", "CMPSC 64", "CMPSC 130B", "CMPSC 130A"])
    ta_14 = Applicant("14", 3.8, False, ["Algorithms", "Randomized Algorithms"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 134", "CMPSC 40", "CMPSC 16", "CMPSC 130B"])
    ta_15 = Applicant("15", 3.6, False, ["Object-Oriented Design", "C++"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 40", "CMPSC 130B", "CMPSC 130A"])
    ta_16 = Applicant("16", 3.7, False, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 130B", "CMPSC 130A", "CMPSC 134"])
    
    # Add all TAs to the list
    ta_list = [ta_1, ta_2, ta_3, ta_4, ta_5, ta_6, ta_7, ta_8, ta_9, ta_10, ta_11, ta_12, ta_13, ta_14, ta_15, ta_16]
    course_list, edge_list, ta_list_incl_dummies = get_courses_and_edges(course_requirements, ta_list)
    
    graph = MatchingGraph(course_list, ta_list_incl_dummies, edge_list)
    matching(graph)
    graph.print_matches()
    print('---')
    final_graph = complete_matching(ta_list_incl_dummies, course_list, edge_list)

    try:
        final_graph.print_matches()
    except:
        print(final_graph)

print("every applicant matched, every course filled")
every_filled()

#little phds and some masters, will have courses unmatched
def little_phds_some_masters():
    # Defining TA applicants
    ta_1 = Applicant("1", 3.9, True, ["Algorithms", "Problem Solving"], ["C++", "Java"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 32", "CMPSC 40"])
    ta_2 = Applicant("2", 4.0, True, ["Algorithms", "Data Structures"], ["Python", "Java"], ["Research Assistant"], ["CMPSC 16", "CMPSC 32", "CMPSC 40", "CMPSC 130A"])
    ta_3 = Applicant("3", 3.7, True, ["Object-Oriented Design", "C++"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 40", "CMPSC 64", "CMPSC 130B"])
    ta_4 = Applicant("4", 3.8, True, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 40", "CMPSC 64", "CMPSC 130B", "CMPSC 130A"])
    
    # Additional Master's applicants
    ta_12 = Applicant("12", 3.9, False, ["Data Structures", "Algorithms"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 16", "CMPSC 24"])
    ta_13 = Applicant("13", 3.7, False, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 40", "CMPSC 64", "CMPSC 130B", "CMPSC 130A"])
    ta_14 = Applicant("14", 3.8, False, ["Algorithms", "Randomized Algorithms"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 134", "CMPSC 40", "CMPSC 16", "CMPSC 130B"])
    ta_15 = Applicant("15", 3.6, False, ["Object-Oriented Design", "C++"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 40", "CMPSC 130B", "CMPSC 130A"])
    ta_16 = Applicant("16", 3.7, False, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 130B", "CMPSC 130A", "CMPSC 134"])
    ta_17 = Applicant("17", 3.6, False, ["Object-Oriented Design", "C++"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 64", "CMPSC 16", "CMPSC 130A"])
    ta_18 = Applicant("18", 3.7, False, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 24", "CMPSC 130B", "CMPSC 134"])

    # Add all TAs to the list
    ta_list = [ta_1, ta_2, ta_3, ta_4,ta_12, ta_13, ta_14, ta_15, ta_16, ta_17, ta_18]
    course_list, edge_list, ta_list_incl_dummies = get_courses_and_edges(course_requirements, ta_list)
    
    graph = MatchingGraph(course_list, ta_list_incl_dummies, edge_list)
    matching(graph)
    graph.print_matches()
    print('---')
    final_graph = complete_matching(ta_list_incl_dummies, course_list, edge_list)

    try:
        final_graph.print_matches()
    except:
        print(final_graph)

print("little phds and some masters")
little_phds_some_masters()

#no phds some masters
def no_phds():
    # Defining TA applicants
    ta_9 = Applicant("9", 3.5, False, ["Problem Solving", "Algorithms"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 130A", "CMPSC 130B"])
    ta_10 = Applicant("10", 3.6, False, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 134", "CMPSC 130B", "CMPSC 130A"])
    ta_11 = Applicant("11", 3.5, False, ["Problem Solving", "Algorithms"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 130B", "CMPSC 130A"])
    ta_12 = Applicant("12", 3.9, False, ["Data Structures", "Algorithms"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 16", "CMPSC 24"])
    ta_13 = Applicant("13", 3.7, False, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 40", "CMPSC 64", "CMPSC 130B", "CMPSC 130A"])
    ta_14 = Applicant("14", 3.8, False, ["Algorithms", "Randomized Algorithms"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 134", "CMPSC 40", "CMPSC 16", "CMPSC 130B"])
    ta_15 = Applicant("15", 3.6, False, ["Object-Oriented Design", "C++"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 40", "CMPSC 130B", "CMPSC 130A"])
    ta_16 = Applicant("16", 3.7, False, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 130B", "CMPSC 130A", "CMPSC 134"])
    ta_17 = Applicant("17", 3.6, False, ["Object-Oriented Design", "C++"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 64", "CMPSC 16", "CMPSC 130A"])
    ta_18 = Applicant("18", 3.7, False, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 24", "CMPSC 130B", "CMPSC 134"])

    # Add all TAs to the list
    ta_list = [ta_9, ta_10, ta_11, ta_12, ta_13, ta_14, ta_15, ta_16, ta_17, ta_18]
    course_list, edge_list, ta_list_incl_dummies = get_courses_and_edges(course_requirements, ta_list)
    
    graph = MatchingGraph(course_list, ta_list_incl_dummies, edge_list)
    matching(graph)
    graph.print_matches()
    print('---')
    final_graph = complete_matching(ta_list_incl_dummies, course_list, edge_list)

    try:
        final_graph.print_matches()
    except:
        print(final_graph)

print("no phds")
no_phds()

#some phds not matched, only put down one preference for some phds so harder to match them
def some_phds_not_matched():
    # Defining TA applicants
    ta_1 = Applicant("1", 3.9, True, ["Algorithms", "Problem Solving"], ["C++", "Java"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 32", "CMPSC 40"])
    ta_2 = Applicant("2", 4.0, True, ["Algorithms", "Data Structures"], ["Python", "Java"], ["Research Assistant"], ["CMPSC 16", "CMPSC 32", "CMPSC 40", "CMPSC 130A"])
    ta_3 = Applicant("3", 3.7, True, ["Object-Oriented Design", "C++"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 40", "CMPSC 64", "CMPSC 130B"])
    ta_4 = Applicant("4", 3.8, True, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 40", "CMPSC 64", "CMPSC 130B", "CMPSC 130A"])
    ta_5 = Applicant("5", 3.6, True, ["Data Structures", "Algorithms"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 16", "CMPSC 24"])
    ta_6 = Applicant("6", 3.7, True, ["Advanced Algorithms", "Data Structures"], ["C++", "Python"], ["Research Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 40", "CMPSC 111"])
    ta_7 = Applicant("7", 3.8, True, ["Randomized Algorithms", "Data Structures"], ["Python", "C"], ["Teaching Assistant"], ["CMPSC 134", "CMPSC 111", "CMPSC 40", "CMPSC 16"])
    ta_8 = Applicant("8", 3.6, True, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111"])
    ta_9 = Applicant("9", 3.5, True, ["Problem Solving", "Algorithms"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 16"])
    ta_10 = Applicant("10", 3.6, True, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111"])
    ta_11 = Applicant("11", 3.5, True, ["Problem Solving", "Algorithms"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 16"])

    # Additional Master's applicants
    ta_12 = Applicant("12", 3.9, False, ["Data Structures", "Algorithms"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 16", "CMPSC 24"])
    ta_13 = Applicant("13", 3.7, False, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 40", "CMPSC 64", "CMPSC 130B", "CMPSC 130A"])
    ta_14 = Applicant("14", 3.8, False, ["Algorithms", "Randomized Algorithms"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 134", "CMPSC 40", "CMPSC 16", "CMPSC 130B"])
    ta_15 = Applicant("15", 3.6, False, ["Object-Oriented Design", "C++"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 40", "CMPSC 130B", "CMPSC 130A"])
    ta_16 = Applicant("16", 3.7, False, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 130B", "CMPSC 130A", "CMPSC 134"])
    ta_17 = Applicant("17", 3.6, False, ["Object-Oriented Design", "C++"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 64", "CMPSC 16", "CMPSC 130A"])
    ta_18 = Applicant("18", 3.7, False, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 24", "CMPSC 130B", "CMPSC 134"])

    # Add all TAs to the list
    ta_list = [ta_1, ta_2, ta_3, ta_4, ta_5, ta_6, ta_7, ta_8, ta_9, ta_10, ta_11, ta_12, ta_13, ta_14, ta_15, ta_16, ta_17, ta_18]
    course_list, edge_list, ta_list_incl_dummies = get_courses_and_edges(course_requirements, ta_list)
    
    graph = MatchingGraph(course_list, ta_list_incl_dummies, edge_list)
    matching(graph)
    graph.print_matches()
    print('---')
    final_graph = complete_matching(ta_list_incl_dummies, course_list, edge_list)
    print(final_graph)

print("some phds cant be matched")
some_phds_not_matched()

#all the phds are matched, each course gets phds, no masters are matched
def phds_no_masters_matched():
    # Defining TA applicants
    ta_1 = Applicant("1", 3.9, True, ["Algorithms", "Problem Solving"], ["C++", "Java"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 32", "CMPSC 40"])
    ta_2 = Applicant("2", 4.0, True, ["Algorithms", "Data Structures"], ["Python", "Java"], ["Research Assistant"], ["CMPSC 16", "CMPSC 32", "CMPSC 40", "CMPSC 130A"])
    ta_3 = Applicant("3", 3.7, True, ["Object-Oriented Design", "C++"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 32", "CMPSC 40", "CMPSC 64", "CMPSC 130B"])
    ta_4 = Applicant("4", 3.8, True, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 40", "CMPSC 64", "CMPSC 130B", "CMPSC 130A"])
    ta_5 = Applicant("5", 3.6, True, ["Data Structures", "Algorithms"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 16", "CMPSC 24"])
    ta_6 = Applicant("6", 3.7, True, ["Advanced Algorithms", "Data Structures"], ["C++", "Python"], ["Research Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 40", "CMPSC 111"])
    ta_7 = Applicant("7", 3.8, True, ["Randomized Algorithms", "Data Structures"], ["Python", "C"], ["Teaching Assistant"], ["CMPSC 134", "CMPSC 111", "CMPSC 40", "CMPSC 16"])
    ta_8 = Applicant("8", 3.6, True, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 134", "CMPSC 40", "CMPSC 130A"])
    ta_9 = Applicant("9", 3.5, True, ["Problem Solving", "Algorithms"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 16", "CMPSC 24", "CMPSC 130A", "CMPSC 130B"])
    ta_10 = Applicant("10", 3.6, True, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 16"])
    ta_11 = Applicant("11", 3.5, True, ["Problem Solving", "Algorithms"], ["Java", "C++"], ["Teaching Assistant"], ["CMPSC 32"])
    ta_12 = Applicant("12", 3.8, True, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 40", "CMPSC 64", "CMPSC 130B", "CMPSC 130A"])
    ta_13 = Applicant("13", 3.6, True, ["Data Structures", "Algorithms"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 16", "CMPSC 24"])
    ta_14 = Applicant("14", 3.7, True, ["Advanced Algorithms", "Data Structures"], ["C++", "Python"], ["Research Assistant"], ["CMPSC 130A", "CMPSC 130B", "CMPSC 40", "CMPSC 111"])
    ta_15 = Applicant("15", 3.8, True, ["Randomized Algorithms", "Data Structures"], ["Python", "C"], ["Teaching Assistant"], ["CMPSC 134", "CMPSC 111", "CMPSC 40", "CMPSC 16"])
    ta_16 = Applicant("16", 3.6, True, ["Computational Science", "Numerical Methods"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 111", "CMPSC 134", "CMPSC 40", "CMPSC 130A"])
   
    # Additional Master's applicants
    ta_17 = Applicant("17", 3.9, False, ["Data Structures", "Algorithms"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 32"])
    ta_18 = Applicant("18", 3.7, False, ["Compilers", "Computer Organization"], ["Assembly", "C"], ["Teaching Assistant"], ["CMPSC 32"])
    ta_19 = Applicant("19", 3.8, False, ["Algorithms", "Randomized Algorithms"], ["Python", "Java"], ["Teaching Assistant"], ["CMPSC 32"])
    ta_20 = Applicant("20", 3.6, False, ["Object-Oriented Design", "C++"], ["C++", "Python"], ["Teaching Assistant"], ["CMPSC 32"])
    
    # Add all TAs to the list
    ta_list = [ta_1, ta_2, ta_3, ta_4, ta_5, ta_6, ta_7, ta_8, ta_9, ta_10, ta_11, ta_12, ta_13, ta_14, ta_15, ta_16, ta_17, ta_18, ta_19, ta_20]
    course_list, edge_list, ta_list_incl_dummies = get_courses_and_edges(course_requirements, ta_list)
    
    graph = MatchingGraph(course_list, ta_list_incl_dummies, edge_list)
    matching(graph)
    graph.print_matches()
    print('---')
    final_graph = complete_matching(ta_list_incl_dummies, course_list, edge_list)
    print(final_graph)

print("phds matched no masters matched")
phds_no_masters_matched()


#no valid matching is always appearing 
#if all phds are matched and the masters can now get matched...still provides 'no valid matching'
#if every course is filled with phds we dont get the 'no valid matching'

print("teststastuduyasdgua")

courses_df = pd.read_csv('test2c.csv')
applicants_df = pd.read_csv('test2a.csv')
rankings_df = pd.read_csv('test2r.csv')
courses, tas, rankings, edges = format_dfs(courses_df, applicants_df, rankings_df)



course_list, edge_list, ta_list_incl_dummies = get_courses_and_edges (courses, tas)
#course_list, edge_list = get_courses_edges ([course_1, course_2], [edge_1, edge_2, edge_3, edge_4, edge_5, edge_6])
#print ('course list', [x for x in course_list])
#print ('edge list', edge_list)
graph = MatchingGraph(course_list, ta_list_incl_dummies, edge_list)
matching(graph)
graph.print_matches()
print('---')
final_graph = complete_matching(ta_list_incl_dummies, course_list, edge_list)
