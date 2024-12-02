from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Fruit model
class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    fruits = Fruit.query.all()
    return render_template('index.html', fruits=fruits)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/fruits', methods=['GET'])
@login_required
def get_fruits():
    fruits = Fruit.query.all()
    return jsonify([{'id': fruit.id, 'name': fruit.name} for fruit in fruits])

@app.route('/fruits', methods=['POST'])
@login_required
def add_fruit():
    new_fruit = request.form
    fruit_name = new_fruit['name']
    fruit = Fruit(name=fruit_name)
    db.session.add(fruit)
    db.session.commit()
    return jsonify({"id": fruit.id, "name": fruit.name}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables
        try:
            user = User(username='admin', password=generate_password_hash('password'))
            db.session.add(user)
            db.session.commit()
        except:
            pass 
    app.run(debug=True)