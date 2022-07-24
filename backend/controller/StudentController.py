import uuid
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, abort, fields, marshal_with
# from backend.auth_middleware import token_required
from backend.controller import BaseController
from model.sub.sms.dy_sms_student import StudentModel
from backend import api
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from backend import engine

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

student_post_args = reqparse.RequestParser()
student_post_args.add_argument("user_id", type=str, help="User ID of Student is required", required=True)
student_post_args.add_argument("fav_sub", type=str, help="Fav subject of Student")

student_put_args = reqparse.RequestParser()
student_put_args.add_argument("user_id", type=str,help="User ID of Student")
student_put_args.add_argument("fav_sub", type=str,help="Fav subject of Student")

resource_fields_student = {
    "id": fields.String,
    "user_id": fields.String,
    "fav_sub" : fields.String,
    "created_date" : fields.String,
    "updated_date" : fields.String,
}

base = BaseController()
resource_fields = base.resource_fields
resource_fields['student'] = fields.List(fields.Nested(resource_fields_student))



class StudentController(BaseController):
    def __init__(self):
        super().__init__()
        self.model = StudentModel
    
    @marshal_with(resource_fields)
    def get(self, id):
        a, b = self.callGetQuery(id)
        response = {**a, "student": b}
        return response

    @marshal_with(resource_fields)
    def post(self):
        args = student_post_args.parse_args()
        model = self.model(id=str(uuid.uuid4()), user_id= args["user_id"], fav_sub=args["fav_sub"], created_date=self.currentDateTime, updated_date=self.currentDateTime)
        a, b = self.callPostQuery(model)
        response = {**a, "student": b}
        return response

    @marshal_with(resource_fields)
    def put(self, id):
        args = student_put_args.parse_args()
        returnData = self.queryStatement(id)
        stmt = select(self.model).where(self.model.id.in_([id]))
        returnData = session.scalars(stmt).first()
        if not returnData:
            abort(404, message="user doesn't exist, cannot update")
        if args['user_id']:
            returnData.user_id = args['user_id']
        if args['fav_sub']:
            returnData.fav_sub = args['fav_sub']
        returnData.updated_date = self.currentDateTime
        session.commit()
        # a, b = self.callPutQuery(id, args)
        response = {**self.callPutQuery(), "student": returnData}
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        a, b = self.callDeleteQuery(id)
        response = {**a, "student": b}
        return response

class StudentAllController(BaseController):
    def __init__(self):
        self.model = StudentModel

    @marshal_with(resource_fields)
    def get(self):
        a, b = self.callGetAllQuery()
        print(type(b))
        for i in b:
            print("Mualalala")
            print(i.user_id)
        response = {**a, "student": b}
        return response

api.add_resource(StudentController, "/student/<string:id>", "/student/")
api.add_resource(StudentAllController,"/student/all/")
