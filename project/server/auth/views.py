from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt
from project.server.models import User
from project.server.db import Database

auth_blueprint = Blueprint('auth', __name__)
madb = Database()
monuser = User()

class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = madb.verifier_utilisateur(post_data.get('login'), post_data.get('mdp'))
        if not user:
            try:
                madb.creer_utilisateur(post_data.get('login'), post_data.get('mdp'), post_data.get('role'))
                # generate the auth token
                auth_token = monuser.encode_auth_token(post_data.get('login'), post_data.get('role'))
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


class LoginAPI(MethodView):
    """
    User Login Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            userrole = madb.verifier_utilisateur(post_data.get('login'), post_data.get('mdp'))
            if not userrole:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
            else:
                auth_token = monuser.encode_auth_token(post_data.get('login'), userrole)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(responseObject)), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500


class ModifyAPI(MethodView):
    """
    User modification Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = madb.verifier_utilisateur(post_data.get('login'), post_data.get('mdp'))
        if user:
            try:
                madb.modifier_utilisateur(post_data.get('login'), post_data.get('new_mdp'))
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully modified.'
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exists. Please use register api.',
            }
            return make_response(jsonify(responseObject)), 2


class DeleteAPI(MethodView):
    """
    Delete Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = madb.verifier_utilisateur(post_data.get('login'), post_data.get('mdp'))
        if user:
            try:
                madb.supprimer_utilisateur(post_data.get('login'))
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully deleted.'
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exists.',
            }
            return make_response(jsonify(responseObject)), 202

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
modify_view = ModifyAPI.as_view('modify_api')
delete_view = DeleteAPI.as_view('delete_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/modify',
    view_func=modify_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/delete',
    view_func=delete_view,
    methods=['POST']
)
