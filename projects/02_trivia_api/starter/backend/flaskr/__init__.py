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

  #  Retrieves all categories
  @app.route('/categories')
  def get_categories():
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
  # Endpoint to delete a question based on the provided question ID
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
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
  
 
  '''
  @TODO: COMPLETED
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # Endpoint ot Search question based on the search term provided through the POST method
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    search_term = request.get_json()['searchTerm']
    formatted_search_term = f'%{search_term}%'

    try:
      questions = Question.query.filter(Question.question.ilike(formatted_search_term)).all()
      formatted_questions = [question.format() for question in questions]

      total_questions = len(formatted_questions)
    except:
      abort(500)
    finally:
      return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': total_questions,
        'current_category': None
      })

  '''
  @TODO: COMPLETED
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  #  Endpoint that retrieves a question within a particular category
  @app.route('/categories/<int:category_id>/questions')
  def get_categorized_questions(category_id):
    category = Category.query.get(category_id)
    
    if category is None:
      abort(404)
    else:
      try:
        questions = Question.query.filter(Question.category == category.id)
        formatted_questions = [question.format() for question in questions]

        total_questions = len(formatted_questions)
      except:
        abort(500)
      finally:
        return jsonify({
          'success': True,
          'questions': formatted_questions,
          'total_questions': total_questions,
          'current_category': {category.id: category.type}
        })

  '''
  @TODO: COMPLETED
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  # Endpoint that retrieves random queze within a category
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():    
    previous_questions = request.get_json()['previous_questions']
    quiz_category = request.get_json()['quiz_category']

    try:

      if quiz_category['id'] != 0:
        new_questions = Question.query.filter(Question.category == quiz_category['id']).filter(~Question.id.in_(previous_questions))
      else:
        new_questions = Question.query.filter(~Question.id.in_(previous_questions))
      
      formatted_questions = [question.format() for question in new_questions]

      if (len(formatted_questions) > 0):
        random_question = random.choice(formatted_questions)
        return jsonify({
          'success': True,
          'question': random_question
        })
      else:
        return jsonify({
          'success': True
        })
    except:
      abort(500)


  '''
  @TODO: COMPLETED
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  # Bad request Error Handler
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'error': 400,
      'message': 'bad request'
    }), 400
  # Resource not found error handler
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'error': 404,
      'message': 'resource not found'
    }), 404
  
  # Unprocessable Entity response error handler
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'error': 422,
      'message': 'unprocessable'
    }), 422
  
  # Internal server error handler
  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
      'error': 500,
      'message': 'internal server error'
    }), 500
  
  return app
