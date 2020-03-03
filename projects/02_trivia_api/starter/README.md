<h3>YATA (Yet.Another.Trivia.App)</h3>

The Udacity Full Stack training course requires the student to assist in the completion
of a trivia website. This is where YATA comes in, this web service demos how one can 
create a rest API using Flask. How to set it up and begin developing on it.

<h3>Getting Started</h3>
This project is written in Python 3.7 but has been tested as far back as Python 3.6.
It is highly recommended you follow the PEP 8 style guide if you wish to submit to this project.
You need to have at least Postgres 12 installed along with the supporting command line tools. 

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

Setting up git ignore
```https://git-scm.com/docs/gitignore```

<h3>Getting Started - Setup database</h3>
Using psql connect to your database service and create two empty databases called trivia and trivia_test

```create database trivia;```

```create database trivia_test;```

Now import the live trivia database and the testing database at the command line.
The source sql file can be found in the backend directory.

```psql trivia < trivia_03_02_2020.sql```

```psql trivia_test < trivia_03_02_2020.sql```


<h3>Getting Started - Setup frontend env</h3>
Now install the needed NPM system so you can insall the needed java script libraries for the front end please visit 

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
```flask run```

<h3>Getting Started - Start the frontend</h3>
Go to the frontend directory where you run npm install and run the following
```npm start```

<h3>Getting Started - Access the site</h3>
Assuming you haven't encountered any errors you should be able
to access the trivia site at 
```http://localhost:3000/```

<h3>API Endpoints - GET</h3>
Categories 

The categories endpoint supports three GET requests, one to see all available
categories, a specific category, and all questions for a specific category.

All categories

Example call ```curl 127.0.0.1:5000/categories```

Example response
```javascript
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "categories_total": 6
}
```

Specific category

Example call ```curl 127.0.0.1:5000/categories/1```

Example response
```javascript
{
  "id": 1, 
  "type": "Science"
}

```

Questions linked to a category

Example call ```curl http://localhost:5000/categories/1/questions ```

Example response
```javascript
{
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Art2", 
      "category": 2, 
      "difficulty": 1, 
      "id": 71, 
      "question": "Art2"
    }
  ], 
  "success": true, 
  "total_questions": 6
}

```
Questions 

The questions endpoint supports one get request and one delete request.

Get all questions, response is automatically paginated to 10 per page

Example call ```curl http://localhost:5000/questions```

Example response
```javascript
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
{
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 36
}

```

Get all questions for a specific page

Example call ```curl http://localhost:5000/questions?page=2```

Example response
```javascript
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Sci Answer 1", 
      "category": 1, 
      "difficulty": 1, 
      "id": 59, 
      "question": "Sci Question 1"
    }
  ], 
  "success": true, 
  "total_questions": 36
}

<h3>API Endpoints - DELETE</h3>
```
Delete specific question

Example call
```curl -X DELETE http://localhost:5000/questions/14```

Example response
```javascript
{
  "deleted": 1, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 35
}

```

<h3>API Endpoints - POST</h3>

There are 3 endpoints, two for questions and one for randomly generated quizzes.

Create new question

Example call ```curl -X POST 127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "TEST_QUESTION", "answer": "This is a test answer", "category": "4","difficulty": 2}'```

Example response
```javascript
{
  "id": 76, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 36
}

```

Search allows you to search for one or more questions

Example call 
```curl -X POST 127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm": "Which"}'```

Example respone
```javascript
{
  "currentCategory": null, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "totalQuestions": 7
}

```
The quizzes endpoint when provided with a category will randomly respond with a question associated
with the provided category. If you are tracking which questions you have processed you can supply the
quizzes endpoint with the question ids of previous questions. With the question ids the endpoint will omit questions that
have already been presented. 

It is also possible to omit the category json to receive a random category and question.

Example call random question with specified category skip question 70```curl -X POST 127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [70], "quiz_category": {"type": "Science", "id": "0"}}'```

Example call random category and question skip question 70 ```curl -X POST 127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [70], "quiz_category": {"type": "click", "id": 0}}'```

Example response
```javascript
{
  "question": {
    "answer": "Blood", 
    "category": 1, 
    "difficulty": 4, 
    "id": 22, 
    "question": "Hematology is a branch of medicine involving the study of what?"
  }, 
  "question_count": 5, 
  "success": true
}

```
 <h3>HTTP Status codes</h3>
 The follow status codes are supported by the API
````
200 - Good response
400 - Bad request
404 - Page or question not found
422 - Bad request
405 - Http call type not supported by end point 
500 - Server side error
````

Example failure response
```javascript
{
  "error": 405, 
  "message": "The method is not allowed for the requested URL.", 
  "success": false
}

```
 
<h3>Api References</h3>
This api was developed using rest standards

Project initially was forked from 
```https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter```

<h3>Authors</h3>
Udacity
 
David Mauler

<h3>Acknowledgements</h3>
A special thanks you the Udacity folks that helped make this project possible.
