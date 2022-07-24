from flask_jwt_extended import jwt_required
from flask_restful import reqparse, abort, fields, marshal_with
# from backend.auth_middleware import token_required
from backend.controller import BaseController
from model.sub.sms.dy_sms_student import StudentModel
from backend import api

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("first_name", type=str, help="First name of the user is required", required=True)
user_post_args.add_argument("last_name", type=str,help="Last name of the user", required=True)
user_post_args.add_argument("email", type=str,help="Email of the user", required=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("first_name", type=str,help="First name of the user is required")
user_put_args.add_argument("last_name", type=str, help="Last name of the user")

resource_fields_user = {
    "id": fields.Integer,
    "last_name": fields.String,
    "first_name": fields.String,
}

base = BaseController()
resource_fields = base.resource_fields
resource_fields['user'] = fields.Nested(resource_fields_user)



class StudentController(BaseController):
    def __init__(self):
        self.model = StudentModel
    
    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, id):
        a, b = self.callGetQuery(id)
        response = {**a, "user": b}
        return response

    @marshal_with(resource_fields)
    def post(self, id):
        args = user_post_args.parse_args()
        a, b = self.callPostQuery(id, args)
        response = {**a, "user": b}
        return response

    @marshal_with(resource_fields)
    def put(self, id):
        args = user_put_args.parse_args()
        a, b = self.callPutQuery(id, args)
        response = {**a, "user": b}
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        a, b = self.callDeleteQuery(id)
        response = {**a, "user": b}
        return response

#api.add_resource(User, "/user/<string:first_name>")
api.add_resource(StudentController, "/student/<int:id>")
# user = StudentController(StudentModel).get()
