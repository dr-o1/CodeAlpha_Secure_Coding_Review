from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    if task_name:
        conn = get_db_connection()
        conn.execute(f"INSERT INTO tasks (name) VALUES ('{task_name}')")  # Vulnerable to SQL injection
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<task_name>')
def delete_task(task_name):
    conn = get_db_connection()
    conn.execute(f"DELETE FROM tasks WHERE name = '{task_name}'")  # Vulnerable to SQL injection
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
