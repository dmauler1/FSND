# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

DONE - 1. Use Flask-CORS to enable cross-domain requests and set response headers. 
DONE - 2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
DONE - 3. Create an endpoint to handle GET requests for all available categories. 
DONE - 4. Create an endpoint to DELETE question using a question ID. 
DONE - 5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
DONE - 6. Create a POST endpoint to get questions based on category. 
DONE - 7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
DONE - 8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
DONE - 9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


Setup db
Run plsql
Create database
    create database trivia;
Disconnect from database
Create database for website testing
     psql trivia < trivia_03_02_2020.sql 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


<h3>YATA (Yet.Another.Trivia.App)</h3>

The Udacity Full Stack training course requires the student to assist in the completion
of a trivia website. This is where YATA comes in, this web service demos how one can 
create a rest API using Flask. How to set it up and begin developing on it.

<h3>Getting Started</h3>
This project is written in Python 3.7 but has been tested as far back as Python 3.6.
It is highly recommended you follow the PEP 8 style guide if you wish to submit to this project.
You need to have at least PSQL 12 installed along with the supporting command line tools. 

<h3>Getting Started - Clone Project</h3>
The project can be found at ```https://github.com/dmauler1/FSND```. 
Then click "Clone or download" and copy the the ssh git clone string. 
Now clone the project in a directory that you want to use for the project.
Now drill down in the trivia code directory found under
```/the/directory/you/created/FSND/projects/02_trivia_api/```

<h3>Getting Started - Setup backend env</h3>
Once you have the code pulled down create virtual environment inside the project directory backend.
Be sure to add the virtual environment to your .gitignore file. 

Now you need to install the requisite python modules using the provided requirements.txt file. The 
requirement.txt file is found in the backend directory. If you are unsure on how to do this see the following links.

Virtual environments - See section Creating virtual environment and Activating a virtual environment 

```https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/```

Requirements.txt - See Requirements Files section
```https://pip.pypa.io/en/stable/user_guide/```

<h3>Getting Started - Setup database</h3>
Using psql connect to your database service and create two an empty databases called trivia and trivia_test

```create database trivia;```

```create database trivia_test;```

Now import the live trivia database and the testing database at the command line

```psql trivia < trivia_03_02_2020.sql```

```psql trivia_test < trivia_03_02_2020.sql```


<h3>Getting Started - Setup frontend env</h3>
The install the needed libraries for the front end please visit 

```https://nodejs.org/en/download/```

Once you have npm installed enter the frontend directory and run the following command

```npm install```

<h3>Getting Started - Start the backend</h3>
Go back to the backend directory and make sure to source(activate) your
python virtual environment.
 
Now set the needed Flask environment values.

```export FLASK_APP=flaskr```

```export FLASK_ENV=development```

Now start the backend
```flask start```

<h3>Getting Started - Start the frontend</h3>
Go to the frontend directory where you run npm install and run the following
```npm start```

<h3>Getting Started - Access the site</h3>
Assuming you haven't encountered any errors you should be able
to access the trivia site at 
```http://localhost:3000/```

<h3>Api References</h3>
This api was developed using rest standards

Project initially was forked from 
```https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter```

<h3>Authors</h3>
Udacity
 
David Mauler

<h3>Acknowledgements</h3>
A special thanks you the Udacity folks that helped make this project possible.
