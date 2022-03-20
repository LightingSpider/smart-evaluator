# Smart Evaluator

The purpose of this project is to create a ***smart evaluator*** for both students and teachers.
The flow is simple. Teacher uploads a .csv file which contains the correct answer for every question and the question weight. After that every student
who uploads his .csv he will be evaluated automatically. This process automates the evaluation process but also helps both students and teachers.

For now, the evaluation works only for multiple choice answers, but this code-base can be used in order to add also more complex evaluation systems.

This repository containts 2 containerized applications named **rest** and **storage-trigger**.
Both of them are deployed on ***Google Cloud Run*** and are using other GCP products like Cloud Storage, Big Query and Eventarc.

Especially, **rest** container hosts all the APIs of the application like UploadFile, GetAverageGrade etc.
And **storage-trigger** is triggered every time an object is uploaded on Storage Bucket, downloads locally the file and starts a lite data processing,
where the transformed data are stored and analyzed with Big Query. Also, storage-trigger works with Eventarc.

Every container has the same code-base. 
At configuration.py file we initialize all the connections with the necessary clients (Storage, BigQuery etc.)
At resources.py file are the endpoints.
At modules.py are all the functions for processing and evaluation.
At main.py we set-up the server.
