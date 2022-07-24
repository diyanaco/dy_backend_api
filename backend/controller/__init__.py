from typing import Generic, TypeVar
import uuid
from flask_restful import Resource, fields, marshal_with
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from backend import engine
from flask_restful import abort

from backend.constants import APIconstants
from model.sys.dy_shared_user import UserModel

import datetime

resource_fields = {
    "status_code": fields.Integer,
    "message": fields.String,
}
# T = TypeVar('T')

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class BaseController(Resource):
    def __init__(self, model=None, ):
        # self.resource_fields = {
        #     "status_code": fields.Integer,
        #     "message":fields.String,
        #     "error": fields.String,
        #     model_name : model_resource_field
        # }
        self.resource_fields = {
            "status_code": fields.Integer,
            "message": fields.String,
            "error": fields.String,
        }
        self.model = model
        self.currentDateTime = datetime.datetime.now().astimezone().isoformat()
    
    def callGetQuery(self, id,):
        returnData = self.queryStatement(id)
        if not returnData:
            abort(404, message="Could not find user with that id")
        result = {
            'status_code': 200,
            'message' : APIconstants.RETRIEVED,
        }
        return result, returnData

    def callGetAllQuery(self):
        returnData = self.queryStatement()
        if not returnData:
            abort(404, message="The table is empty")
        result = {
            'status_code': 200,
            'message' : APIconstants.RETRIEVED,
        }
        return result, returnData

    def callGetWhereQuery(self, whereCol):
        returnData = self.queryStatement(whereCol=whereCol)
        if not returnData:
            abort(404, message="The table is empty")
        result = {
            'status_code': 200,
            'message' : APIconstants.RETRIEVED,
        }
        return result, returnData
    
    def callGetAllByIdsQuery(self, ids):
        returnData = self.queryStatement(ids=ids)
        if not returnData:
            abort(404, message="None of the Ids exist")
        result = {
            'status_code': 200,
            'message' : APIconstants.RETRIEVED,
        }
        return result, returnData

    def callPostQuery(self, modifiedData):
        # returnData = self.queryStatement(id)
        # if returnData:
        #     abort(404, message="id has already been taken")
        # modifiedData = self.model(id=str(uuid.uuid4), first_name=args["first_name"], last_name=args['last_name'])
        session.add(modifiedData)
        session.commit()
        result = {
            'status_code': 200,
            'message' : APIconstants.CREATED,
        }
        return result, modifiedData

    def callPutQuery(self):
        # returnData = self.queryStatement(id)
        # if not returnData:
        #     abort(404, message="user doesn't exist, cannot update")
        # if args['first_name']:
        #     returnData.first_name = args['first_name']
        # if args['last_name']:
        #     returnData.last_name = args['last_name']
        # session.commit()
        result = {
            'status_code': 200,
            'message' : APIconstants.UPDATED,
        }
        return result

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

    def queryStatement(self,id=None, whereCol=None, ids=None):
        #Will only get by id (Works for get/delete only)
        # For post, it is handled by child component
        if(id):
            stmt = select(self.model).where(self.model.id.in_([id]))
            data = session.scalars(stmt).first()
            return data
        #Will return list of models
        if(ids):
            data = []
            for id in ids :
                data_element = session.query(self.model).get(id)
                if data_element == None:
                    continue
                data.append(data_element)              
            return data
        #Query based on col criteria
        if(whereCol):
            #The query is outside of the loop is because the filter function
            #will chain the criteria fields. So the the session query is called 
            #only once.
            query = session.query(self.model)
            for attr, value  in whereCol.items():
                if value==None:
                    continue
                query = query.filter(getattr(self.model, attr).like("%%%s%%" % value))
            return query
        #Will query all data
        else:
            # #users = (self.model).query.all()
            # stmt = select(self.model)
            # for row in session.execute(stmt):
            #     print("session.execute")
            #     print(row.first_name)
            #     print(type(row))
            # return session.execute(stmt).all()
            # TODO: #27 Implement order by updated_date
            data = session.query(self.model).order_by(self.model.updated_date.desc())
            # for instance in data :
            #     print("Kiki Lala")
            #     print(instance.user_id, instance.fav_sub)
            return data