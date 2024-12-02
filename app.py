from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
db = SQLAlchemy(app)

# Fruit model
class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

@app.route('/')
def index():
    fruits = Fruit.query.all()
    return render_template('index.html', fruits=fruits)

@app.route('/fruits', methods=['GET'])
def get_fruits():
    fruits = Fruit.query.all()
    return jsonify([{'id': fruit.id, 'name': fruit.name} for fruit in fruits])

@app.route('/fruits', methods=['POST'])
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
    app.run(debug=True)