from io import BytesIO
import pandas as pd
from google.cloud import bigquery
import math
import random

import configuration
configuration.init()

# --------------- Teachers ---------------

def answers_df(teacher_answer_bytes: bytes):

    teacherDf = pd.read_csv(BytesIO(teacher_answer_bytes))

    # read teacher.csv files to generate the answers
    answers = teacherDf
    courseID = answers.loc[0]['Course ID']
    courseName = answers.loc[2]['Professor']

    # drop first 3 rows and replace header with the 1st row (Question ID, Correct Answer, Question Weight)
    answers = answers.iloc[3:].reset_index().drop('index', axis=1)
    answers.columns = answers.iloc[0]
    answers = answers[1:]

    # add to df 2 columns course name and course id
    answers.insert(0, 'Course Name', courseName.split('\n') * 25)
    answers.insert(0, 'Course ID', courseID.split('\n') * 25)

    # answer df columns tolist()
    qId = answers['Question ID'].tolist()
    cAnswer = answers['Correct Answer'].tolist()
    qWeight = answers['Question Weight'].tolist()

    ans_df = pd.DataFrame({'Question ID': qId,
                           'Correct Answer': cAnswer,
                           'Question Weight': qWeight,
                           })
    # ans_csv.to_csv('./answers/{}_answers.csv'.format(courseName), index=False)
    return ans_df

def add_answers(ans_df, course_id):

    # Construct a BigQuery client object.
    table_id = 'pliroforiaka-systimata-2022.exams.teachers_answers'

    rows_to_insert = [
        {u'Course_ID': u'{}'.format(course_id),
         u'Q1': u'{}'.format(ans_df['Correct Answer'][0]),
         u'Q2': u'{}'.format(ans_df['Correct Answer'][1]),
         u'Q3': u'{}'.format(ans_df['Correct Answer'][2]),
         u'Q4': u'{}'.format(ans_df['Correct Answer'][3]),
         u'Q5': u'{}'.format(ans_df['Correct Answer'][4]),
         u'Q6': u'{}'.format(ans_df['Correct Answer'][5]),
         u'Q7': u'{}'.format(ans_df['Correct Answer'][6]),
         u'Q8': u'{}'.format(ans_df['Correct Answer'][7]),
         u'Q9': u'{}'.format(ans_df['Correct Answer'][8]),
         u'Q10': u'{}'.format(ans_df['Correct Answer'][9]),
         u'Q11': u'{}'.format(ans_df['Correct Answer'][10]),
         u'Q12': u'{}'.format(ans_df['Correct Answer'][11]),
         u'Q13': u'{}'.format(ans_df['Correct Answer'][12]),
         u'Q14': u'{}'.format(ans_df['Correct Answer'][13]),
         u'Q15': u'{}'.format(ans_df['Correct Answer'][14]),
         u'Q16': u'{}'.format(ans_df['Correct Answer'][15]),
         u'Q17': u'{}'.format(ans_df['Correct Answer'][16]),
         u'Q18': u'{}'.format(ans_df['Correct Answer'][17]),
         u'Q19': u'{}'.format(ans_df['Correct Answer'][18]),
         u'Q20': u'{}'.format(ans_df['Correct Answer'][19]),
         u'Q21': u'{}'.format(ans_df['Correct Answer'][20]),
         u'Q22': u'{}'.format(ans_df['Correct Answer'][21]),
         u'Q23': u'{}'.format(ans_df['Correct Answer'][22]),
         u'Q24': u'{}'.format(ans_df['Correct Answer'][23]),
         u'Q25': u'{}'.format(ans_df['Correct Answer'][24])}
    ]
    errors = configuration.big_query_client.insert_rows_json(
        table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert)
    )  # Make an API request.
    if not errors:
        print('New rows have been added.')
    else:
        print('Encountered errors while inserting rows: {}'.format(errors))

# --------------- Students ---------------

def get_correct_answers(class_id: str):

    query = """
        SELECT * 
        FROM `pliroforiaka-systimata-2022.exams.teachers_answers`
        WHERE Course_ID = @class_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("class_id", "STRING", class_id)
        ]
    )
    return configuration.big_query_client.query(query, job_config=job_config).to_dataframe()

def get_average_grade(Student_ID: str):

    query = """
        SELECT AVG(grade) as avg_grade
        FROM(
            SELECT Grade_Total as grade
            FROM `pliroforiaka-systimata-2022.exams.results` as b
            WHERE Student_ID = @Student_ID
        )
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("Student_ID", "STRING", Student_ID)
        ]
    )
    query_res = configuration.big_query_client.query(query, job_config=job_config)

    results = {}
    results["Student_ID"] = Student_ID
    print(type(query_res))
    print(query_res)
    for row in query_res:
        results["Average_Grade"] = row.avg_grade
    return results

