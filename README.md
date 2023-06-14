# KIMO.AI Assignment

This is a solution for KIMO.AI SW assignment. 

## Requirements:
This application has been developed using python 3.8.16, other requirements are listed under requirements.txt

## Contents:

* application - folder containing all the files related to the application
* dataloader - folder containing te initial courses data and script to bulk update the mongo db with it
* test - folder containing unit tests for the endpoints
* Dockerfile - Docker image build file
* docker-compose.yml - Docker Compose configuration file
* requirements.txt - requirements file for python packages

## Dataloading
In *data_loader* folder run the dbload.py using the below command, this will load the data from __courses.json__ to mongodb and would create the required collections on the fly:

```
python dbload.py
```

> **ASSUMPTIONS**: Two collections were created courses and chapters in mongodb and rest of the operations is carried out by the API endpoints


## API endpoints
In application folder, **main.py** is the entrypoint of the application. This includes all the endpoints to interact with the database and retrieve information.

## Unit Tests
In the test folder endpoints_test.py includes all the endpoints unit test cases.


