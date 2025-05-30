import numpy as np
import pandas as pd
# from ..loading_data_ilp import *
from loading_input import get_applicants_by_course

def preference_by_variability(applicants, r_c, var_high=True):
    """
    generate a distribution of scores for the applicants that has stark high/low or consistent
    """
    number_of_applicants = len(applicants)
    scores = np.zeros(number_of_applicants)

    if var_high:
        scores = np.random.randint(1, r_c + 1, number_of_applicants)  # Ensure high is greater than low
    else:
        scoring_trend = np.random.choice(['high', 'low'])
        if scoring_trend == 'high':
            low = int(min(r_c - r_c/2, r_c - 1)) # ensure that low < high
            scores = np.random.randint(low, r_c + 1, number_of_applicants)  # Ensure high is greater than low
        else:
            high = int(max(r_c - r_c/2, 2)) # ensure that high > low, and is at least 2
            scores = np.random.randint(1, high, number_of_applicants)  # Ensure high is greater than low

    return scores

def select_from_applicants(applicants, course_applicants, r_c, random_amount_applied=False, random_amount_selected=False):
    """
    determine which applicants are rated for a course
    """
    amount_selected = r_c + 2
    selected_applicants = []

    if random_amount_selected:
        amount_selected = np.random.randint(r_c + 4, 2 * (r_c + 4))

    if random_amount_applied:
        # randomly select a number of applicants that did not apply for the course
        amount_not_applied = np.random.randint(0, amount_selected)
        amount_applied = amount_selected - amount_not_applied

        if amount_applied > len(course_applicants):
            amount_applied = len(course_applicants)
            amount_not_applied = amount_selected - amount_applied
        selected_applicants = np.random.choice(course_applicants, size=amount_applied, replace=False, )
        # Ensure selected_applicants is a list before extending
        selected_applicants = selected_applicants.tolist() if isinstance(selected_applicants, np.ndarray) else selected_applicants
        
        # Extend selected_applicants with applicants who did not apply
        non_applicants = np.random.choice(applicants, size=amount_not_applied, replace=False)
        selected_applicants.extend(non_applicants)
    else:
        if len(course_applicants) < amount_selected:
            selected_applicants = course_applicants
            # Supplement with applicants who did not apply
            remaining_needed = amount_selected - len(course_applicants)
            non_applicants = np.random.choice(applicants, size=remaining_needed, replace=False)
            selected_applicants.extend(non_applicants)
        else:
            selected_applicants = np.random.choice(course_applicants, size=amount_selected, replace=False)

    return selected_applicants

def generate_prof_preferences(num_ta_required_df, applicants_df, all_applicants_df):
    """
    generate some data for how professors would rank their TAs
    num_ta_required_df: DataFrame with the number of TAs required for each course where columns are 'course', 'space'
    applicants_df: DataFrame where columns are the courses and filled with ids of applicants for that course
    """

    # Filter all_applicants_df to only include PhD students
    phd_applicants_df = all_applicants_df[all_applicants_df['class_level'] == 'PHD']
    phd_applicants = phd_applicants_df['id'].tolist()

    prof_preferences = {}
    for course in num_ta_required_df['course']:
        # get the number of TAs required for the course
        r_c = int(np.ceil(num_ta_required_df.loc[num_ta_required_df['course'] == course, 'space'].values[0] / 35))
        # get the applicants for the course
        course_applicants = applicants_df[course].dropna().astype(int).tolist()

        # Filter course_applicants to only include PhD students
        course_applicants = [applicant for applicant in course_applicants if applicant in phd_applicants]

        random_amount_applied = False # np.random.choice([True, False])
        random_amount_selected = np.random.choice([True, False])
        random_variability = np.random.choice([True, False])

        # generate a distribution of scores for the applicants
        selected_applicants = select_from_applicants(phd_applicants, course_applicants, r_c, random_amount_applied=random_amount_applied, random_amount_selected=random_amount_selected)
        
        # Convert applicants to integers
        selected_applicants = [int(applicant) for applicant in selected_applicants]
        
        scores = preference_by_variability(selected_applicants, r_c, var_high=random_variability)

        prof_preferences[course] = {
            'course': course,
            'num_tas_required': r_c,
            'applicants': selected_applicants,
            'scores': scores
        }
    
    prof_preferences_df = pd.DataFrame.from_dict(prof_preferences, orient='index')
    prof_preferences_df.to_csv('prof_preferences.csv', index=False)

    with open('test-sets/prof_preferences_rankings.csv', 'w') as f:
        f.write(f"course,ta,ranking\n")
        for course in prof_preferences.keys():
            for applicant, score in zip(prof_preferences[course]['applicants'], prof_preferences[course]['scores']):
                f.write(f"{course},{applicant},{score}\n")

num_ta_required_df = pd.read_csv('test-sets/course_enrollment.csv')
applicants_df = pd.read_csv('applicants_by_course.csv')
all_applicants_df = pd.read_csv('test-sets/cleaned-ta-app-data.csv')

if __name__ == "__main__":
    generate_prof_preferences(num_ta_required_df, applicants_df, all_applicants_df)