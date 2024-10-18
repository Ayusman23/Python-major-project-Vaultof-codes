from flask import Flask, render_template, request, redirect, jsonify
import json

app = Flask(__name__)

class Task:
    def __init__(self, title, description, category):
        self.title = title
        self.description = description
        self.category = category
        self.completed = False

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return [Task(**data) for data in json.load(f)]
    except FileNotFoundError:
        return []

tasks = load_tasks()

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    category = request.form['category']
    tasks.append(Task(title, description, category))
    save_tasks(tasks)
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    tasks[task_id].completed = True
    save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks.pop(task_id)
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
