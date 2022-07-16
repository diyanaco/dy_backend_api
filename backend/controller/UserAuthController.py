from backend import api
from backend.controller import BaseController
from flask import request, jsonify
from backend.controller.UserController import UserController
from model.sys.dy_shared_user import UserModel
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from backend import engine
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from backend import app
from flask_restful import abort, fields, marshal_with
import uuid
from flask_jwt_extended import create_access_token, create_refresh_token

resource_fields_user_auth = {
    "email": fields.String,
    "password" : fields.String,
    'access-token' : fields.String,
    'refresh_token' : fields.String,
}

base = BaseController()
resource_fields = base.resource_fields
resource_fields['user_auth'] = fields.Nested(resource_fields_user_auth)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class AuthLoginController(BaseController):
    def get(self):
        print("hello")
        try:
            userRequest = request.json
            print(userRequest)
            if not userRequest:
                return {
                    "message": "Please provide user details",
                    "userRequest": None,
                    "error": "Bad request"
                }, 400
            #query user data
            stmt = select(UserModel).where(UserModel.email.in_([userRequest['email']]))
            user = session.scalars(stmt).first()
            #Check user hash password with given password through login
            if not user or not check_password_hash(user.password, userRequest['password']):
                print("goodbye")
                return {
                    "message": "Your credentials are wrong",
                }, 400
            if user:
                try:
                    access_token = create_access_token(identity = user.id)
                    refresh_token = create_refresh_token(identity = user.id)
                    return {
                        "message": "Successfully fetched auth token",
                        "user_auth": {
                            "access-token" : access_token,
                            "refresh-token" : refresh_token
                        }
                    }
                except Exception as e:
                    return {
                        "error": "Something went wrong",
                        "message": str(e)
                    }, 500
            return {
                "message": "Error fetching auth token!, invalid email or password",
                "data": None,
                "error": "Unauthorized"
            }, 404
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
            }, 500

class AuthSignupController(BaseController):
    @marshal_with(resource_fields)
    def post(self):
        try:
            userRequest = request.json
            if not userRequest:
                return {
                    "status_code": 400,
                    "message": "Please provide user details",
                    "user_auth": None,
                    "error": "Bad request"
                }, 400

            """Create a new user"""
            stmt = select(UserModel).where(UserModel.email.in_([userRequest['email']]))
            user = session.scalars(stmt).first()
            access_token = create_access_token(identity = user.id)
            refresh_token = create_refresh_token(identity = user.id)
            if user:
                return {
                    "status_code" : 404,
                    "message" : "Email has already been taken",
                    "user_auth" : {
                        "access-token" : access_token,
                        "refresh-token" : refresh_token
                    }
                }
            modifiedUser = UserModel(id=str(uuid.uuid4()), first_name=userRequest["first_name"], last_name=userRequest['last_name'],email=userRequest["email"], password=generate_password_hash(userRequest['password']))
            session.add(modifiedUser)
            session.commit()
            return {
                "status_code" : 201,
                "message": "Successfully created new user",
                "user_auth": modifiedUser
            }, 201
        except Exception as e:
            return {
                "status_code": 500,
                "error": str(e),
            }, 500

api.add_resource(AuthLoginController, "/user/login")
#api.add_resource(UserAuthController, "/user/signup", endpoint='signup', methods=['POST'])
api.add_resource(AuthSignupController, "/user/signup")