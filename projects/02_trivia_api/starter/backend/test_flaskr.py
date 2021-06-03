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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
