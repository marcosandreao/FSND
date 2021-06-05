# Backend - Full Stack Trivia API 

## Development Setup

1. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

2. **Install the dependencies:**
```
pip install -r requirements.txt
```

3. **Envs:**
```
export FLASK_APP=flaskr
export FLASK_ENV=development # enables debug mode
```
4. **Setup database:**
```
psql trivia < trivia.psql
```
5. **RUN:**
```
bash
flask run --reload
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