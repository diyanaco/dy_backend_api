from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

engine = create_engine('sqlite:///diyanaco.db', echo=True, connect_args={'check_same_thread': False})
Base = declarative_base()

#another test

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

#test hello world commit all

from model.sys.dy_shared_user import UserModel
from backend.controller.UserController import UserController

#Only run once to create tables
#Base.metadata.create_all(engine)

#To insert new user
# user1 = UserModel(id = 123, first_name ="Zaim", last_name = "Saha")
# session.add(user1)
# session.commit()

@app.route("/")
def hello_diyana():
    return "<p>This is diyanaco API!</p>"