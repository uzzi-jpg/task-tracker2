# Databricks notebook source
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'tasks.json'

# Load tasks from file
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'todo': [], 'progress': [], 'done': []}

# Save tasks to file
def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f)

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(load_tasks())

# Save all tasks
@app.route('/tasks', methods=['POST'])
def save_all_tasks():
    tasks = request.json
    save_tasks(tasks)
    return jsonify({'status': 'saved'})

# Add a task
@app.route('/tasks/<column>', methods=['POST'])
def add_task(column):
    tasks = load_tasks()
    new_task = request.json
    tasks[column].append(new_task)
    save_tasks(tasks)
    return jsonify({'status': 'added'})

# Delete a task
@app.route('/tasks/<column>/<int:task_id>', methods=['DELETE'])
def delete_task(column, task_id):
    tasks = load_tasks()
    tasks[column] = [t for t in tasks[column] if t['id'] != task_id]
    save_tasks(tasks)
    return jsonify({'status': 'deleted'})

if __name__ == '__main__':
    print('Server running on http://localhost:5000')
    app.run(debug=True, port=5000)