from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:porat2410@localhost/Namba'

db=SQLAlchemy(app)

class Student(db.Model):
    __tablename__='users'
    user_ID=db.Column(db.String(40),primary_key=True)
    name=db.Column(db.String(40))
    def __init__(self,username, name):
        self.user_ID=username
        self.name = name

class Poll_ID(db.Model):
    __tablename__='poll_id'
    poll_ID=db.Column(db.Integer,primary_key=True)

    def __init__(self):
        self.poll_ID = 0


class Admins(db.Model):
    __tablename__='admins'
    Username=db.Column(db.String(40),primary_key=True)
    Password=db.Column(db.String(40))
    def __init__(self,username, password):
        self.Username = username
        self.Password = password


class Polls(db.Model):
    __tablename__='polls'
    poll_ID=db.Column(db.String(40),primary_key=True)
    question=db.Column(db.String(255))
    answers = db.Column(db.ARRAY(db.String(100)))
    answers_counter = db.Column(db.ARRAY(db.Integer))
    closed = db.Column(db.BOOLEAN)
    multiple_choice = db.Column(db.BOOLEAN)
    quiz = db.Column(db.BOOLEAN)
    correct_answers = db.Column(db.ARRAY(db.Integer))
    solution=db.Column(db.String(255))

    def __init__(self,poll_ID, question, answers, answers_counter, closed, multiple_choice,
                 quiz, correct_answers, solution):
        self.poll_ID = poll_ID
        self.question = question
        self.answers = answers
        self.answers_counter = answers_counter
        self.closed = closed
        self.multiple_choice = multiple_choice
        self.quiz = quiz
        self.correct_answers = correct_answers
        self.solution = solution

class Polls_answers(db.Model):
    __tablename__='polls_answers'
    poll_ID=db.Column(db.String(40), ForeignKey(Polls.poll_ID) ,primary_key=True)
    user_ID=db.Column(db.String(40), ForeignKey(Student.user_ID) ,primary_key=True)
    answers = db.Column(db.ARRAY(db.String(100)))
    is_correct = db.Column(db.BOOLEAN)

    def __init__(self,poll_ID, user_ID, answers, is_correct):
        self.poll_ID = poll_ID
        self.user_ID = user_ID
        self.answers = answers
        self.is_correct = is_correct


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/init_pollID', methods=['POST'])
def init_pollID():

    try:
        poll_id=Poll_ID()
        db.session.add(poll_id)
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e


@app.route('/submit', methods=['POST'])
def submit(id, name):

    try:
        student=Student(id, name)
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e

@app.route('/delete', methods=['POST'])
def delete(id):
    try:
        Student.query.filter_by(user_ID=id).delete()
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e


@app.route('/add_admin', methods=['POST'])
def add_admin(username, password):

    try:
        admin = Admins(username, password)
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e


@app.route('/delete_admin', methods=['POST'])
def delete_admin(username):
    try:
        Admins.query.filter_by(Username=username).delete()
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e

@app.route('/add_poll', methods=['GET', 'POST'])
def add_poll(question, answers, answers_counter, closed, multiple_choice,
             quiz, correct_answers, solution):
    Result=db.session.query(Poll_ID).all()
    poll_id = Result[0].poll_ID

    try:
        poll = Polls(poll_id, question, answers, answers_counter, closed, multiple_choice,
                     quiz, correct_answers, solution)
        db.session.add(poll)
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e

    Result[0].poll_ID += 1
    db.session.commit()

@app.route('/delete_poll', methods=['POST'])
def delete_poll(poll_id):
    try:
        Polls.query.filter_by(poll_ID=poll_id).delete()
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e



if __name__ == '__main__':  #python interpreter assigns "__main__" to the file you run
    app.run(debug=True)