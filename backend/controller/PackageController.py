import uuid
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, abort, fields, marshal_with
from backend.controller import BaseController
from model.sub.sms.dy_sms_package import PackageModel
from backend import api
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from backend import engine

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
base = BaseController()
Model = PackageModel
field1 = "name"
field2 = "level_id"
field3 = "package_set_id"
field4 = "subject_id"

# field2 = "user_id"
view = "data"
endpoint = "package"

package_post_args = reqparse.RequestParser()
package_post_args.add_argument(
    field1, type=str, help="Name of package is required", required=True)
package_post_args.add_argument(
    field2, type=str, help="Level Id of package is required", required=True)
package_post_args.add_argument(
    field3, type=str, help="Package Set Id of package is required", required=True)
package_post_args.add_argument(
    field4, type=str, help="Subject Id of package is required", required=True)

package_post_query_args = reqparse.RequestParser()
package_post_query_args.add_argument(
    field1, type=str, help="Name of the package")
package_post_query_args.add_argument(
    field2, type=str, help="Level ID of the package")
package_post_query_args.add_argument(
    field3, type=str, help="Package Set ID of the package")
package_post_query_args.add_argument(
    field4, type=str, help="Subject ID of the package")

package_post_ids_args = reqparse.RequestParser()
package_post_ids_args.add_argument(
    "ids", type=str, action="append", help="List of Ids must at least have one")

package_put_args = reqparse.RequestParser()
package_put_args.add_argument(field1, type=str, help="Name of package")
package_put_args.add_argument(field2, type=str, help="Level ID of package")
package_put_args.add_argument(field3, type=str, help="Package Set of package")
package_put_args.add_argument(field4, type=str, help="Subject ID of package")

resource_fields_package = {
    "id": fields.String,
    field1: fields.String,
    field2: fields.String,
    field3: fields.String,
    field4: fields.String,
    "created_date": fields.String,
    "updated_date": fields.String,
}

resource_fields = base.resource_fields
resource_fields[view] = fields.List(fields.Nested(resource_fields_package))


class PackageController(BaseController):
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
        args = package_post_args.parse_args()
        model = self.model(id=str(uuid.uuid4()),
                           name=args[field1],
                           level_id = args[field2],
                           package_set_id = args[field3],
                           subject_id = args[field4],
                           created_date=self.currentDateTime,
                           updated_date=self.currentDateTime)
        a, b = self.callPostQuery(model)
        response = {**a, view: b}
        return response

    @marshal_with(resource_fields)
    def put(self, id):
        args = package_put_args.parse_args()
        returnData = self.queryStatement(id)

        if not returnData:
            abort(404, message="class doesn't exist, cannot update")
        if args[field1]:
            returnData.name = args[field1]
        if args[field2]:
            returnData.level_id = args[field2]
        if args[field3]:
            returnData.package_set_id = args[field3]
        if args[field4]:
            returnData.subject_id = args[field4]
        
        returnData.updated_date = self.currentDateTime
        session.commit()
        response = {**self.callPutQuery(), view: returnData}
        return response

    @marshal_with(resource_fields)
    def delete(self, id):
        a, b = self.callDeleteQuery(id)
        response = {**a, view: b}
        return response


class PackageAllController(BaseController):
    def __init__(self):
        self.model = Model

    @marshal_with(resource_fields)
    def get(self):
        a, b = self.callGetAllQuery()
        response = {**a, view: b}
        return response


class PackageQueryController(BaseController):
    def __init__(self):
        self.model = Model

    @marshal_with(resource_fields)
    def post(self):
        args = package_post_query_args.parse_args()
        a, b = self.callGetWhereQuery(args)
        response = {**a, view: b}
        return response


class PackageIdsController(BaseController):
    def __init__(self, model=Model):
        super().__init__(model)

    @marshal_with(resource_fields)
    def post(self):
        args = package_post_ids_args.parse_args()
        # Get All by ids
        a, b = self.callGetAllByIdsQuery(args['ids'])
        response = {**a, view: b}
        return response


api.add_resource(PackageController, "/" + endpoint +
                 "/<string:id>", "/" + endpoint + "/")
api.add_resource(PackageAllController, "/" + endpoint + "/all/")
api.add_resource(PackageQueryController, "/" + endpoint + "/query/")
api.add_resource(PackageIdsController, "/" + endpoint + "/ids/")
