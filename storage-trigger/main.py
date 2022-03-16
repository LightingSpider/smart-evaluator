import os
from flask import Flask, request

import modules
import configuration

configuration.init()
app = Flask(__name__)

@app.route('/student', methods=['POST'])
def student():

    # Get the last added object in the Students Bucket
    blobs = [(blob, blob.updated) for blob in configuration.client.list_blobs(
        'pliroforiaka-2022-students'
    )]
    latest_blob = sorted(blobs, key=lambda tup: tup[1])[-1][0]

    # Get the class_id and student_id
    student_id, class_id = latest_blob.name[:-4].split('_')

    # Download the CSV file as bytes
    student_answer_bytes = latest_blob.download_as_bytes()
    print(student_answer_bytes)

    # Add the student's results to Big Query
    modules.students(student_answer_bytes, student_id, class_id)

    return {'msg': 'Results saved successfully'}

@app.route('/teacher', methods=['POST'])
def teacher():

    # Get the last added object in the Teachers Bucket
    blobs = [(blob, blob.updated) for blob in configuration.client.list_blobs(
        'pliroforiaka-2022-teachers'
    )]
    latest_blob = sorted(blobs, key=lambda tup: tup[1])[-1][0]

    # Get the class_id and teacher_id
    teacher_id, class_id = latest_blob.name[:-4].split('_')

    # Download the CSV file as bytes
    teacher_answer_bytes = latest_blob.download_as_bytes()
    print(teacher_answer_bytes)

    # Add the teacher's answers to Big Query
    df = modules.answers_df(teacher_answer_bytes)
    modules.add_answers(df, class_id)

    return {'msg': 'Answers saved successfully'}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
