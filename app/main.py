from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory storage for todos
todos = []
todo_id_counter = 1

# HTML template
template = """
<!DOCTYPE html>
<html>
<head>
    <title>To-Do List App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
        }
        .add-form {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            padding: 12px 24px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
        }
        button:hover {
            background: #5568d3;
        }
        .todo-list {
            list-style: none;
        }
        .todo-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: transform 0.2s;
        }
        .todo-item:hover {
            transform: translateX(5px);
        }
        .todo-item.completed {
            opacity: 0.6;
        }
        .todo-item.completed .todo-text {
            text-decoration: line-through;
            color: #888;
        }
        .todo-text {
            flex: 1;
            color: #333;
        }
        .todo-actions {
            display: flex;
            gap: 10px;
        }
        .btn-small {
            padding: 6px 12px;
            font-size: 14px;
            border-radius: 6px;
        }
        .btn-complete {
            background: #28a745;
        }
        .btn-complete:hover {
            background: #218838;
        }
        .btn-delete {
            background: #dc3545;
        }
        .btn-delete:hover {
            background: #c82333;
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #888;
        }
        .stats {
            text-align: center;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 My To-Do List</h1>
        
        <form method="POST" action="/add" class="add-form">
            <input type="text" name="task" placeholder="Add a new task..." required>
            <button type="submit">Add Task</button>
        </form>
        
        {% if todos %}
            <ul class="todo-list">
                {% for todo in todos %}
                <li class="todo-item {% if todo.completed %}completed{% endif %}">
                    <span class="todo-text">{{ todo.task }}</span>
                    <div class="todo-actions">
                        {% if not todo.completed %}
                        <form method="POST" action="/complete/{{ todo.id }}" style="display: inline;">
                            <button type="submit" class="btn-small btn-complete">✓ Done</button>
                        </form>
                        {% endif %}
                        <form method="POST" action="/delete/{{ todo.id }}" style="display: inline;">
                            <button type="submit" class="btn-small btn-delete">✕ Delete</button>
                        </form>
                    </div>
                </li>
                {% endfor %}
            </ul>
            
            <div class="stats">
                Total Tasks: {{ total }} | Completed: {{ completed }} | Pending: {{ pending }}
            </div>
        {% else %}
            <div class="empty-state">
                <p>No tasks yet. Add one above to get started! 🚀</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    total = len(todos)
    completed = sum(1 for todo in todos if todo['completed'])
    pending = total - completed
    
    return render_template_string(
        template, 
        todos=todos, 
        total=total, 
        completed=completed, 
        pending=pending
    )

@app.route('/add', methods=['POST'])
def add_todo():
    global todo_id_counter
    task = request.form.get('task')
    
    if task:
        todos.append({
            'id': todo_id_counter,
            'task': task,
            'completed': False,
            'created_at': datetime.now()
        })
        todo_id_counter += 1
    
    return redirect(url_for('home'))

@app.route('/complete/<int:todo_id>', methods=['POST'])
def complete_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = True
            break
    
    return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

