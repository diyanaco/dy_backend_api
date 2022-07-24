from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, abort, fields, marshal_with, marshal
# from backend.auth_middleware import token_required
from backend.controller import BaseController
from model.sys.dy_shared_user import UserModel
from backend import api
import json
from sqlalchemy.orm import sessionmaker
from backend import engine



Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("first_name", type=str, help="First name of the user is required", required=True)
user_post_args.add_argument("last_name", type=str,help="Last name of the user", required=True)
user_post_args.add_argument("email", type=str,help="Email of the user", required=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("first_name", type=str,help="First name of the user ")
user_put_args.add_argument("last_name", type=str, help="Last name of the user")

resource_fields_user = {
    "id": fields.String,
    "last_name": fields.String,
    "first_name": fields.String,
}

base = BaseController()
resource_fields = base.resource_fields
# resource_fields['user'] = fields.Nested(resource_fields_user)
resource_fields['user'] = fields.List(fields.Nested(resource_fields_user))

class UserController(BaseController):
    def __init__(self):
        # super().__init__("user", resource_fields_user)
        self.model = UserModel
    
    @marshal_with(resource_fields)
    def get(self, id):
        #Get by Id
        a, b = self.callGetQuery(id)
        print("FirstName")
        print(b.first_name)

        response = {**a, "user": b}
        return response

    #Post is done in UserAuthController
    # @marshal_with(resource_fields)
    # def post(self):
    #     args = user_post_args.parse_args()
    #     a, b = self.callPostQuery( args)
    #     response = {**a, "user": b}
    #     return response

    @marshal_with(resource_fields)
    def put(self, id):
        args = user_put_args.parse_args()
        # a, b = self.callPutQuery(id, args)
        returnData = self.queryStatement(id)
        if not returnData:
            abort(404, message="user doesn't exist, cannot update")
        if args['first_name']:
            returnData.first_name = args['first_name']
        if args['last_name']:
            returnData.last_name = args['last_name']
        session.commit()
        response = {**self.callPutQuery(), "user": returnData}
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        a, b = self.callDeleteQuery(id)
        response = {**a, "user": b}
        return response

class UserQueryController(BaseController):
    def __init__(self):
        # super().__init__("user", resource_fields_user)
        self.model = UserModel
    @marshal_with(resource_fields)
    def get(self):
        print("Hello Baby")

class UserAllController(BaseController):
    def __init__(self):
        # super().__init__("user", resource_fields_user)
        self.model = UserModel

    # @jwt_required()
    @marshal_with(resource_fields)
    def get(self):
        #Get All
        a, b = self.callGetAllQuery()
        # print(json.dumps(marshal(b, resource_fields_testing)))
        response = {**a, "user": b}
        return response

#api.add_resource(User, "/user/<string:first_name>")
api.add_resource(UserController, "/user/<string:id>")
api.add_resource(UserAllController, "/user/all/")
api.add_resource(UserQueryController, "/user/query")
# user = UserController(UserModel).get()
