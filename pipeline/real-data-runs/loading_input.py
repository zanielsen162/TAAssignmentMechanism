import numpy as np
import pandas as pd

def format_as_list(row):
    templist = row['desired_courses'].split(',')
    templist[:] = [item for item in templist if item != '']
    row['desired_courses'] = templist

    return row

def get_applicants_by_course(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    applicants_by_course = {}  

    df = df.apply(format_as_list, axis=1)
    for row in df.itertuples():
        for course in row.desired_courses:
            applicants_by_course.setdefault(course, []).append(int(row.id))
    
    app_by_course_df = pd.DataFrame.from_dict(applicants_by_course, orient='index').transpose()
    app_by_course_df.to_csv('applicants_by_course.csv', index=False)
    return app_by_course_df