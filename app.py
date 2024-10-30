import sqlite3
import os

from flask import Flask, render_template, request, flash, url_for, abort, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import re

from DataBase import DataBase

# Define constants for database path, debug mode, and secret key
DATABASE = '/tmp/flsk.db'
DEBUG = True
SECRET_KEY = 'Your secret key'

# Create a Flask application instance
app = Flask(__name__)
app.config.from_object(__name__)

# Update the database configuration to use a file in the application directory
app.config.update({'DATABASE': os.path.join(app.root_path, 'flsk.db')})


# Function to connect to the SQLite database
def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row  # Use Row factory to access columns by name
    return con


# Function to create the database and initialize it with schema from a SQL file
def create_db():
    db = connect_db()
    with open('create_db.sql', 'r') as f:
        db.cursor().executescript(f.read())  # Execute SQL script to create tables
    db.commit()  # Commit the changes
    db.close()  # Close the connection


# Route for the index page
@app.route('/index')
@app.route('/')
def index():
    db_con = connect_db()
    dbase = DataBase(db_con)

    # Render the index page with posts fetched from the database
    return render_template('index.html', posts=dbase.get_objects('posts'))


# Route for creating a new post
@app.route('/create', methods=['GET', 'POST'])
def create():
    db_con = connect_db()
    dbase = DataBase(db_con)

    if request.method == 'POST':
        # Validate the form data
        if len(request.form['title']) < 3 or len(request.form['text']) < 10:
            flash('Error adding article', category='error')  # Show error message
        else:
            res = dbase.add_post(request.form['title'], request.form['text'])

            if res:
                flash('Article successfully added', category='success')
            else:
                flash('Error adding article', category='error')

    # Render the post creation form
    return render_template('create.html')


# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')  # Render the about page


# Route for displaying a specific post by its ID
@app.route("/post/<int:post_id>")
def show_post(post_id):
    db_con = connect_db()
    dbase = DataBase(db_con)

    post = dbase.get_post(post_id)  # Fetch the post from the database

    return render_template('post.html', post=post)  # Render the post detail page


# Function to validate user profile access.
# This function checks if the user is logged in and if the logged-in user matches the provided username.
# If the user is not authorized, it aborts the request with a 401 Unauthorized error.
# Currently, this function is not used in the project, but it can be utilized for extending the application
# to secure user profile routes in the future.
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)  # Abort if the user is not authorized
#     return f'User {username}'  # Return the username


# Route for user sign-up
@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if 'userLogged' in session:
        flash('You are already registered', 'error')
        return redirect(url_for('index'))  # Redirect if user is already logged in

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate input fields
        if not email or not password or not confirm_password:
            flash('All fields must be filled', 'error')
            return redirect(url_for('sign_up'))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('sign_up'))

        # Check password complexity
        if len(password) < 5:
            flash('Password must be at least 5 characters long', 'error')
            return redirect(url_for('sign_up'))
        if not re.search(r'\d', password):
            flash('Password must contain at least one digit', 'error')
            return redirect(url_for('sign_up'))
        if not re.search(r'[^\w\s]', password):
            flash('Password must contain at least one special character', 'error')
            return redirect(url_for('sign_up'))

        db_con = connect_db()
        dbase = DataBase(db_con)

        if dbase.get_user_by_email(email):
            flash('User with this email already exists', 'error')
            return redirect(url_for('sign_up'))

        # Hash the password before saving
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        if dbase.add_user(email, hashed_password):
            # Set session for the user after successful registration
            session['userLogged'] = email
            flash('Registration successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Error during registration', 'error')

    # Render the sign-up form
    return render_template('sign-up.html')


# Route for user login
@app.route("/login", methods=['GET', 'POST'])
def login():
    # Redirect to index if the user is already logged in
    if 'userLogged' in session:
        flash('You are already logged in', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input fields
        if not email or not password:
            flash('All fields must be filled', 'error')
            return redirect(url_for('login'))

        db_con = connect_db()
        dbase = DataBase(db_con)
        user = dbase.get_user_by_email(email)

        # Verify user credentials
        if user and check_password_hash(user['password'], password):
            session['userLogged'] = user['email']  # Set session for the user
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')

    # Render the login form
    return render_template('login.html')


# Route for user logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('userLogged', None)  # Remove user from session
    flash('You have logged out successfully', 'success')
    return redirect(url_for('index'))


# Error handler for 404 (Not Found) errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404  # Render custom 404 error page


# Main entry point to create the database and run the Flask application
if __name__ == '__main__':
    create_db()  # Create the database on startup
    app.run()  # Start the Flask application
