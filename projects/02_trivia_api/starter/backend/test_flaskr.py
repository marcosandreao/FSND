import json
import unittest
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        config = {
            "SQLALCHEMY_DATABASE_URI":
                "postgres://{}/{}".format('caryn:caryn@localhost:5432', "trivia_test"),
            'SQLALCHEMY_TRACK_MODIFICATIONS': 'false'}

        """Define test variables and initialize app."""
        self.app = create_app(config)
        self.client = self.app.test_client
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total'] > 0)
        # check if total is equal len data list
        self.assertEqual(len(data['data']), data['total'])

    def test_get_paginated_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total'] > 0)
        self.assertTrue(len(data['data']))
        self.assertTrue(data['has_next'])
        self.assertFalse(data['has_prev'])
        self.assertEquals(2, data['total_pages'])
        self.assertEquals(1, data['page'])

    def test_get_paginated_questions_page_2(self):
        res = self.client().get('/api/questions?page=2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total'] > 0)
        self.assertTrue(len(data['data']))
        self.assertFalse(data['has_next'])
        self.assertTrue(data['has_prev'])
        self.assertEquals(2, data['total_pages'])
        self.assertEquals(2, data['page'])

    def test_get_paginated_questions_page_not_found(self):
        res = self.client().get('/api/questions?page=0')
        self.assertEqual(res.status_code, 404)

    def test_delete_question(self):
        res = self.client().delete('/api/questions/22')
        self.assertEqual(res.status_code, 204)

    def test_post_question(self):
        res = self.client().post('/api/questions', json={
            'question': 'Heres a new question string',
            'answer': 'Heres a new answer string',
            'difficulty': 1,
            'category': 3,
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(int(data['id']) > 0)

    def test_post_question_empty_data(self):
        res = self.client().post('/api/questions', json={
            'difficulty': 1,
            'category': 3,
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['message']['answer'])

    def test_get_questions_by_category(self):
        res = self.client().get('/api/categories/3/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total'])
        self.assertEqual(len(data['data']), data['total'])
        # check is all result is from category 3
        self.assertEqual(len(data['data']), len([d for d in data['data'] if d['category'] == '3']))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
