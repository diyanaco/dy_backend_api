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
student_post_args.add_argument("guardian_id", type=str, help="Guardian of Student")
student_post_args.add_argument("package_set_id", type=str, help="Package Set of Student")
student_post_args.add_argument("education_id", type=str, help="Education of Student")
student_post_args.add_argument("level_id", type=str, help="Level of Student")

student_post_query_args = reqparse.RequestParser()
student_post_query_args.add_argument("fav_sub", type=str,help="Fav subject of the student")
student_post_query_args.add_argument("guardian_id", type=str, help="Guardian of Student")
student_post_query_args.add_argument("package_set_id", type=str, help="Package Set of Student")
student_post_query_args.add_argument("education_id", type=str, help="Education of Student")
student_post_query_args.add_argument("level_id", type=str, help="Level of Student")

student_post_ids_args = reqparse.RequestParser()
student_post_ids_args.add_argument("ids", type=str, action="append", help="List of Ids must at least have one")

student_put_args = reqparse.RequestParser()
student_put_args.add_argument("user_id", type=str,help="User ID of Student")
student_put_args.add_argument("fav_sub", type=str,help="Fav subject of Student")
student_put_args.add_argument("guardian_id", type=str, help="Guardian of Student")
student_put_args.add_argument("package_set_id", type=str, help="Package Set of Student")
student_put_args.add_argument("education_id", type=str, help="Education of Student")
student_put_args.add_argument("level_id", type=str, help="Level of Student")
resource_fields_student = {
    "id": fields.String,
    "user_id": fields.String,
    "fav_sub" : fields.String,
    "guardian_id" : fields.String,
    "package_set_id" : fields.String,
    "education_id" : fields.String,
    "level_id" : fields.String,
    "created_date" : fields.String,
    "updated_date" : fields.String,
}

base = BaseController()
resource_fields = base.resource_fields
#TODO #53 change student to data 
#In frontend, the response key is data
#Need to change to all controller
resource_fields['student'] = fields.List(fields.Nested(resource_fields_student))
view = "student"

class StudentController(BaseController):
    def __init__(self):
        super().__init__()
        self.model = StudentModel
    
    @marshal_with(resource_fields)
    def get(self, id):
        a, b = self.callGetQuery(id)
        response = {**a, view: b}
        return response

    @marshal_with(resource_fields)
    def post(self):
        args = student_post_args.parse_args()
        model = self.model(id=str(uuid.uuid4()), user_id= args["user_id"], fav_sub=args["fav_sub"], created_date=self.currentDateTime, updated_date=self.currentDateTime)
        a, b = self.callPostQuery(model)
        response = {**a, view: b}
        return response

    @marshal_with(resource_fields)
    def put(self, id):
        args = student_put_args.parse_args()
        returnData = self.queryStatement(id)
        # stmt = select(self.model).where(self.model.id.in_([id]))
        # returnData = session.scalars(stmt).first()
        if not returnData:
            abort(404, message="Student doesn't exist, cannot update")
        if args['user_id']:
            returnData.user_id = args['user_id']
        if args['fav_sub']:
            returnData.fav_sub = args['fav_sub']
        returnData.updated_date = self.currentDateTime
        session.commit()
        # a, b = self.callPutQuery(id, args)
        response = {**self.callPutQuery(), view: returnData}
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        a, b = self.callDeleteQuery(id)
        response = {**a, view: b}
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
        response = {**a, view: b}
        return response
class StudentQueryController(BaseController):
    def __init__(self):
        # super().__init__("user", resource_fields_user)
        self.model = StudentModel

    @marshal_with(resource_fields)
    def post(self):
        args = student_post_query_args.parse_args()
        a, b = self.callGetWhereQuery(args)
        response = {**a, view:b}
        return response
class StudentIdsController(BaseController):
    def __init__(self, model=StudentModel):
        super().__init__(model)

    @marshal_with(resource_fields)
    def post(self):
        args = student_post_ids_args.parse_args()
        #Get All by ids
        a, b = self.callGetAllByIdsQuery(args['ids'])
        response = {**a, view: b}
        return response
        
api.add_resource(StudentController, "/student/<string:id>", "/student/")
api.add_resource(StudentAllController,"/student/all/")
api.add_resource(StudentQueryController, "/student/query/")
api.add_resource(StudentIdsController, "/student/ids/")

