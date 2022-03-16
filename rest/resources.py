from flask import request
from flask_restx import Resource, fields, abort
from werkzeug.utils import secure_filename
import os

import configuration

class TeacherUploadFile(Resource):

    def post(self):

        try:

            data = dict(request.form)
            class_id = data['class_id']
            teacher_id = data['teacher_id']

            # Save the given file
            uploaded_file = request.files['file']
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(configuration.app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

            # Upload the file to the bucket
            storage_path = f"{teacher_id}_{class_id}.csv"
            blob = configuration.bucket_teachers.blob(storage_path)
            blob.upload_from_filename(file_path)

            # Delete the file
            os.remove(file_path)

            return {
                "statusCode": 200,
                "file_path": file_path,
                "storage_path": storage_path
            }

        except FileNotFoundError as e:
            abort(500, f"Invalid file path. {str(e)}", statusCode=500)

class StudentUploadFile(Resource):

    def post(self):

        try:

            data = dict(request.form)
            class_id = data['class_id']
            student_id = data['student_id']

            # Save the given file
            uploaded_file = request.files['file']
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(configuration.app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

            # Upload the file to the bucket
            storage_path = f"{student_id}_{class_id}.csv"
            blob = configuration.bucket_students.blob(storage_path)
            blob.upload_from_filename(file_path)

            # Delete the file
            os.remove(file_path)

            return {
                "statusCode": 200,
                "file_path": file_path,
                "storage_path": storage_path
            }

        except FileNotFoundError as e:
            abort(500, f"Invalid file path. {str(e)}", statusCode=500)
