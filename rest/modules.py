import configuration
from google.cloud import bigquery

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

    results = {"Student_ID": Student_ID}
    for row in query_res:
        results["Average_Grade"] = round(row.avg_grade, 3)
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
    results = {"Course_ID": Course_ID}
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
    results = {"Course_ID": Course_ID}
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

