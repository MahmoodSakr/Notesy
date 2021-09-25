from . import db  # == from website import db object
from sqlalchemy.sql import func  # this function return the current time
""" UserMixin provides default implementations for methods which Flask-Login expects to be
have by the user objects """
# flask-login module helps us log users, and user object needs to inherit from the UserMixin

from flask_login import UserMixin

# create a model to describe the schema for the User table
class User(db.Model, UserMixin):
    """ define schema/layout for the objects/rows to be stored in your db, tell what the 
    stored object will have like name, email, ... etc """
    # start with define the field/column(type,constrains)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    # to define an one to many relation between User&Note as each user can have many notes
    notes = db.relationship('Note') 
    # notes column store all notes related to each user as a list [] so you can loop over it 
    # to get each note as a note row from the Note table

# create a model to describe the schema for the Notes table
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text())
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # to attach the two tables (User,Note) based on the FK column
    # user in small char denote the table inside the sql db itself
    # User in capital char denote the model class
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


'''
Note how we never defined a __init__ constructor method on the User class? 
That’s because SQLAlchemy adds an implicit constructor to all model classes which 
accepts keyword arguments for all its columns and relationships.

If you decide to override that implicit constructor for any reason, make sure to keep 
to make it accepting **kwargs and call the super constructor with those **kwargs as following

class Table(db.Model):
    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        # do custom stuff

'''