# setup the flask app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

# instantiate the SQLAlchemy object to control all things from the connected db
# this object can be imported out this module to perform operation on the connected db
db = SQLAlchemy()
DB_NAME = "database.db" # this is the db file name to be created 

# customization your app setting
def create_app():
    app = Flask(__name__)
    # to secure your website session and cookies data, its value can be any string at least one char
    app.config['SECRET_KEY'] = 's1a1k1r1a1t1i1o1n'
    """ SQLite3
    can be integrated with Python using the built-in sqlite3 module which works as a SQL 
    interface, You don't need to install it as it is shipped by default along with Python 
    version 2.5.x onwards, but you have to import it to handle this built-in db """
    # define where your db is located and then integrate it with your app
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # import the blueprints objects from their modules and register it with their prefix url 
    from .views import views 
    from .auth import auth
    '''register your predefined blueprints, so that it will work as router that routes any
    request to the urlprefix to the API routes defined in the sepecified blueprint file'''
    app.register_blueprint(views, url_prefix='/') 
    app.register_blueprint(auth, url_prefix='/')
    # checks for the existance of DB 
    from .models import User, Note
    # if it doen't created before, it will be created, otherwise nothing will be executed
    createDB(app)
    
    # cutomization the loggin manager
    login_manager = LoginManager()
    # the flask will redirect you to this route if any route function required user login 
    # and the user is not login
    login_manager.login_view='auth.login' 
    login_manager.init_app(app) # tell the login manager that this is the used app
    
    # tell flask how you load a user
    # we load, reference, search for the user based on its PK
    @login_manager.user_loader
    def load_user(id):
        # get(id) similar to filter method except the get search only for user based on his PK
        return User.query.get(int(id)) 
    return app

def createDB(app):
    dbPath = 'website/'+DB_NAME   # this DB path supposed to be existed
    if not path.exists(dbPath):
        db.create_all(app=app)
        print('The DB is created successfully')
    else:
        print('db is existed at its path')


