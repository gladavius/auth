# project/server/auth/views.py


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
                madb.creer_utilisateur(post_data.get('login'), post_data.get('mdp'))
                # generate the auth token
                auth_token = monuser.encode_auth_token(post_data.get('login'))
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
            user = madb.verifier_utilisateur(post_data.get('login'), post_data.get('mdp'))
            if user :
                auth_token = monuser.encode_auth_token(post_data.get('login'))
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500


class RefreshAPI(MethodView):
    """
    User Resource
    """
    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                responseObject = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    }
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401


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
refresh_view = RefreshAPI.as_view('refresh_api')
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
    '/auth/refresh',
    view_func=refresh_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/delete',
    view_func=delete_view,
    methods=['POST']
)
