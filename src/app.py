from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# from openai import OpenAI
# import os
import sqlite3

# class Status(enum.Enum):
#     HTTP_200_OK = 200
#     HTTP_201_CREATED = 201
# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sha256'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# def init_db():
#     conn = sqlite3.connect('knowledge_base.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS knowledge (
#                     id INTEGER PRIMARY KEY,
#                     question TEXT NOT NULL,
#                     answer TEXT NOT NULL
#                  )''')
#     conn.commit()
#     conn.close()

# @app.before_request
# def initialize():
#     init_db()

######################################################################
# H E A L T H   C H E C K
######################################################################
@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="OK"), 200

######################################################################
# H O M E   P A G E
######################################################################
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2')

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You are not logged in!', 'danger')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

######################################################################
# C R E A T E   A   N E W   P R O D U C T
######################################################################
# @app.route("/generate", methods=["POST"])
# def generate_text():
#     """
#     Creates a Product
#     This endpoint will create a Product based the data in the body that is posted
#     """
#
#     data = request.get_json()
#
#     if 'prompt' not in data:
#         return jsonify({'error': 'No prompt provided'}), 400
#
#     prompt = data['prompt']
#     print(data)
#     try:
#         print("Before respnse")
#         response = client.completions.create(model="gpt-3.5-turbo", #text-davinci-004",  # or another model like "gpt-4"
#         prompt=prompt,
#         max_tokens=150)
#         print(response.dict)
#
#         return jsonify({
#             'prompt': prompt,
#             'response': response.choices[0].text.strip()
#         })
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#


# @app.route("/generate/<prompt>", methods=["GET"])
# def generate_text_get(prompt):
#     """
#     Creates a Product
#     This endpoint will create a Product based the data in the body that is posted
#     """
#
#     try:
#         response = client.chat.completions.create(model="gpt-3.5-turbo", #text-davinci-004",  # or another model like "gpt-4"
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=150)
#         print(response.dict)
#
#         return jsonify({
#             'prompt': prompt,
#             'response': response.choices[0].text.strip()
#         })
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
