from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

# Sample data: a list of fruits
fruits = [
    {"id": 1, "name": "Apple"},
    {"id": 2, "name": "Banana"},
]

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html', fruits=fruits)

# Get the list of fruits
@app.route('/fruits', methods=['GET'])
def get_fruits():
    return jsonify(fruits)

# Add a new fruit
@app.route('/fruits', methods=['POST'])
def add_fruit():
    new_fruit = request.form
    fruit_name = new_fruit['name']
    fruit_id = len(fruits) + 1
    fruits.append({"id": fruit_id, "name": fruit_name})
    return jsonify({"id": fruit_id, "name": fruit_name}), 201

# Update an existing fruit
@app.route('/fruits/<int:fruit_id>', methods=['PUT'])
def update_fruit(fruit_id):
    fruit = next((fruit for fruit in fruits if fruit['id'] == fruit_id), None)
    if fruit is None:
        return jsonify({'error': 'Fruit not found'}), 404
    updated_data = request.form
    fruit.update(updated_data)
    return jsonify(fruit)

# Delete a fruit
@app.route('/fruits/<int:fruit_id>', methods=['DELETE'])
def delete_fruit(fruit_id):
    global fruits
    fruits = [fruit for fruit in fruits if fruit['id'] != fruit_id]
    return jsonify({'message': 'Fruit deleted'}), 204

if __name__ == '__main__':
    app.run(debug=True)
