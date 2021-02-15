# Full Stack Trivia API Backend

## Introduction

This API bridges user interaction with the database, making the game possible. The requests are performed by the frontend, upon interaction by the user, and handled by this API to ensure correct behavior of the website, the game, and to ensure database validity.

## Getting Started

Base URL: http://localhost:5000/
API keys: currently this API does not require keys neither does it enforce authentication. It is currently restricted to local usage.

## Endpoints
### GET /categories
Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding type of the category
Request Arguments: None
Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
Test on the terminal:
curl http://127.0.0.1:5000/categories
### GET /questions
Fetches a list of all the questions in the database, paginated
Request Arguments: None
Returns: A dictionary containing a list of questions for the current page, the number of total_questions in the database, a dictionary of categories in the database, and the current_category. With the following structure:
{
    'categories': {
        '1': 'Science',
        '2': 'Art',
        ...
    },
    'current_category': null,
    'questions': [
        {
            'answer': 'Apollo 13',
            'category': 5,
            'difficulty': 4,
            'id': 2,
            'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?'
        },
        {
            ...
        },
        ...
    ],
    'total_questions': 19
}
Test on the terminal:
curl http://127.0.0.1:5000/questions

### DELETE /questions/int:question_id
Deletes a question from the database by its ID
Request Arguments: the to-be-deleted question's ID directly in the URI
Returns: A success message:
{
    'success': True
}
Test on the terminal:
curl -X DELETE http://127.0.0.1:5000/questions/2
### POST /questions
Adds a new question to the database. Will reject if the question already exists!
Request Arguments:
{
    'question': 'string: The question to be added',
    'answer': 'string: The answer to the question',
    'difficulty': int: How difficult is this question, from 1 to 5,
    'category': int: ID of the category of this question
}
Returns: A success message:
{
    'success': True
}
### Test on the terminal:
curl -X POST -H "Content-Type: application/json" \
    -d '{"question":"Who came up with the Theory of Relativity?","answer":"Albert Einstein", "difficulty": 2, "category": 1}' \
    http://127.0.0.1:5000/questions
POST /questions/search
Searches for questions that match the string provided, even partially
Request Arguments:
{
    'searchTerm': 'string: The term to match questions against'
}
Returns: Paginated questions matched, along with relevant info for the frontend:
{
    'success': True,
    'questions': [a list of the questions that matched the searchTerm],
    'total_questions': int: How many questions were matched, for pagination purposes,
    'current_category': None
}
Test on the terminal:
curl -X POST -H "Content-Type: application/json" \
    -d '{"searchTerm": "who"}' \
    http://127.0.0.1:5000/questions/search
GET /categories/int:category_id/questions
Fetches all questions in a category
Request Arguments: the desired category's ID to fetch questions from, in the request URI
Returns: Paginated questions of the requested category, along with relevant info for the frontend:
{
    'success': True,
    'questions': [a list of questions of the requested category],
    'total_questions': int: the number of questions in the requested category,
    'current_category': {category.id: category.type}
}
Test on the terminal:
curl http://127.0.0.1:5000/categories/1/questions
POST /quizzes
Fetches a new, random question of the specified category for the ongoing quiz
Request Arguments: Use id of 0 for ALL categories:
{
    'previous_questions': [a list of the previous questions played in the current quiz],
    'quiz_category': {'category.id': 'category.type'} --> ID and Type of the current quiz's category
}
Returns:
{
    'success': True,
    'question': {a random question}
}
Test on the terminal:
curl -X POST -H "Content-Type: application/json" \
    -d '{"previous_questions": [], "quiz_category": {"1": "Science"}}' \
    http://127.0.0.1:5000/quizzes

## Error Handling

The API works with regular HTTP errors. Additionally, it returns custom JSON responses for the following HTTP errors:

400 Bad Request
{
    'error': 400,
    'message: 'bad request'
}
404 Not Found
{
    'error': 404,
    'message': 'resource not found'
}
422 Unprocessable
{
    'error': 422,
    'message': 'unprocessable'
}
500 Internal Server Error
{
    'error': 500,
    'message': 'internal server error'
}

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

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

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


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```