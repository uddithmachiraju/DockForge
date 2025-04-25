import os 
from flask import Flask, render_template, request, redirect, session
import psycopg2
from uuid import uuid4

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = os.environ.get('SECRET_KEY', str(uuid4()))

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname='dockforge',
        user='postgres',
        password='Raju@2003',
        host='localhost',
        port='5432'
    )

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE user_uid = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user_id
            session['email'] = user[0]

            # Update last login
            cursor.execute("UPDATE progress SET last_login = NOW() WHERE user_uid = %s", (user_id,))
            conn.commit()

            cursor.close()
            conn.close()
            return redirect('/')
        else:
            return "Invalid ID. Please sign up first."
    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        user_id = str(uuid4())[:8]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Email already registered. Please log in."

        # Insert into users table
        cursor.execute("INSERT INTO users (email, user_uid) VALUES (%s, %s)", (email, user_id))

        # Insert into progress table
        cursor.execute("INSERT INTO progress (user_uid) VALUES (%s)", (user_id,))

        conn.commit()
        cursor.close()
        conn.close()

        session['user_id'] = user_id
        session['email'] = email

        return f"Your unique ID is: {user_id}. Please save it for login."

    return render_template('signup.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
