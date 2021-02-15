import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

#  Trivial App test case class
class TriviaTestCase(unittest.TestCase):

    # Define test variables and initialize app.
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('user', 'password', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Who invented the telegraph?',
            'answer': 'Samuel Morse',
            'difficulty': 3,
            'category': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    '''
        GET /categories
    '''
    # Tests retrival of all categories from DB
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
    
    # Test the bad request error handling
    def test_404_get_categories(self):
        res = self.client().get('/category')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
    
    '''
        GET /questions
    '''
    #Tests correct retrieval of questions upon request
    def test_get_paginated_questions(self):        
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertIsNone(data['current_category'])
    
    # Tests route error handling
    def test_404_get_paginated_questions(self):
        res = self.client().get('/question')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    '''
        DELETE /questions/<question_id>
    '''
    # Test question deletion from DB
    def test_delete_question(self):
        question = Question.query.first()
        res = self.client().delete(f'/questions/{question.id}')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
    
    # Test non existing question deletion
    def test_404_delete_question(self):
        res = self.client().delete('/questions/200')
        self.assertEqual(res.status_code, 404)

    '''
        POST /questions
    '''
    # Tests new question post to DB
    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''
        Search questions
    '''
    # Test question search in DB
    def test_search_question(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'a'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertIsNone(data['current_category'])
    
    # Tests question search not in DB
    def test_search_question_none_found(self):
        res = self.client().post('/questions/search', json={'searchTerm': '$'})
        data = json.loads(res.data)
        
        self.assertEqual(data['total_questions'], 0)
    
    '''
        GET questions by category
    '''
    # Tests retrieving questions within a particular category
    def test_get_categorized_questions(self):
        category = Category.query.first()
        res = self.client().get(f'/categories/{category.id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], {f'{category.id}': category.type})
    
    # Test category not found 
    def test_404_category_not_found(self):
        res = self.client().get(f'/categories/10000/questions')
        self.assertEqual(res.status_code, 404)
    
    '''
        Retrieve new question for quiz
    '''
    #  Test random quize retrieval
    def test_get_quiz_question(self):
        request_data = {
            'previous_questions': [],
            'quiz_category': {'id': 0} # ALL categories
        }
        res = self.client().post('/quizzes', json=request_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()