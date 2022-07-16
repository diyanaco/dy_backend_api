import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)
SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
print(SECRET_KEY)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_SECRET_KEY'] = 'thisissoawesometrustme'
CORS(app)
jwt = JWTManager(app)

##May be useful in the future
# db_url = 'localhost:5432'
# db_name = 'online-exam'
# db_user = 'postgres'
# db_password = '0NLIN3-ex4m'
# engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')

engine = create_engine('sqlite:///diyanaco.db', echo=True, connect_args={'check_same_thread': False})
Base = declarative_base()

#another test

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

#test hello world commit all

from model.sys.dy_shared_user import UserModel
from backend.controller.UserController import UserController
from backend.controller.UserAuthController import AuthLoginController, AuthSignupController

#Only run once to create tables
#Base.metadata.create_all(engine)

#To insert new user
# user1 = UserModel(id = 123, first_name ="Zaim", last_name = "Saha")
# session.add(user1)
# session.commit()
# from .views import views
# from .auth import auth

# app.register_blueprint(views, url_prefix='/')
# app.register_blueprint(auth, url_prefix='/')

@app.before_first_request
def create_tables():
    Base.metadata.create_all(engine)

@app.route("/")
def hello_diyana():
    return "<p>This is diyanaco API!</p>"