from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User  # to be used as representer of the user table
# to secure your password and not to store it as a plain text, we use the hash
# to convert the password palin text to something much more secure
# the hash function is one way function which it hasn't any inverse
# inverse function = if you have the output you can get the input and viceversa
# uninverse function = if you have the output you cannot get the input , so given x you got y, but given y you can't get x
# the hasing password can't be converted to plaintext
# you can chech if the input password is equal to the stored hash or not
# sha256 is well known hashing algorithm
# werkzeug is a tool in germany
from werkzeug.security import generate_password_hash, check_password_hash
# the following imported function get aided by the UserMixin as that is the reasons why 
# we make the User model class inherits from the UserMixin class
from flask_login import login_user, login_required, logout_user, current_user
'''
current_user >> hold information about the current logged user
login_user(userObj,remember='True') >> this keep the user be logined even you close the server  
or close the browser session, unless you don't cleared the history or delete the cookies or 
sessions, and be used after the loggin function assure of user credential or after the user 
is signed up.
logout_user() # will automatically log out the current user, no need for input user obj
@login_required >> decorator to the route function make it can't be executed unless the 
user be loggined first as it which couples with verify_password callback and provides True
if the username and password match.
current_user >> is an object of the werkzeug.local.LocalProxy class 
and it give you all information about the current user row as it represent the current
user object which denote the user row and it can access all the columns/fields of this user
by user.fieldName '''
# instantiate Blueprint obj
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # for the post requests for the /login route
        email = request.form['email']
        password = request.form.get('password')
        # make search for the user by the email column value
        user = User.query.filter_by(email=email).first()
        # if the user email is existed
        if user:
            # Checks for whether the password is correct or not by compare the stored hash pass
            # with the given password
            if check_password_hash(user.password, password):
                flash(f'Hello {user.first_name} in your profile',
                category="success")
                # to make the server save the user until you clear the session, cookies, 
                # otherwise, this user will be saved even you close the server
                login_user(user,remember=True) 
                # or return redirect(url_for('views.home'))
                return redirect('/')
            else:
                flash('Sorry your password is incorrect', category="error")
                # will request this route as get request
                return redirect(url_for('auth.login'))
        else:
            flash('This user is not existed, please sign up first !',category="error")
            return redirect('/sign-up')
    else:
        # for the get requests for the the /login route
        # let the page know who is the current user
        return render_template('login.html',user=current_user)


@auth.route('/logout', methods=['GET'])
@login_required # decorator enfore the foute function to be called after the user is logined
def logout():
    logout_user() # will automatically log out the current user
    return redirect('/login') #return redirect(url_for('auth.login'))
    
@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['firstName']
        password1 = request.form['password1']
        password2 = request.form.get('password2')
        # flash messages be triggered to the rendered template so from the template you can
        # control where to display it
        user = User.query.filter_by(email=email).first()
        # checks for the existance of the user before store the received user data into db
        if user:
            flash('This user is already existed before', category='error')
        # do the validation operations on the received form values before storing into db
        elif (len(email) < 4):
            flash('your email must be greter than 3 char', category='error')
        elif (len(first_name) < 2):
            flash('your email must be greter than 3 char', category='error')
        elif password1 != password2:
            flash('Passwords must be matched!', category='error')
        elif (len(password1) < 7):
            flash('Your password is less than 7 characters', category='error')
        else:
            # create a new user row in the db with a hashed password
            hashed_pass = generate_password_hash(password1, method='sha256')
            new_user = User(email=email, first_name=first_name,
                            password=hashed_pass)
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash('Your account has been created', category='success')
            # to redirect, select the route url
            # or
            # select blueprint file name and its route function inside it
            # return redirect(url_for('views.home'))
            return redirect('/')
    # this template will receive the flashed messages
    return render_template('signUp.html',user=current_user)