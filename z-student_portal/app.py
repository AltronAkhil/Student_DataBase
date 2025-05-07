from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# DB setup
def init_db():
    conn = sqlite3.connect('student.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                    (id INTEGER PRIMARY KEY,
                     name TEXT,
                     email TEXT UNIQUE,
                     password TEXT)''')
    conn.close()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('student.db')
        try:
            conn.execute("INSERT INTO students (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "User already registered!"
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student_id = request.form['studentId']
        password = request.form['password']
        
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id=? AND password=?", (student_id, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['name'] = user[1]  # name
            session['email'] = user[2]  # email
            return redirect('/student')
        else:
            return "Invalid login!"
    return render_template('login.html')

@app.route('/student')
def student():
    if 'name' in session and 'email' in session and 'id' in session:
        return render_template('student.html',
                               name=session['name'],
                               email=session['email'],
                               student_id=session['id'])
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)