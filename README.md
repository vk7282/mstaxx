## Synopsis

A simple book API recipe for all CRUD(Create, Read, Update and Delete) operations and API for external book information.

## Pre-requisites

* Postgresql 
* Python 3 
* Port number 8080 should be open as the API runs on this port.

## How to Run (development)

#### Set up database
* Login to postgres database and don't use any credentials for the dbs.
* Create 2 databases named `book` for actual production and `test_book` for testing API.

**NOTE** - Make sure there is not credentials set for both the created databases.

#### Set up API project 
* Clone this git repository on your local machine by running the command
`git clone `

* cd to `mstaxx` dir and create a virtual environment by `python3 -m venv myenv`
* Activate the virtual environment by `source myenv/bin/activate`.
* Install the python dependencies from `requirements.txt` file by running the command `pip install -r requirements.txt`.
* Run the server by `python run.py`. 
* This will run the server locally on `http://localhost:8080` with API exposed for the testing.

## Unit Testing 

you can run the unit tests for the project by running the command `nose2 -v app.tests`.

## Coverage

you can enable the coverage and see it in the current directory after running the below command.

`nose2 -v --with-coverage --coverage-config .coveragerc --coverage-report html app.tests`

**NOTE** - You can always exclude the folder in the file `.coveragerc` for the coverage consideration.