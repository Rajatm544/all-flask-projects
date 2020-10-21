from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin, login_required, UserManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['CSRF_ENABLED'] = False
app.config['USER_ENABLE_EMAIL'] = True
app.config['USER_ENABLE_CONFIRM_EMAIL'] = True
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    @property
    def email_confirmed_at(self):
        return self.confirmed_at

    @email_confirmed_at.setter
    def email_confirmed_at(self, value):
        self.confirmed_at = value


user_manager = UserManager(app, db, User)

@app.route('/')
def index():
    return '<h1>This is the home page!</h1>'

@app.route('/profile')
@login_required
def profile():
    return '<h1>This is the profile page</h1>'

if __name__ == '__main__':
    app.run(debug=True)