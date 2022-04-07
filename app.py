from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/testing'

db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     location = db.Column(db.String(50))
#     date_created = db.Column(db.DateTime, default=datetime.datetime.now())

user = db.Table('User',db.metadata, autoload = True, autoload_with=db.engine)

@app.route('/')
def index():
    results = db.session.query(user).all()
    for r in results:
        print(r.Name)

    return ''

