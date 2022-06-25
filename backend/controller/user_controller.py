from unittest import result
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from model.sys.dy_shared_user import UserModel
from backend import session, engine, api
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("first_name", type=str, help="First name of the user is required", required=True)
user_post_args.add_argument("last_name", type=str, help="Last name of the user", required=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("first_name", type=str, help="First name of the user is required")
user_put_args.add_argument("last_name", type=str, help="Last name of the user")

resource_fields = {
    'id': fields.Integer,
    'first_name' : fields.String,
    'last_name' : fields.String
}

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class User(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        print(id)
        stmt = select(UserModel).where(UserModel.id.in_([id]))
        for user in session.scalars(stmt):
            result = user
        # result = session.query(UserModel).filter(UserModel.first_name.in_([first_name]))
        if not result:
            abort(404, message="Could not find user with that id")
        return result

    @marshal_with(resource_fields)
    def post(self, id):
        print(id)
        args = user_post_args.parse_args()
        stmt = select(UserModel).where(UserModel.id.in_([id]))
        for user in  session.scalars(stmt):
            if user:
                abort(409, message="user id taken...")
        user = UserModel(id=id, first_name=args["first_name"] , last_name=args['last_name'])
        session.add(user)
        session.commit()
        return user, 201

    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_put_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="user doesn't exist, cannot update")

        if args['first_name']:
            result.first_name = args['first_name']
        if args['last_name']:
            result.last_name = args['last_name']

        session.commit()
        return result


    def delete(self, user_id):
        return '', 204

#api.add_resource(User, "/user/<string:first_name>")
api.add_resource(User, "/user/<int:id>")
