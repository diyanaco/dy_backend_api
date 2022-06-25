from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
engine = create_engine('sqlite:///diyanaco.db', echo=True)
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
#Only run once to create tables

from model.sys.dy_shared_user import User

Base.metadata.create_all(engine)

user1 = User(id = 123, first_name ="Zaim", last_name = "Saha")
session.add(user1)
session.commit()