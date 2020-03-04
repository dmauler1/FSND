import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        self.db = setup_db(self.app, self.database_path)

        # binds the app to the current context
        """with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()"""

    def tearDown(self):
        """Executed after reach test"""
        pass

    def create_test_question(self):
        sql = """INSERT INTO QUESTIONS
                 (id, question, answer, category, difficulty)
                 VALUES (1000, 'This is a test question',
                 'This is a test answer', '4', 2)"""

        self.db.session.execute(sql)
        self.db.session.commit()

    def delete_test_question(self):
        question = Question.query.filter(Question.id == 1000).one_or_none()

        if question is not None:
            question.delete()

    """ Unit tests for Trivia app """

    def test_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_paginate_questions_page1(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_paginate_questions_page2(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertEqual(False, data['success'])
        self.assertEqual('resource not found', data['message'])

    def test_delete_question(self):
        self.delete_test_question()
        self.create_test_question()
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1000)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

        deleted_question = Question.query.filter(
            Question.id == 1000).one_or_none()
        self.assertEqual(deleted_question, None)

        self.delete_test_question()

    def test_delete_question_does_not_exist(self):
        self.delete_test_question()
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertEqual(data['success'], False)
        self.assertEqual('resource not found', data['message'])

    def test_create_question(self):
        res = self.client().post('/questions',
                                 json={'question': 'TEST_QUESTION',
                                       'answer': 'This is a test answer',
                                       'category': '4',
                                       'difficulty': 2})
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

        question = Question.query.filter(
            Question.question == 'TEST_QUESTION').one_or_none()
        question.delete()

    def test_missing_question(self):
        res = self.client().post('/questions',
                                 json={'answer': 'This is a test answer',
                                       'category': '4',
                                       'difficulty': 2})

        data = json.loads(res.data)

        self.assertEqual(422, res.status_code)
        self.assertEqual(False, data['success'])
        self.assertEqual('Missing question property', data['message'])

    def test_missing_answer(self):
        res = self.client().post('/questions',
                                 json={'question': 'TEST_QUESTION',
                                       'category': '4',
                                       'difficulty': 2})

        data = json.loads(res.data)

        self.assertEqual(422, res.status_code)
        self.assertEqual(False, data['success'])
        self.assertEqual('Missing answer property', data['message'])

    def test_missing_category(self):
        res = self.client().post('/questions',
                                 json={'question': 'TEST_QUESTION',
                                       'answer': 'This is a test answer',
                                       'difficulty': 2})

        data = json.loads(res.data)

        self.assertEqual(422, res.status_code)
        self.assertEqual(False, data['success'])
        self.assertEqual('Missing category property', data['message'])

    def test_missing_difficulty(self):
        res = self.client().post('/questions',
                                 json={'question': 'TEST_QUESTION',
                                       'answer': 'This is a test answer',
                                       'category': '4'
                                       })

        data = json.loads(res.data)

        self.assertEqual(422, res.status_code)
        self.assertEqual(False, data['success'])
        self.assertEqual('Missing difficulty property', data['message'])

    def test_search_for_question(self):
        self.delete_test_question()
        self.create_test_question()

        res = self.client().post('/questions/search',
                                 json={
                                     'searchTerm': 'This is a test question'})
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(True, data['success'])
        self.assertTrue(data['questions'])
        self.assertEqual('This is a test question',
                         data['questions'][0]['question'])
        self.assertTrue(data['totalQuestions'])

        self.delete_test_question()

    def test_search_for_question_no_result(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'zzzz'})
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertEqual(False, data['success'])
        self.assertEqual(
            'Unable to locate any questions based on search term zzzz',
            data['message'])

    def test_get_questions_for_category(self):
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(True, data['success'])
        self.assertTrue(data['questions'])

    def test_get_questions_fail_missing_category(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertEqual(False, data['success'])
        self.assertRaises(KeyError, lambda: data['questions'])

    def test_get_quiz(self):
        res = self.client().post('/quizzes', json={"previous_questions": [30],
                                                   "quiz_category": {
                                                       "type": "Science",
                                                       "id": "0"}})
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(True, data['success'])
        self.assertTrue(data['question']['answer'])
        self.assertTrue(data['question']['category'])
        self.assertTrue(data['question']['difficulty'])
        self.assertTrue(data['question']['id'])
        self.assertTrue(data['question']['question'])
        self.assertTrue(data['question_count'])

    def test_get_quiz_no_category(self):
        res = self.client().post('/quizzes', json={"previous_questions": [30],
                                                   "quiz_category": {
                                                       "type": "BadScience",
                                                       "id": "1000"}})
        data = json.loads(res.data)
        self.assertEqual(404, res.status_code)
        self.assertEqual(False, data['success'])
        self.assertEqual(
            'Provided category id 1000 not found!', data['message'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
