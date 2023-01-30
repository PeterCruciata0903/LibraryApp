import os
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder="")
bcrypt = Bcrypt(app)
global current_username

'''
SQLALCHEMY_DATABASE_URI: The database URI to specify the database you want to establish a connection with.
In this case, the URI follows the format sqlite:///path/to/database.db.

You use the os.path.join() function to intelligently join the base directory you constructed and stored in the basedir variable, and the database.db file name.
This will connect to a database.db database file in your flask_app directory. The file will be created once you initiate the database.
SQLALCHEMY_TRACK_MODIFICATIONS: A configuration to enable or disable tracking modifications of objects. You set it to False to disable tracking and use less memory. For more, see the configuration page in the Flask-SQLAlchemy documentation.
'''
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def signin_post():
    return render_template('index.html')


# This post is called by the login.html once a user submits their login
@app.route('/lib', methods=['GET', 'POST'])
def lib_post():
    # When our login form is submitted, save the login info, save to our database, and then send user to the index.html file
    if request.method == "POST":
        global current_username
        _username = request.form.get("username")
        _password = request.form.get("password")
        current_username = _username

        # check if the login exists, if not, create a new user
        user = User.query.filter_by(username=_username).first()
        if not user:
            return render_template('signup.html')
        else:
            #Compare hashed password to input
            if bcrypt.check_password_hash(user.password, _password):
                # send the user to the library index.html page
                return render_template('lib.html')
            else:
                return render_template('index.html')



# This post is called by the inventory page to get back to lib.html


@app.route('/search')
def search_post():
    return render_template('lib.html')

@app.route('/reg')
def reg_post():
    return render_template('signup.html')



# This post swaps to the inventory page in the navbar
@app.route('/inventory')
def inv_post():
    books = ReserveBook.query
    return render_template('inventory.html', books=books)

# This post swaps to the sign in page if you do not already have an account


@app.route('/signup', methods=['GET', 'POST'])
def signup_post():
    if request.method == "POST":
        global current_username
        _username = request.form.get("username")
        #Save password after hashing to encrypt
        _password = bcrypt.generate_password_hash(request.form.get("password"))
        current_username = _username
        
        new_user = User(username=_username, password=_password, book="")
        db.session.add(new_user)
        db.session.commit()

        return render_template('lib.html')


@app.route('/reserved', methods=['GET', 'POST'])
def reservebook_post():
    if request.method == "POST":
        _title = request.form.get("title")
        if ReserveBook.query.filter_by(bookTitle=_title).first().booksAvailable == 1:
            global current_username
            cur_user = User.query.filter_by(username=current_username).first()
            cur_user.book = _title
            db.session.commit()

            cur_book = ReserveBook.query.filter_by(bookTitle=_title).first()
            cur_book.booksAvailable = 0
            db.session.commit()

            books = ReserveBook.query
            return render_template('inventory.html', books=books)
        else:
            books = ReserveBook.query
            return render_template('inventory.html', books=books)


@app.route('/returned', methods=['GET', 'POST'])
def returnbook_post():
    if request.method == "POST":
        global current_username
        cur_user = User.query.filter_by(username=current_username).first()
        _title = request.form.get("title")
        cur_user.book = ""
        db.session.commit()

        cur_book = ReserveBook.query.filter_by(bookTitle=_title).first()
        cur_book.booksAvailable = 1
        db.session.commit()

        books = ReserveBook.query
        return render_template('inventory.html', books=books)


# This post dynamically prints the current user's info to userinfo.html
@app.route('/info')
def info_post():
    global current_username
    cur_user = User.query.filter_by(username=current_username).first()
    return render_template('userinfo.html', cur_user=cur_user)

@app.route('/quote')
def quote_post():
    global current_username
    cur_user = User.query.filter_by(username=current_username).first()
    return render_template('quote.html', cur_user=cur_user)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000, threaded=True)


# The User table for our database
class User(db.Model):
    username = db.Column(db.String(100), nullable=False, primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    book = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


# The User table for our database


class ReserveBook(db.Model):
    ISBN = db.Column(db.String(255), primary_key=True)
    bookTitle = db.Column(db.String(255), nullable=False)
    bookAuthor = db.Column(db.String(255), nullable=False)
    booksAvailable = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    releaseDate = db.Column(db.String(255))

    def __repr__(self):
        return f'<ReserveBook {self.bookTitle}>'
