import pandas as pd
from classes import *
from valid_matching import *
from ilptesting import format_dfs

def convert_to_course_requirements(courses_df):
    course_requirements = []
    for _, row in courses_df.iterrows():
        course_id = row['course']
        skills = row['skills'].split(',') if pd.notna(row['skills']) else []
        ta_req_nbr = row['TAs_req']
        course_requirements.append(CourseRequirement(course_id, skills, ta_req_nbr))
    return course_requirements

def convert_to_ta_list(applicants_df, rankings_df):
    ta_list = []
    for _, row in applicants_df.iterrows():
        ta_id = row['id']
        gpa = row['gpa']
        is_phd = row['class']  # True for PhD, False for Masters
        courses_taken = row['courses_taken'].split(',') if pd.notna(row['courses_taken']) else []
        skills = row['skills'].split(',') if pd.notna(row['skills']) else []
        prev_exp = row['prev_exp'].split(',') if pd.notna(row['prev_exp']) else []
        
        # Get course preferences from rankings
        pref_courses = rankings_df[rankings_df['ta'] == ta_id]['course'].tolist()
        
        ta = Applicant(ta_id, gpa, is_phd, courses_taken, skills, prev_exp, pref_courses)
        ta_list.append(ta)
    
    return ta_list

def check_matching_from_csv(courses_file, applicants_file, rankings_file):
    print(f"\nReading CSV files...")
    courses_df = pd.read_csv(courses_file)
    applicants_df = pd.read_csv(applicants_file)
    rankings_df = pd.read_csv(rankings_file)
    
    print("Converting data to required format...")
    course_requirements = convert_to_course_requirements(courses_df)
    ta_list = convert_to_ta_list(applicants_df, rankings_df)
    
    print("Attempting to find a matching...")
    course_list, edge_list, ta_list_incl_dummies = get_courses_and_edges(course_requirements, ta_list)
    graph = MatchingGraph(course_list, ta_list_incl_dummies, edge_list)
    matched_graph = complete_matching(ta_list, course_list, edge_list)

    print("\n--------------------final----------------------")
    if matched_graph and matched_graph.curr_match:
        print("A valid matching was found!")
        for course, ta in matched_graph.curr_match.items():
            if course and ta:
                print(f"{course.key_str()} is matched with {ta.key_str()}")
        
        # Print statistics
        print("\nMatching Statistics:")
        total_matches = sum(1 for course, ta in matched_graph.curr_match.items() if course and ta)
        print(f"Total matches made: {total_matches}")
        print(f"Total courses that needed TAs: {len(course_requirements)}")
        print(f"Total TAs available: {len(ta_list)}")
        
        # Check for unmatched PhDs
        unmatched_phds = [ta for ta in ta_list if ta.class_level and not any(t == ta for c, t in matched_graph.curr_match.items())]
        if unmatched_phds:
            print("\nWarning: Some PhD students were not matched:")
            for ta in unmatched_phds:
                print(f"  - {ta.key_str()}")
    else:
        print("No valid matching was found!")
        print("\nPossible reasons:")
        print("1. Not enough TAs for the required positions")
        print("2. TA preferences don't align with course needs")
        print("3. Constraints cannot be satisfied with current preferences")

if __name__ == "__main__":
    # You can change these file names to match your CSV files
    courses_file = "test3c.csv"
    applicants_file = "test3a.csv"
    rankings_file = "test3r.csv"
    
    check_matching_from_csv(courses_file, applicants_file, rankings_file) 