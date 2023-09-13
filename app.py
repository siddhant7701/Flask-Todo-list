from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, secret key

# Initialize an empty dictionary to store user information
users = {}

# Initialize an empty dictionary to store user tasks (username: tasks)
user_tasks = {}

# Define functions for different operations

# Modify the 'view_tasks' function to display only the user's tasks
def view_tasks():
    # Ensure the user is authenticated
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieve the username from the session
    username = session['username']

    # Display only the tasks associated with the user
    user_tasks_list = user_tasks.get(username, [])

    return render_template('index.html', tasks=user_tasks_list, username=username)

@app.route('/')
def index():
    # Check if the user is authenticated
    if 'username' in session:
        username = session['username']
        user_tasks_list = user_tasks.get(username, [])
        return render_template('index.html', tasks=user_tasks_list, username=username)
    else:
        return redirect(url_for('login'))

@app.route('/add_task', methods=['POST'])
def add_task():
    # Ensure the user is authenticated
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieve the username from the session
    username = session['username']

    task_name = request.form.get('task_name')
    task_description = request.form.get('task_description')

    task = {"name": task_name, "description": task_description, "completed": False}

    # Check if the user already has tasks
    if username not in user_tasks:
        user_tasks[username] = []

    user_tasks[username].append(task)

    return redirect(url_for('index'))

@app.route('/mark_completed', methods=['POST'])
def mark_completed():
    # Ensure the user is authenticated
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieve the username from the session
    username = session['username']

    task_name = request.form.get('task_name')

    for task in user_tasks.get(username, []):
        if task["name"] == task_name:
            task["completed"] = True

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the provided credentials are valid
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            # Register the new user
            users[username] = password
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('register.html', error="Username already exists. Please choose another.")

    return render_template('register.html')

@app.route('/logout')
def logout():
    # Clear the session and log the user out
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
