from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SECRET_KEY'] = 'admin' 
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    content  = db.Column(db.String(500), nullable=False) 
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
            return f"Error: {str(e)}"
            
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

@app.route('/', methods=['POST', 'GET'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST': 
        if request.form.get('action') == 'delete':
            msg_id = request.form.get('delete_id') # msg_id = 3
            msg = Message.query.get(msg_id)  # SELECT * FROM message WHERE id = X;
            if msg:
                try:
                    db.session.delete(msg)
                    db.session.commit()
                    return redirect(url_for('chat'))
                except:
                    db.session.rollback()
                    return "There was an issue deleting the message. Maybe try again?"
        else:          
            content = request.form['content']
            new_message = Message(username=session['username'], content=content)
            try: 
                db.session.add(new_message)
                db.session.commit()
                return redirect(url_for('chat'))
            except:
                db.session.rollback()
                return "Issue sending message."

    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', chat_history=messages, current_user=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
