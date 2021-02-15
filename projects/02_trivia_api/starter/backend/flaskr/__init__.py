import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

'''
@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs - COMPLETED
'''

'''
@TODO: Use the after_request decorator to set Access-Control-Allow - COMPLETED
'''
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # CORS(app, resources={r"*/api/*": {"origins": "*"}})
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  QUESTIONS_PER_PAGE = 10

  # Paginates the items recieved in the parameter items
  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE 
    question = formatted_questions = [question.format() for question in selection]
    current_question = question[start:end]
    return current_question

# -------------------------------------------------------------
# Categories
# -------------------------------------------------------------
  '''
  @TODO: COMPLETED
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    """GET all categories"""
    categories = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories}

    return jsonify({
      'success': True,
      'categories': formatted_categories
    })

# ------------------------------------------------------------
#  Questions 
# ------------------------------------------------------------
  '''
  @TODO: COMPLETED
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  # Retrievees list of paginated questions
  @app.route('/questions', methods=['GET'])
  def get_paginated_questions():
    questions = Question.query.all()
    current_questions = paginate_questions(request, questions)
    categories = {category.id: category.type for category in Category.query.all()}

    if len(current_questions) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': categories,
      'current_category': None
    })

  '''
  @TODO: COMPLETED
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  ''' 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    """DELETE a question from the database"""
    question = Question.query.filter(Question.id == question_id).first_or_404()
    try:
      question.delete()
    except:
      abort(500)
    finally:
      return jsonify({
        'success': True
      })

  '''
  @TODO: COMPLETED
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  # POSTs a new question to the database
  @app.route('/questions', methods=['POST'])
  def add_question():
    request_data = request.get_json()
    question = request_data['question']
    answer = request_data['answer']
    difficulty = request_data['difficulty']
    category = request_data['category']

    repeated_question = Question.query.filter(Question.question == question).one_or_none()

    if repeated_question is None:
      try:
        new_question = Question(
          question=question,
          answer=answer,
          difficulty=difficulty,
          category=category
        )
        new_question.insert()
      except:
        abort(500)
      finally:
        return jsonify({
          'success': True
        })
    else:
      abort(422)
  
 
  
  
  return app
