import uuid
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, abort, fields, marshal_with
# from backend.auth_middleware import token_required
from backend.controller import BaseController
from model.sub.sms.dy_sms_subject import SubjectModel
from backend import api
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from backend import engine

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

view = "data"
endpoint = "subject"

subject_post_args = reqparse.RequestParser()
subject_post_args.add_argument("name", type=str, help="Name of subject is required", required=True)

subject_post_query_args = reqparse.RequestParser()
subject_post_query_args.add_argument("name", type=str,help="Name of the subject")

subject_post_ids_args = reqparse.RequestParser()
subject_post_ids_args.add_argument("ids", type=str, action="append", help="List of Ids must at least have one")

subject_put_args = reqparse.RequestParser()
subject_put_args.add_argument("name", type=str,help="Name of Subject")

resource_fields_subject = {
    "id": fields.String,
    "name": fields.String,
    "created_date" : fields.String,
    "updated_date" : fields.String,
}

base = BaseController()
resource_fields = base.resource_fields
resource_fields[view] = fields.List(fields.Nested(resource_fields_subject))

class SubjectController(BaseController):
    def __init__(self):
        super().__init__()
        self.model = SubjectModel
    
    @marshal_with(resource_fields)
    def get(self, id):
        a, b = self.callGetQuery(id)
        response = {**a, view: b}
        return response

    @marshal_with(resource_fields)
    def post(self):
        args = subject_post_args.parse_args()
        model = self.model(id=str(uuid.uuid4()), name= args["name"], created_date=self.currentDateTime, updated_date=self.currentDateTime)
        a, b = self.callPostQuery(model)
        response = {**a, view: b}
        return response

    @marshal_with(resource_fields)
    def put(self, id):
        args = subject_put_args.parse_args()
        returnData = self.queryStatement(id)
        # stmt = select(self.model).where(self.model.id.in_([id]))
        # returnData = session.scalars(stmt).first()
        if not returnData:
            abort(404, message="subject doesn't exist, cannot update")
        if args['name']:
            returnData.name = args['name']
        returnData.updated_date = self.currentDateTime
        session.commit()
        response = {**self.callPutQuery(), view: returnData}
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        a, b = self.callDeleteQuery(id)
        response = {**a, view: b}
        return response

class SubjectAllController(BaseController):
    def __init__(self):
        self.model = SubjectModel

    @marshal_with(resource_fields)
    def get(self):
        print("subject")
        a, b = self.callGetAllQuery()
        response = {**a, view: b}
        return response

class SubjectQueryController(BaseController):
    def __init__(self):
        # super().__init__("user", resource_fields_user)
        self.model = SubjectModel

    @marshal_with(resource_fields)
    def post(self):
        args = subject_post_query_args.parse_args()
        a, b = self.callGetWhereQuery(args)
        response = {**a, view:b}
        return response

class SubjectIdsController(BaseController):
    def __init__(self, model=SubjectModel):
        super().__init__(model)

    @marshal_with(resource_fields)
    def post(self):
        args = subject_post_ids_args.parse_args()
        #Get All by ids
        a, b = self.callGetAllByIdsQuery(args['ids'])
        response = {**a, view: b}
        return response
        
api.add_resource(SubjectController, "/" + endpoint + "/<string:id>", "/" + endpoint + "/")
api.add_resource(SubjectAllController,"/" + endpoint + "/all/")
api.add_resource(SubjectQueryController, "/" + endpoint + "/query/")
api.add_resource(SubjectIdsController, "/" + endpoint + "/ids/")

