from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SECRET_KEY'] = 'admin'
socketio = SocketIO(app, cors_allowed_origins='*')

KEY_FILE = os.path.join(os.path.dirname(__file__), 'secret.key')
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'rb') as f:
        fernet = Fernet(f.read())
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    fernet = Fernet(key)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    content  = db.Column(db.String(1000), nullable=False) 
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return "Username already exists. Please choose a different one."
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first() # SELECT * FROM user WHERE username = 'test' LIMIT 1;

        if user and check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('chat'))
        else:
            return "Invalid username or password"
            
    return render_template('login.html')

@app.route('/', methods=['GET'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    messages = Message.query.order_by(Message.timestamp.desc()).all()
    for msg in messages:
        msg.content = fernet.decrypt(msg.content.encode()).decode()
    return render_template('index.html', chat_history=messages, current_user=session['username'])

@socketio.on('send_message')
def handle_send_message(data):
    username = session['username']
    content = data['content']
    encrypted_content = fernet.encrypt(content.encode()).decode()
    new_message = Message(username=username, content=encrypted_content)
    db.session.add(new_message)
    db.session.commit()
    
    emit('new_message', {
        'username': username,
        'message': content,
        'timestamp': new_message.timestamp.strftime('%H:%M')
    }, broadcast=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
   socketio.run(app, port=5000)
