from tkinter import constants
from unittest import result
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from backend.controller import BaseController
from model.sys.dy_shared_user import UserModel
from backend import session, engine, api
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import json
from backend.constants import APIconstants

user_post_args = reqparse.RequestParser()
user_post_args.add_argument(
    "first_name", type=str, help="First name of the user is required", required=True)
user_post_args.add_argument("last_name", type=str,
                            help="Last name of the user", required=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("first_name", type=str,
                           help="First name of the user is required")
user_put_args.add_argument("last_name", type=str, help="Last name of the user")

resource_fields_user = {
    "id": fields.Integer,
    "last_name": fields.String,
    "first_name": fields.String,
}

base = BaseController()
resource_fields = base.resource_fields
resource_fields['user'] = fields.Nested(resource_fields_user)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class UserController(BaseController):
    def __init__(self):
        base.__init__(UserModel)

    @marshal_with(resource_fields)
    def get(self, id):
        a, b = base.callGetQuery(id)
        response = {**a, "user":b}
        return response

    @marshal_with(resource_fields)
    def post(self, id):
        args = user_post_args.parse_args()
        stmt = select(UserModel).where(UserModel.id.in_([id]))
        result = session.scalars(stmt).first()
        if (result):
            abort(404, message="id has alread been taken")
        user = UserModel(
            id=id, first_name=args["first_name"], last_name=args['last_name'])
        session.add(user)
        session.commit()
        response = {
            "status_code" : 200, 
            "message" : APIconstants.CREATED,
            "user": user
        }
        return response

    @marshal_with(resource_fields)
    def put(self, id):
        args = user_put_args.parse_args()
        stmt = select(UserModel).where(UserModel.id.in_([id]))
        user = session.scalars(stmt).first()
        if not user:
            abort(404, message="user doesn't exist, cannot update")
        if args['first_name']:
            user.first_name = args['first_name']
        if args['last_name']:
            user.last_name = args['last_name']
        session.commit()
        response = {
            "status_code":200,
            "message": APIconstants.UPDATED,
            "user":user
        }
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        stmt = select(UserModel).where(UserModel.id.in_([id]))
        user = session.scalars(stmt).first()
        response = {
            "status_code":200,
            "message":APIconstants.DELETED,
            "user":user
        }
        if not user:
            abort(404, message="user doesn't exist, cannot delete")
        session.delete(user)
        session.commit()
        return response


#api.add_resource(User, "/user/<string:first_name>")
api.add_resource(UserController, "/user/<int:id>")
# user = UserController(UserModel).get()
