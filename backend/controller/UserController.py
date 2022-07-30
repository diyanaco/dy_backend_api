import argparse
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, abort, fields, marshal_with, marshal
# from backend.auth_middleware import token_required
from backend.controller import BaseController
from model.sys.dy_shared_user import UserModel
from backend import api
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from backend import engine



Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("first_name", type=str, help="First name of the user is required", required=True)
user_post_args.add_argument("last_name", type=str,help="Last name of the user", required=True)
user_post_args.add_argument("email", type=str,help="Email of the user", required=True)

user_post_query_args = reqparse.RequestParser()
user_post_query_args.add_argument("first_name", type=str, help="First name of the user is required")
user_post_query_args.add_argument("last_name", type=str,help="Last name of the user")
user_post_query_args.add_argument("email", type=str,help="Email of the user")

user_post_ids_args = reqparse.RequestParser()
user_post_ids_args.add_argument("ids", type=str, action="append", help="List of Ids must at least have one")

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("first_name", type=str,help="First name of the user ")
user_put_args.add_argument("last_name", type=str, help="Last name of the user")

resource_fields_user = {
    "id": fields.String,
    "last_name": fields.String,
    "first_name": fields.String,
    "email" : fields.String,
    "created_date" : fields.String,
    "updated_date" : fields.String,
}

base = BaseController()
resource_fields = base.resource_fields
# resource_fields['user'] = fields.Nested(resource_fields_user)
resource_fields['data'] = fields.List(fields.Nested(resource_fields_user))

class UserController(BaseController):
    def __init__(self):
        super().__init__()
        self.model = UserModel
    
    @marshal_with(resource_fields)
    def get(self, id):
        #Get by Id
        a, b = self.callGetQuery(id)
        response = {**a, "data": b}
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
        returnData = self.queryStatement(id)
        # stmt = select(self.model).where(self.model.id.in_([id]))
        # returnData =  session.scalars(stmt).first()
        if not returnData:
            abort(404, message="user doesn't exist, cannot update")
        if args['first_name']:
            returnData.first_name = args['first_name']
        if args['last_name']:
            returnData.last_name = args['last_name']
        returnData.updated_date = self.currentDateTime
        session.commit()
        response = {**self.callPutQuery(), "data": returnData}
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        a, b = self.callDeleteQuery(id)
        response = {**a, "data": b}
        return response

#TODO #30 : Implement search by criteria
class UserQueryController(BaseController):
    def __init__(self):
        # super().__init__("user", resource_fields_user)
        self.model = UserModel

    @marshal_with(resource_fields)
    def post(self):
        args = user_post_query_args.parse_args()
        print("Hello World")
        print(args)
        a, b = self.callGetWhereQuery(args)
        response = {**a, "data":b}
        return response

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
        response = {**a, "data": b}
        return response
class UserIdsController(BaseController):
    def __init__(self, model=UserModel):
        super().__init__(model)

    @marshal_with(resource_fields)
    def post(self):
        args = user_post_ids_args.parse_args()
        #Get All by ids
        a, b = self.callGetAllByIdsQuery(args['ids'])
        response = {**a, "data": b}
        return response
#api.add_resource(User, "/user/<string:first_name>")
api.add_resource(UserController, "/user/<string:id>")
api.add_resource(UserAllController, "/user/all/")
api.add_resource(UserQueryController, "/user/query/")
api.add_resource(UserIdsController, "/user/ids/")
# user = UserController(UserModel).get()
