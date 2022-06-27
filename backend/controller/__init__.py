from typing import Generic, TypeVar
from flask_restful import Resource, fields, marshal_with
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from backend import engine
from flask_restful import abort

from backend.constants import APIconstants

resource_fields = {
    "status_code" : fields.Integer,
    "message": fields.String,
}
T = TypeVar('T')

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class BaseController(Resource, Generic[T]):
    def __init__(self, model : T = None):
        self.resource_fields = {
            "status_code": fields.Integer,
            "message":fields.String
        }
        self.model = model
    
    def callGetQuery(self, id):
        stmt = select(self.model).where(self.model.id.in_([id]))
        # first() will return none if there was no result.
        # one() will raise an error if the result was
        user = session.scalars(stmt).first()
        if not user:
            abort(404, message="Could not find user with that id")
        # print(user.__dict__)
        # Serializing json
        #json_object = json.dumps(result, indent = 4)
        result = {
            'status_code': 200,
            'message' : APIconstants.RETRIEVED,
        }
        #response = json.dumps(marshal_with(result,resource_fields))
        return result, user
