from flask_restful import Resource, fields


class BaseController(Resource):
    def __init__(self):
        self.resource_fields = {
            "status_code": fields.Integer
        }
