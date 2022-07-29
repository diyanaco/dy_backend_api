import uuid
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, abort, fields, marshal_with
from backend.controller import BaseController
from model.sub.sms.dy_sms_class import ClassModel
from backend import api
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from backend import engine
from model.sys.dy_shared_branch import ClassModel

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
base = BaseController()
Model = ClassModel
field1 = "name"
# field2 = "type"
view = "class"

class_post_args = reqparse.RequestParser()
class_post_args.add_argument(
    field1, type=str, help="User ID of class is required", required=True)
# class_post_args.add_argument(
#     field2, type=str, help="User ID of class is required", required=True)

class_post_query_args = reqparse.RequestParser()
class_post_query_args.add_argument(
    field1, type=str, help="User ID of the class")
# class_post_query_args.add_argument(
#     field2, type=str, help="User ID of the class")

class_post_ids_args = reqparse.RequestParser()
class_post_ids_args.add_argument(
    "ids", type=str, action="append", help="List of Ids must at least have one")

class_put_args = reqparse.RequestParser()
class_put_args.add_argument(field1, type=str, help="User ID of Guardian")
# class_put_args.add_argument(field2, type=str, help="User ID of Guardian")

resource_fields_class = {
    "id": fields.String,
    field1: fields.String,
    # field2: fields.String,
    "created_date": fields.String,
    "updated_date": fields.String,
}

resource_fields = base.resource_fields
resource_fields[view] = fields.List(fields.Nested(resource_fields_class))

class ClassController(BaseController):
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
        args = class_post_args.parse_args()
        model = self.model(id=str(uuid.uuid4()),
                           name=args[field1],
                           created_date=self.currentDateTime,
                           updated_date=self.currentDateTime)
        a, b = self.callPostQuery(model)
        response = {**a, view: b}
        return response

    @marshal_with(resource_fields)
    def put(self, id):
        args = class_put_args.parse_args()
        returnData = self.queryStatement(id)

        if not returnData:
            abort(404, message="class doesn't exist, cannot update")
        if args[field1]:
            returnData.name = args[field1]
        # if args[field2]:
        #     returnData.type = args[field2]
        returnData.updated_date = self.currentDateTime
        session.commit()
        response = {**self.callPutQuery(), view: returnData}
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        a, b = self.callDeleteQuery(id)
        response = {**a, view: b}
        return response


class ClassAllController(BaseController):
    def __init__(self):
        self.model = Model

    @marshal_with(resource_fields)
    def get(self):
        a, b = self.callGetAllQuery()
        response = {**a, view: b}
        return response


class ClassQueryController(BaseController):
    def __init__(self):
        self.model = Model

    @marshal_with(resource_fields)
    def post(self):
        args = class_post_query_args.parse_args()
        a, b = self.callGetWhereQuery(args)
        response = {**a, view: b}
        return response


class ClassIdsController(BaseController):
    def __init__(self, model=Model):
        super().__init__(model)

    @marshal_with(resource_fields)
    def post(self):
        args = class_post_ids_args.parse_args()
        # Get All by ids
        a, b = self.callGetAllByIdsQuery(args['ids'])
        response = {**a, view: b}
        return response


api.add_resource(ClassController, "/" + view +"/<string:id>", "/" + view + "/")
api.add_resource(ClassAllController, "/" + view +"/all/")
api.add_resource(ClassQueryController, "/" + view +"/query/")
api.add_resource(ClassIdsController, "/" + view + "/ids/")
