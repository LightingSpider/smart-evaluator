import os
import configuration
app = configuration.init()

from resources import TeacherUploadFile, StudentUploadFile, AverageGrade, AllStudents, AllStudentsInClass, FailedStudentsInClass, PassedStudentsInClass

configuration.api.add_resource(TeacherUploadFile, '/teachers/upload_file')
configuration.api.add_resource(StudentUploadFile, '/students/upload_file')

configuration.api.add_resource(AverageGrade, '/students/<student_id>/average')
configuration.api.add_resource(AllStudentsInClass, '/class/<course_id>/all_students')
configuration.api.add_resource(AllStudents, '/students/all')
configuration.api.add_resource(FailedStudentsInClass, '/class/<course_id>/failed_students')
configuration.api.add_resource(PassedStudentsInClass, '/class/<course_id>/passed_students')

if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT")), threaded=True)
    # app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
