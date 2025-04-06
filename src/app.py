from flask import Flask, render_template, request, redirect, session
from uuid import uuid4 

app = Flask(__name__, template_folder = "../templates", static_folder="../static")

@app.route("/")
def home():
    return render_template("index.html") 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user_id = str(uuid4())  # In real case, you'd look it up or create
        session['user_id'] = user_id
        session['email'] = email
        return redirect('/')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        user_id = str(uuid4())
        session['user_id'] = user_id
        session['email'] = email
        return redirect('/')
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(
        port = 5000, 
        debug = True 
    )