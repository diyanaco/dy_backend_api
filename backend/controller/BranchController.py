import uuid
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, abort, fields, marshal_with
from backend.controller import BaseController
from model.sub.sms.dy_sms_guardian import GuardianModel
from backend import api
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from backend import engine

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
base = BaseController()
Model = GuardianModel
field1 = "name"
field2 = "type"
view = "branch"

guardian_post_args = reqparse.RequestParser()
guardian_post_args.add_argument(
    field1, type=str, help="User ID of guardian is required", required=True)
guardian_post_args.add_argument(
    field2, type=str, help="User ID of guardian is required", required=True)

guardian_post_query_args = reqparse.RequestParser()
guardian_post_query_args.add_argument(
    field1, type=str, help="User ID of the guardian")
guardian_post_query_args.add_argument(
    field2, type=str, help="User ID of the guardian")

guardian_post_ids_args = reqparse.RequestParser()
guardian_post_ids_args.add_argument(
    "ids", type=str, action="append", help="List of Ids must at least have one")

guardian_put_args = reqparse.RequestParser()
guardian_put_args.add_argument(field1, type=str, help="User ID of Guardian")
guardian_put_args.add_argument(field2, type=str, help="User ID of Guardian")

resource_fields_guardian = {
    "id": fields.String,
    field1: fields.String,
    field2: fields.String,
    "created_date": fields.String,
    "updated_date": fields.String,
}

resource_fields = base.resource_fields
resource_fields[view] = fields.List(fields.Nested(resource_fields_guardian))

class BranchController(BaseController):
    def __init__(self):
        super().__init__()
        self.model = Model

    @marshal_with(resource_fields)
    def get(self, id):
        a, b = self.callGetQuery(id)
        response = {**a, view: b}
        return response

    @marshal_with(resource_fields)
    def post(self):
        args = guardian_post_args.parse_args()
        model = self.model(id=str(uuid.uuid4()),
                           primary_user_id=args[field1],
                           secondary_user_id=args[field2],
                           created_date=self.currentDateTime,
                           updated_date=self.currentDateTime)
        a, b = self.callPostQuery(model)
        response = {**a, view: b}
        return response

    @marshal_with(resource_fields)
    def put(self, id):
        args = guardian_put_args.parse_args()
        returnData = self.queryStatement(id)

        if not returnData:
            abort(404, message="guardian doesn't exist, cannot update")
        if args[field1]:
            returnData.primary_user_id = args[field1]
        if args['secondary_user_id']:
            returnData.secondary_user_id = args['secondary_user_id']
        returnData.updated_date = self.currentDateTime
        session.commit()
        response = {**self.callPutQuery(), view: returnData}
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        a, b = self.callDeleteQuery(id)
        response = {**a, view: b}
        return response


class BranchAllController(BaseController):
    def __init__(self):
        self.model = Model

    @marshal_with(resource_fields)
    def get(self):
        a, b = self.callGetAllQuery()
        response = {**a, view: b}
        return response


class BranchQueryController(BaseController):
    def __init__(self):
        self.model = Model

    @marshal_with(resource_fields)
    def post(self):
        args = guardian_post_query_args.parse_args()
        a, b = self.callGetWhereQuery(args)
        response = {**a, view: b}
        return response


class BranchIdsController(BaseController):
    def __init__(self, model=Model):
        super().__init__(model)

    @marshal_with(resource_fields)
    def post(self):
        args = guardian_post_ids_args.parse_args()
        # Get All by ids
        a, b = self.callGetAllByIdsQuery(args['ids'])
        response = {**a, view: b}
        return response


api.add_resource(BranchController, "/" + view +"/<string:id>", "/" + view + "/")
api.add_resource(BranchAllController, "/" + view +"/all/")
api.add_resource(BranchQueryController, "/" + view +"/query/")
api.add_resource(BranchIdsController, "/" + view + "/ids/")
