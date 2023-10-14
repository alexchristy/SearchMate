from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data to act as a database
tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'done': False
    },
    {
        'id': 2,
        'title': 'Go to the gym',
        'done': True
    }
]

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        return jsonify({'tasks': tasks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = next((item for item in tasks if item['id'] == task_id), None)
        if task is None:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({'task': task}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        new_task = request.json
        new_task['id'] = max(task['id'] for task in tasks) + 1 if tasks else 1
        tasks.append(new_task)
        return jsonify({'task': new_task}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update an existing task by ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = next((item for item in tasks if item['id'] == task_id), None)
        if task is None:
            return jsonify({'error': 'Task not found'}), 404
        task.update(request.json)
        return jsonify({'task': task}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = next((item for item in tasks if item['id'] == task_id), None)
        if task is None:
            return jsonify({'error': 'Task not found'}), 404
        tasks.remove(task)
        return jsonify({'message': 'Task deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)