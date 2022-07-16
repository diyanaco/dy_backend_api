from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from model.sys.dy_shared_user import UserModel
from sqlalchemy.orm import sessionmaker
from backend import engine
from sqlalchemy import select

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "error": "Unauthorized"
            }, 401
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            stmt = select(UserModel).where(UserModel.id._in([data["user_id"]]))
            current_user = session.scalars(stmt).first()
            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "error": "Unauthorized"
                }, 401

        except Exception as e:
            return {
                "message": "Something went wrong",
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated
