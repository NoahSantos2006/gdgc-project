from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'

# tell Flask where the SQLite database file is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class User(db.Model):

    # gives an index for each row in the db table
    id = db.Column(db.Integer, primary_key=True)

    # store a column named "email" with max 120 strings in each row
    # unique makes it so there aren't two rows with the same email
    # nullable makes it so that the email can't be NULL
    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)


    def set_password(self, password):

        # can't store the actual password so we store a hash instead
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        # checks the actual password and returns True if password is the same
        return check_password_hash(self.password_hash, password)
    
@app.route('/')
def home():
    return "Home page is working! Go to /create_test_user to make a user."

@app.route('/create_test_user')
def create_test_user():
    # change these to what you want
    email = "test@example.com"
    password = "12345"

    # check if user already exists
    existing = User.query.filter_by(email=email).first()
    if existing:
        return "User already exists!"

    # makes a class for "user"
    user = User(email=email)
    user.set_password(password)  # hashes the password

    # adds user to the database
    db.session.add(user)

    db.session.commit()
    return "Test user created!"

@app.route('/login', methods=['GET', 'POST'])
def login_page():

    if request.method == 'GET':

        return render_template('login.html')
    
    email = request.form.get('email')
    password = request.form.get('password')

    return f"You submitted: {email}, {password}"

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'GET':
        return render_template('signup.html')

    email = request.form.get('email')
    password = request.form.get('password')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return render_template('signup.html', error="email already in use")

    new_user = User(email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login_page'))


if __name__ == '__main__':

    with app.app_context():

        db.create_all()  # this creates database.db and the tables

    app.run(debug=True)

