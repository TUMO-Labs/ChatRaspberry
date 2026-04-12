from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    content  = db.Column(db.String(500), nullable=False) 
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def chat():
    if request.method == 'POST': 
        username = request.form['username']
        content  = request.form['content']

        new_message = Message(username=username, content=content)

        try: 
            db.session.add(new_message)
            db.session.commit()
            
        except:
            db.session.rollback()
            return "There was an issue adding your message. Maybe try again?"
            
    messages = Message.query.order_by(Message.timestamp.desc()).all() # SELECT * FROM message ORDER BY timestamp DESC;
    return render_template('index.html', chat_history=messages)

if __name__ == '__main__':
    app.run(debug=True)