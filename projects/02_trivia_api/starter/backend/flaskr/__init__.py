import os
from flask import Flask, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
KNOWN_JSON_PROPERTIES = ['question', 'answer', 'category', 'difficulty', ]


def paginate(request, selection):
    """
    Take in a web request and check for the desired output page.
    If none is provided default to page one.
    Take all objects in selection and return 10 per page.

    :param request:
    :param selection:
    :return: list
    """
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    some_models = [some_model.format() for some_model in selection]

    return some_models[start:end]


"""
Init web service
"""


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        """
        Setup response headers
        :param response:
        :return: headers
        """
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def categories():
        """
        Get all categories
        :return: json object
        """
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
        """
        Get specific category
        :param cat_id:
        :return: json object
        """
        selection = Category.query.filter(Category.id == cat_id).one_or_none()

        return jsonify({
            'id': selection.id,
            'type': selection.type
        })

    @app.route('/categories/<int:cat_id>/questions', methods=['GET', ])
    def get_questions_for_category(cat_id):
        """
        Get set of questions that are associated with a category
        :param cat_id:
        :return: json object
        """
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

    @app.route('/questions', methods=['GET'])
    def get_questions():
        """
        Get all questions in the database but paginate
        so only 10 at a time are returned. If page is requested
        return page with a max of 10 questions.

        :return: json object
        """
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

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Delete one question for provided question id
        :param question_id:
        :return: json object
        """
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if question is None:
            abort(404, "")

        question.delete()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate(request, selection)

        return jsonify({'success': True,
                        'deleted': question_id,
                        'questions': current_questions,
                        'total_questions': len(selection)})

    @app.route('/questions', methods=['POST', ])
    def create_question():
        """
        Create new question
        Note incoming category ids start at 0 so we need to
        increment the value by 1 to get desired category.

        :return: json object
        """
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

    @app.route('/questions/search', methods=['POST', ])
    def find_question():
        """
        Take in provided string and return all
        questions that partially match search term.
        :return: json object
        """
        body = request.get_json()

        search_term = body.get('searchTerm', None)

        if search_term is None:
            abort(422, 'Missing question search term')

        selection = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()

        if not selection:
            abort(
                404, f"Unable to locate any questions "
                     f"based on search term {search_term}")

        questions = [some_model.format() for some_model in selection]

        json_message = {
            "success": True,
            "questions": questions,
            "totalQuestions": len(questions),
            "currentCategory": None
        }

        return jsonify(json_message)

    @app.route('/quizzes', methods=['POST', ])
    def get_quizzes():
        """
        Generate a random set of questions for a requested category.
        If previously presented question ids are provided they will be
        excluded until all questions are exhausted. If no category is provided
        a random category and question will be returned.
        :return: json object
        """
        json_message = ""

        body = request.get_json()

        previous_questions = body.get('previous_questions', None)

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

        selection = Question.query.filter(Question.category == real_id).all()

        if not selection:
            abort(
                404, f"Provided category id {quiz_category['id']} not found!")

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

        new_question = None

        for question in selection:
            if question.id == picked_id:
                new_question = question
                break

        if new_question:
            # abort(500)
            json_message = jsonify({'success': True,
                                    'question': {
                                        'id': new_question.id,
                                        'question': new_question.question,
                                        'answer': new_question.answer,
                                        'category': new_question.category,
                                        'difficulty': new_question.difficulty
                                    },
                                    'question_count': len(question_ids)})
        else:
            json_message = jsonify({'success': False,
                                    'question': None})

        return json_message

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
