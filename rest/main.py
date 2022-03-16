import os
import configuration
app = configuration.init()

from resources import TeacherUploadFile, StudentUploadFile

configuration.api.add_resource(TeacherUploadFile, '/teachers/upload_file')
configuration.api.add_resource(StudentUploadFile, '/students/upload_file')

if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT")), threaded=True)
    # app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