def get_all_students_in_a_class(Course_ID: str):

    query = """
        SELECT COUNT(*) as count
        FROM `pliroforiaka-systimata-2022.exams.results` as b
        WHERE b.Course_ID = @Course_ID
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("Course_ID", "STRING", Course_ID)
        ]
    )
    query_res = configuration.big_query_client.query(query, job_config=job_config)
    results = {}
    results["Course_ID"] = Course_ID
    for row in query_res:
        results["Students_in_class"] = row.count
    return results

def get_students_in_all_classes():

    query = """
        SELECT Course_ID as course_id, COUNT(*) as count
        FROM `pliroforiaka-systimata-2022.exams.results` as b
        GROUP BY b.Course_ID
    """
    query_res = configuration.big_query_client.query(query)
    results = {}
    cnt = 0
    for row in query_res:
        cnt += 1
        tmp = {}
        tmp["Course_ID"] = row.course_id
        tmp["Students_in_class"] = row.count
        results["course"+str(cnt)] = tmp
    return results


def get_num_students_failed_a_class(Course_ID: str):

    query = """
        SELECT COUNT(*) as count
        FROM `pliroforiaka-systimata-2022.exams.results` as b
        WHERE b.Course_ID = @Course_ID
        AND b.Grade_Total < 5.0
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("Course_ID", "STRING", Course_ID)
        ]
    )
    query_res = configuration.big_query_client.query(query, job_config=job_config)
    results = {}
    results["Course_ID"] = Course_ID
    for row in query_res:
        results["Students_failed"] = row.count
    return results

def get_num_students_passed_a_class(Course_ID: str):

    query = """
        SELECT COUNT(*) as count
        FROM `pliroforiaka-systimata-2022.exams.results` as b
        WHERE b.Course_ID = @Course_ID
        AND b.Grade_Total >= 5.0
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("Course_ID", "STRING", Course_ID)
        ]
    )
    query_res = configuration.big_query_client.query(query, job_config=job_config)
    results = {}
    results["Course_ID"] = Course_ID
    for row in query_res:
        results["Students_passed"] = row.count
    return results

def get_num_students_passed_a_class_certain_year(Course_ID: str, Year: str):

    query = """
        SELECT COUNT(year) as count
        FROM(
            SELECT SUBSTRING(Student_ID, 4, 2) as year
            FROM `pliroforiaka-systimata-2022.exams.results` as b
            WHERE b.Course_ID = @Course_ID
            AND b.Grade_Total >= 5.0
        )
        WHERE year= @Year
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("Course_ID", "STRING", Course_ID),
            bigquery.ScalarQueryParameter("Year", "STRING", Year)
        ]
    )
    query_res = configuration.big_query_client.query(query, job_config=job_config)
    results = {}
    results["Course_ID"] = Course_ID
    results["Year"] = "20"+Year

    for row in query_res:
        results["Students_passed"] = row.count
    return results

def get_num_students_passed_without_bonus(Course_ID: str):

    query = """
        SELECT COUNT(*) as count
        FROM `pliroforiaka-systimata-2022.exams.results` as b
        WHERE b.Course_ID = @Course_ID
        AND b.Grade_Total - b.Grade_Bonus >= 5.0
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("Course_ID", "STRING", Course_ID)
        ]
    )
    query_res = configuration.big_query_client.query(query, job_config=job_config)
    results = {}
    results["Course_ID"] = Course_ID
    for row in query_res:
        results["Students_passed"] = row.count
    return results

def students(student_answer_bytes: bytes, student_id, course_id):

    submitted_ans_df = pd.read_csv(BytesIO(student_answer_bytes))

    res_df = get_correct_answers(course_id)

    print(res_df)

    grade_total = 0
    teachers_ans = []
    for i in range(1, 26, 1):
        teachers_ans.append(res_df['Q{}'.format(i)][0])
    index = 0
    for j in submitted_ans_df['Student Answer']:
        if j == teachers_ans[index]:
            grade_total += 0.4
        index += 1
    grade_bonus = math.ceil(random.uniform(1, 4))
    semester = 10

    # Construct a BigQuery client object.
    table_id = 'pliroforiaka-systimata-2022.exams.results'

    rows_to_insert = [
        {u'Student_ID': u'{}'.format(student_id),
         u'Course_ID': u'{}'.format(course_id),
         u'Semester': u'{}'.format(semester),
         u'Grade_Total': u'{}'.format(grade_total + grade_bonus),
         u'Grade_Bonus': u'{}'.format(grade_bonus)}
    ]
    errors = configuration.big_query_client.insert_rows_json(
        table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert)
    )  # Make an API request.
    if not errors:
        print('New rows have been added.')
    else:
        print('Encountered errors while inserting rows: {}'.format(errors))


#print(get_average_grade("03116749"))
#print(get_all_students_in_a_class("17122"))
#print(get_num_students_passed_a_class_certain_year("17122","17"))
print(get_num_students_passed_without_bonus("17122"))
