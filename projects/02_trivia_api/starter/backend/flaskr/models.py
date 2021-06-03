from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import Column, String, Integer

database_name = "trivia"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class CategoryQuery(BaseQuery):
    def ordered(self):
        return self.order_by(Category.type)


class QuestionQuery(BaseQuery):
    def by_category(self, cat_id):
        return self.filter(Question.category == cat_id).order_by(Question.question)

    def search(self, search_term):
        return self.filter((Question.question.ilike('%{0}%'.format(search_term)))).order_by(Question.question)


class Question(db.Model):
    """
    Question

    """
    __tablename__ = 'questions'
    query_class = QuestionQuery

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


class Category(db.Model):
    """
    Category

    """
    __tablename__ = 'categories'
    query_class = CategoryQuery

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
