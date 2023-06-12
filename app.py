from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATABASE_FOLDER = 'database'
META_FILE = 'metadata.json'

def initialize_database():
    if not os.path.exists(DATABASE_FOLDER):
        os.makedirs(DATABASE_FOLDER)
    if not os.path.exists(META_FILE):
        with open(META_FILE, 'w') as f:
            json.dump([], f)

def create_table(table_name, columns):
    table_path = os.path.join(DATABASE_FOLDER, f"{table_name}.json")
    if os.path.exists(table_path):
        return f"Table '{table_name}' already exists."
    with open(META_FILE, 'r') as f:
        metadata = json.load(f)
    metadata.append({'table_name': table_name, 'columns': columns})
    with open(META_FILE, 'w') as f:
        json.dump(metadata, f)
    return f"Table '{table_name}' created successfully."

def insert_into_table(table_name, values):
    table_path = os.path.join(DATABASE_FOLDER, f"{table_name}.json")
    if not os.path.exists(table_path):
        return f"Table '{table_name}' does not exist."
    with open(table_path, 'a') as f:
        json.dump(values, f)
        f.write('\n')
    return f"Inserted into table '{table_name}' successfully."

@app.route('/create_table', methods=['POST'])
def create_table_route():
    data = request.get_json()
    table_name = data['table_name']
    columns = data['columns']
    response = create_table(table_name, columns)
    return jsonify({'message': response})

@app.route('/insert_into_table', methods=['POST'])
def insert_into_table_route():
    data = request.get_json()
    table_name = data['table_name']
    values = data['values']
    response = insert_into_table(table_name, values)
    return jsonify({'message': response})

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
