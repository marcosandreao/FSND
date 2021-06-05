# https://flask-restful.readthedocs.io/en/latest/
# https://flask.palletsprojects.com/en/2.0.x/
# https://flask-restful.readthedocs.io/en/latest/intermediate-usage.html#use-with-blueprintsl
# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
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


# API Documentation **Project Trivia API**

## API Reference

### Getting Started
- Base URL: `http://127.0.0.1:5000/api` 

### Error Handling
- Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - get a list of all categories objects
- Returns:
    - list of categories objects  
    - HTTP status code 200
- Sample: `curl http://127.0.0.1:5000/api/categories
```
{
   "data":[
      {
         "type":"Art",
         "id":2
      },
      {
         "type":"Entertainment",
         "id":5
      },
      {
         "type":"Geography",
         "id":3
      },
      {
         "type":"History",
         "id":4
      },
      {
         "type":"Science",
         "id":1
      },
      {
         "type":"Sports",
         "id":6
      }
   ],
   "total":6
}
```

#### GET /questions
- General:
    - Returns a list of questions objects, success value, and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Request query parameters
    - Optional: **page** *int* Number page, default value is 1
    - Optional: **search_term** *str* search for a specific question by search term 
- Returns:
    - List of questions object
    - HTTP status code 200
- Sample: `curl http://127.0.0.1:5000/api/questions`
``` {
   "page":1,
   "limit":10,
   "total_pages":3,
   "has_next":true,
   "has_prev":false,
   "total":21,
   "data":[
      {
         "id":27,
         "question":"ab",
         "difficulty":4,
         "answer":"ab",
         "category":"3"
      },
      {
         "id":28,
         "question":"abc",
         "difficulty":3,
         "answer":"abc",
         "category":"6"
      },
      {
         "id":26,
         "question":"asdf",
         "difficulty":2,
         "answer":"asdf",
         "category":"1"
      },
      {
         "id":18,
         "question":"How many paintings did Van Gogh sell in his lifetime?",
         "difficulty":4,
         "answer":"One",
         "category":"2"
      },
      {
         "id":14,
         "question":"In which royal palace would you find the Hall of Mirrors?",
         "difficulty":3,
         "answer":"The Palace of Versailles",
         "category":"3"
      },
      {
         "id":17,
         "question":"La Giaconda is better known as what?",
         "difficulty":3,
         "answer":"Mona Lisa",
         "category":"2"
      },
      {
         "id":25,
         "question":"teste",
         "difficulty":3,
         "answer":"ticulo",
         "category":"1"
      },
      {
         "id":15,
         "question":"The Taj Mahal is located in which Indian city?",
         "difficulty":2,
         "answer":"Agra",
         "category":"3"
      },
      {
         "id":24,
         "question":"vai",
         "difficulty":3,
         "answer":"la",
         "category":"4"
      },
      {
         "id":9,
         "question":"What boxer's original name is Cassius Clay?",
         "difficulty":1,
         "answer":"Muhammad Ali",
         "category":"4"
      }
   ]

```

#### POST /questions
- General:
    - add a new question.
- Request body:
    - Required: **question** *str* Question value
    - Required: **answer** *str* Answer value
    - Required: **difficulty** *int* Difficulty value between 1 and 5
    - Required: **category** *int* Category id _see categories endpoint_
- Returns: 
    - Object with new ID
    - HTTP status code 201
    
- Sample: `curl http://127.0.0.1:5000/api/questions -X POST -H "Content-Type: application/json" -d '{ 'question': 'Heres a new question string', 'answer': 'Heres a new answer string', 'difficulty': 1, 'category': 3, }'`
```
{
   "id":9
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes a specified question using the id of the question 
- Request path parameters
    - Required: **question_id** *int* Id of question
- Returns: 
  - empty body
  - HTTP status code 204
- Sample `curl -X DELETE http://127.0.0.1:5000/api/questions/16`

#### POST /quizzes
- General:
    - Sends a post request in order to get the next random question  
- Request body:
    - Required: **previous_questions** *array* an array of question id's such as [1, 4, 20, 15] or empty array like that []
    - Required: **quiz_category** *int* Category id _#see categories endpoint_ or 0 value to get from all categories
- Returns:
    - Question json object
    - HTTP status code 200. IF there is no more question return STATUS CODE 204
- Sample: `curl http://127.0.0.1:5000/api/quizzes -X POST -H "Content-Type: application/json" -d "{'previous_questions': [1, 4, 20, 15], 'quiz_category': 1 }"`
```
{
   "id":11,
   "question":"Which country won the first ever soccer World Cup in 1930?",
   "difficulty":4,
   "answer":"Uruguay",
   "category":"6"
}
```