import uuid
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, abort, fields, marshal_with
from backend.controller import BaseController
from backend import api
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from backend import engine
from model.sub.sms.dy_sms_payment import PaymentModel

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
base = BaseController()
Model = PaymentModel
field1 = "name"
field2 = "student_id"
field3 = "amount"
view = "payment"

payment_post_args = reqparse.RequestParser()
payment_post_args.add_argument(
    field1, type=str, help="Name of payment is required", required=True)
payment_post_args.add_argument(
    field2, type=str, help="Student ID of payment is required", required=True)
payment_post_args.add_argument(
    field3, type=float, help="Amount of payment is required", required=True)

payment_post_query_args = reqparse.RequestParser()
payment_post_query_args.add_argument(
    field1, type=str, help="Name of the payment")
payment_post_query_args.add_argument(
    field2, type=str, help="Student ID of the payment")
payment_post_query_args.add_argument(
    field3, type=float, help="Amount of the payment")

payment_post_ids_args = reqparse.RequestParser()
payment_post_ids_args.add_argument(
    "ids", type=str, action="append", help="List of Ids must at least have one")

payment_put_args = reqparse.RequestParser()
payment_put_args.add_argument(field1, type=str, help="Name of Guardian")
payment_put_args.add_argument(field2, type=str, help="Student ID of Guardian")
payment_put_args.add_argument(field3, type=float, help="Student ID of Guardian")

resource_fields_payment = {
    "id": fields.String,
    field1: fields.String,
    field2: fields.String,
    field3: fields.Float,
    "created_date": fields.String,
    "updated_date": fields.String,
}

resource_fields = base.resource_fields
resource_fields[view] = fields.List(fields.Nested(resource_fields_payment))


class PaymentController(BaseController):
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
        args = payment_post_args.parse_args()
        model = self.model(id=str(uuid.uuid4()),
                           name=args[field1],
                           student_id = args[field2],
                           amount = args[field3],
                           created_date=self.currentDateTime,
                           updated_date=self.currentDateTime)
        a, b = self.callPostQuery(model)
        response = {**a, view: b}
        return response

    @marshal_with(resource_fields)
    def put(self, id):
        args = payment_put_args.parse_args()
        returnData = self.queryStatement(id)

        if not returnData:
            abort(404, message="class doesn't exist, cannot update")
        if args[field1]:
            returnData.name = args[field1]
        if args[field2]:
            returnData.student_id = args[field2]
        if args[field3]:
            returnData.amount = args[field3]
        returnData.updated_date = self.currentDateTime
        session.commit()
        response = {**self.callPutQuery(), view: returnData}
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        a, b = self.callDeleteQuery(id)
        response = {**a, view: b}
        return response


class PaymentAllController(BaseController):
    def __init__(self):
        self.model = Model

    @marshal_with(resource_fields)
    def get(self):
        a, b = self.callGetAllQuery()
        response = {**a, view: b}
        return response


class PaymentQueryController(BaseController):
    def __init__(self):
        self.model = Model

    @marshal_with(resource_fields)
    def post(self):
        args = payment_post_query_args.parse_args()
        a, b = self.callGetWhereQuery(args)
        response = {**a, view: b}
        return response


class PaymentIdsController(BaseController):
    def __init__(self, model=Model):
        super().__init__(model)

    @marshal_with(resource_fields)
    def post(self):
        args = payment_post_ids_args.parse_args()
        # Get All by ids
        a, b = self.callGetAllByIdsQuery(args['ids'])
        response = {**a, view: b}
        return response


api.add_resource(PaymentController, "/" + view +
                 "/<string:id>", "/" + view + "/")
api.add_resource(PaymentAllController, "/" + view + "/all/")
api.add_resource(PaymentQueryController, "/" + view + "/query/")
api.add_resource(PaymentIdsController, "/" + view + "/ids/")
