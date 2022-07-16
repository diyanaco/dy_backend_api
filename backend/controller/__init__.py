from typing import Generic, TypeVar
from flask_restful import Resource, fields, marshal_with
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from backend import engine
from flask_restful import abort

from backend.constants import APIconstants
from model.sys.dy_shared_user import UserModel

resource_fields = {
    "status_code" : fields.Integer,
    "message": fields.String,
}
#T = TypeVar('T')

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class BaseController(Resource):
    def __init__(self, model=None):
        self.resource_fields = {
            "status_code": fields.Integer,
            "message":fields.String,
            "error": fields.String
        }
        self.model = model
    
    def callGetQuery(self, id,):
        print(self)
        returnData = self.queryStatement(id)
        if not returnData:
            abort(404, message="Could not find user with that id")
        result = {
            'status_code': 200,
            'message' : APIconstants.RETRIEVED,
        }
        return result, returnData

    def callPostQuery(self, id, args):
        returnData = self.queryStatement(id)
        if returnData:
            abort(404, message="id has already been taken")
        modifiedData = self.model(id=id, first_name=args["first_name"], last_name=args['last_name'])
        session.add(modifiedData)
        session.commit()
        result = {
            'status_code': 200,
            'message' : APIconstants.CREATED,
        }
        return result, modifiedData

    def callPutQuery(self, id, args):
        returnData = self.queryStatement(id)
        if not returnData:
            abort(404, message="user doesn't exist, cannot update")
        if args['first_name']:
            returnData.first_name = args['first_name']
        if args['last_name']:
            returnData.last_name = args['last_name']
        session.commit()
        result = {
            'status_code': 200,
            'message' : APIconstants.UPDATED,
        }
        return result, returnData

    def callDeleteQuery(self, id):
        returnData = self.queryStatement(id)
        if not returnData:
            abort(404, message="user doesn't exist, cannot delete")
        session.delete(returnData)
        session.commit()
        response = {
            "status_code":200,
            "message":APIconstants.DELETED,
        }
        return response, returnData

    def queryStatement(self,id):
        stmt = select(self.model).where(self.model.id.in_([id]))
        return session.scalars(stmt).first()
