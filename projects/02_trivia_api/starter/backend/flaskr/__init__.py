import os
from flask import Flask, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
KNOWN_JSON_PROPERTIES = ['question', 'answer', 'category', 'difficulty', ]


"""def validate_json_props(request):
    match_found = False
    match_count = 0

    body = request.get_json()

    if body:
        for property in body:
            for good_json_props in KNOWN_JSON_PROPERTIES:
                if property == good_json_props:
                    print(f"{property} {good_json_props}")
                    match_count = 1 + match_count
                    break
    else:
        match_found = True

    if match_count == len(KNOWN_JSON_PROPERTIES):
        match_found = True

    return match_found"""


def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    some_models = [some_model.format() for some_model in selection]

    return some_models[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Response Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs - DONE
  '''

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow - DONE
  '''

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    @app.route('/categories', methods=['GET'])
    def categories():
        selection = Category.query.order_by(Category.id).all()

        categories = [category.format() for category in selection]

        category_names = []
        for category in categories:
            category_names.append(category['type'])

        return jsonify({'categories': category_names,
                        'categories_total': len(categories)
                        })

    @app.route('/categories/<int:cat_id>', methods=['GET'])
    def get_specific_category(cat_id):
        selection = Category.query.filter(Category.id == cat_id).one_or_none()

        return jsonify({
            'id': selection.id,
            'type': selection.type
        })

    '''
   @TODO: 
   Create a GET endpoint to get questions based on category. 

   TEST: In the "List" tab / main screen, clicking on one of the 
   categories in the left column will cause only questions of that 
   category to be shown. 
   '''

    @app.route('/categories/<int:cat_id>/questions', methods=['GET', ])
    def get_questions_for_category(cat_id):
        cat_id = cat_id + 1
        selection = Question.query.filter(Question.category == cat_id).all()
        formatted_questions = [some_model.format() for some_model in selection]

        if not formatted_questions:
            abort(404, f"No questions found for category id {cat_id}")

        json_message = {
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
        }

        return jsonify(json_message)

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        json_message = ""

        selection_questions = Question.query.order_by(Question.id).all()
        current_questions = paginate(request, selection_questions)
        selection_categories = Category.query.order_by(Category.id).all()

        if request.args.get('page', None):
            if len(current_questions) == 0:
                abort(404, "")

            categories = []

            for category in selection_categories:
                categories.append(category.type)

            json_message = {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": categories,
            }

        else:
            categories = []

            for category in selection_categories:
                categories.append(category.type)

            json_message = {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": categories,
            }

        return jsonify(json_message)

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404, "")

        question.delete()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate(request, selection)

        return jsonify({'success': True,
                        'deleted': question_id,
                        'questions': current_questions,
                        'total_questions': len(selection)})

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/questions', methods=['POST', ])
    def create_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        if question is None:
            abort(422, 'Missing question property')

        if answer is None:
            abort(422, 'Missing answer property')

        if category is None:
            abort(422, 'Missing category property')

        if difficulty is None:
            abort(422, 'Missing difficulty property')

        # Fix incoming category id is off by 1
        category = int(category) + 1

        try:
            new_question = Question(question=question,
                                    answer=answer,
                                    category=category,
                                    difficulty=difficulty)
            new_question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate(request, selection)

            return jsonify({
                'success': True,
                'id': new_question.id,
                'questions': current_questions,
                'total_questions': len(selection)
            })

        except Exception as e:
            abort(500)

        return jsonify({'success': False})

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    @app.route('/questions/search', methods=['POST', ])
    def find_question():
        body = request.get_json()

        search_term = body.get('searchTerm', None)

        if search_term is None:
            abort(422, 'Missing question search term')

        selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        if not selection:
            abort(404, f"Unable to locate any questions based on search term {search_term}")

        questions = [some_model.format() for some_model in selection]

        json_message = {
            "success": True,
            "questions": questions,
            "totalQuestions": len(questions),
            "currentCategory": None
        }

        return jsonify(json_message)

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.route('/quizzes', methods=['POST', ])
    def get_quizzes():
        body = request.get_json()
        print(body)

        previous_questions = body.get('previous_questions', None)
        print(previous_questions)

        quiz_category = body.get('quiz_category', None)

        real_id = 0

        if quiz_category['type'] == 'click':
            possible_categories = Category.query.all()
            id_list = []

            for category in possible_categories:
                id_list.append(category.id)

            real_id = random.choice(id_list)

        else:
            real_id = int(quiz_category['id'])
            real_id = real_id + 1

        print(real_id)

        selection = Question.query.filter(Question.category == real_id).all()

        if not selection:
            abort(404, f"Provided category id {quiz_category['id']} not found!")

        question_ids = []

        for question in selection:
            safe_to_add = True
            for old_question in previous_questions:
                if question.id == old_question:

                    safe_to_add = False
                    break
            if safe_to_add:
                question_ids.append(question.id)

        id_count = len(question_ids)

        picked_id = None

        if id_count > 1:
            picked_id = random.choice(question_ids)
        elif id_count == 1:
            picked_id = question_ids[0]
        else:
            abort(404, "No more questions")

        new_question = None

        for question in selection:
            if question.id == picked_id:
                new_question = question
                break

        if not new_question:
            abort(500)

        return jsonify({'success': True,
            'question': {
            'id': new_question.id,
            'question': new_question.question,
            'answer': new_question.answer,
            'category': new_question.category,
            'difficulty': new_question.difficulty
        },
        'question_count': len(question_ids)})

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(400)
    def not_found(error):
        message = "bad request"

        if error.description:
            message = error.description

        return jsonify({
            "success": False,
            "error": 400,
            "message": message
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        message = "resource not found"

        if error.description:
            message = error.description

        return jsonify({
            "success": False,
            "error": 404,
            "message": message
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        message = "bad request"

        if error.description:
            message = error.description

        return jsonify({
            "success": False,
            "error": 422,
            "message": message
        }), 422

    @app.errorhandler(405)
    def not_found(error):
        message = "method not allowed"

        if error.description:
            message = error.description

        return jsonify({
            "success": False,
            "error": 405,
            "message": message
        }), 405

    return app
