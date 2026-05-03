from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database and create the table
def init_db():
    conn = sqlite3.connect('event.db')
    conn.execute('CREATE TABLE IF NOT EXISTS guests (name TEXT, table_no INTEGER)')
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    table_no = request.form['table_no']

    with sqlite3.connect('event.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO guests (name, table_no) VALUES (?, ?)", (name, table_no))
        conn.commit()
    
    return f"<h2>Success!</h2><p>Thanks {name}! You are registered for Table {table_no}.</p><a href='/'>Back</a> | <a href='/results'>View All</a>"

@app.route('/results')
def results():
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, table_no FROM guests ORDER BY table_no ASC")
    data = cursor.fetchall()
    conn.close()
    return render_template('results.html', guests=data)

if __name__ == '__main__':
    init_db()
    # '0.0.0.0' makes the server visible to other devices on your Wi-Fi
    app.run(host='0.0.0.0', port=5000, debug=True)