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
        response = {**a, "user": b}
        return response

    @marshal_with(resource_fields)
    def post(self, id):
        args = user_post_args.parse_args()
        a, b = base.callPostQuery(id, args)
        response = {**a, "user": b}
        return response

    @marshal_with(resource_fields)
    def put(self, id):
        args = user_put_args.parse_args()
        a, b = base.callPutQuery(id, args)
        response = {**a, "user": b}
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        a, b = base.callDeleteQuery(id)
        response = {**a, "user": b}
        return response


#api.add_resource(User, "/user/<string:first_name>")
api.add_resource(UserController, "/user/<int:id>")
# user = UserController(UserModel).get()
