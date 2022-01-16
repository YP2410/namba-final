from datetime import timedelta
from flask import Flask, render_template, request, send_from_directory, jsonify, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
# from flask_sessionstore import SqlAlchemySessionInterface
from sqlalchemy import ForeignKey
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy.exc
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects.postgresql import ARRAY
import backend.telegram_bot
from backend.config import ApplicationConfig
import pickle

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
CORS(app, supports_credentials=True)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:porat2410@localhost/Namba'
# app.config['SESSION_TYPE'] = 'memcached'
# app.config['SECRET_KEY'] = 'TheFlyingDutchman\n\xec]/'
server_session = Session(app)
# server_session.init_app(app)
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
server_session.app.session_interface.db.create_all()
# SqlAlchemySessionInterface(app, db, "sessions", "sess_")
# app.permanent_session_lifetime = timedelta(minutes=5)

class Student(db.Model):
    __tablename__ = 'users'
    user_ID = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(40))

    def __init__(self, username, name):
        self.user_ID = username
        self.name = name


class Poll_ID(db.Model):
    __tablename__ = 'poll_id'
    poll_ID = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        self.poll_ID = 0


class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        list.__setitem__(self, key, value)
        self.changed()

    def updateItem(self, key, value):
        self.__setitem__(key, value)


class Admins(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.String(40), primary_key=True)
    Password = db.Column(db.String(150))
    '''id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(40), nullable=False, unique=True)
    Password = db.Column(db.String(150), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')'''

    def __init__(self, username, password):
        self.id = username
        self.Password = password


class Polls(db.Model):
    __tablename__ = 'polls'
    poll_ID = db.Column(db.String(40), primary_key=True)
    question = db.Column(db.String(255))
    answers = db.Column(db.ARRAY(db.String(100)))
    answers_counter = db.Column(MutableList.as_mutable(ARRAY(db.Integer)))
    closed = db.Column(db.BOOLEAN)
    multiple_choice = db.Column(db.BOOLEAN)
    quiz = db.Column(db.BOOLEAN)
    correct_answers = db.Column(db.ARRAY(db.Integer))
    solution = db.Column(db.String(255))

    def __init__(self, poll_ID, question, answers, answers_counter, closed, multiple_choice,
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


class Mapping(db.Model):
    __tablename__ = 'mapping'
    poll_ID = db.Column(db.String(40), ForeignKey(Polls.poll_ID), primary_key=True)
    fake_ID = db.Column(db.String(40), primary_key=True)

    def __init__(self, poll_ID, fake_ID):
        self.poll_ID = poll_ID
        self.fake_ID = fake_ID


class Polls_answers(db.Model):
    __tablename__ = 'polls_answers'
    poll_ID = db.Column(db.String(40), ForeignKey(Polls.poll_ID), primary_key=True)
    user_ID = db.Column(db.String(150), ForeignKey(Student.user_ID), primary_key=True)
    answers = db.Column(db.ARRAY(db.String(100)))
    is_correct = db.Column(db.BOOLEAN)

    def __init__(self, poll_ID, user_ID, answers, is_correct):
        self.poll_ID = poll_ID
        self.user_ID = user_ID
        self.answers = answers
        self.is_correct = is_correct



'''class Session(db.Model):
        __tablename__ = "sessions"

        id = db.Column(db.Integer, primary_key=True)
        session_id = db.Column(db.String(255), unique=True)
        data = db.Column(db.LargeBinary)
        expiry = db.Column(db.DateTime)

        def __init__(self, session_id, data, expiry):
            self.session_id = session_id
            self.data = data
            self.expiry = expiry

        def __repr__(self):
            return '<Session data %s>' % self.data


sql_session_model = Session'''

'''@login_manager.user_loader
def load_user(username):
    return Admins.get(username)'''


@app.route('/')
def index():
    return render_template("index.html")
    # return send_from_directory(app.static_folder, 'build/index.html')
    # return 1234


@app.route('/mes', methods=['GET'])
def message():
    # print("got to flask")
    # return render_template("index.html")
    # return send_from_directory(app.static_folder, 'build/index.html')
    return {'message': '1234'}


'''
@app.route('/init_pollID', methods=['POST'])
def init_pollID():

    try:
        poll_id=Poll_ID()
        db.session.add(poll_id)
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e'''


@app.route('/submit', methods=['POST'])
def submit(id, name):
    try:
        student = Student(id, name)
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e


@app.route('/add_mapping', methods=['POST'])
def add_mapping(poll_ID, fake_ID):
    try:
        mapping = Mapping(poll_ID, fake_ID)
        db.session.add(mapping)
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


@app.route('/add_admin/<username>/<password>', methods=['POST'])
def add_admin(username, password):
    try:
        hashed_password = generate_password_hash(password)
        admin = Admins(username, hashed_password)
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        db.session.remove()
        # print("exception")
        if (type(e) is sqlalchemy.exc.IntegrityError):
            return {"result": "This username is already registered to the system."}
        return {"result": "Error occurred"}
    return {"result": True}


@app.route('/delete_admin', methods=['POST'])
def delete_admin(username):
    try:
        Admins.query.filter_by(id=username).delete()
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e


@app.route('/init_poll/<question>/<answers>/<multiple_choice>', methods=['GET', 'POST'])
def init_poll(chat_ID, question, answers, multiple_choice):
    try:
        answers = answers.split(',')
        answers = [a for a in answers if len(a) > 0]
        # in the future will need to send to the poll function a list of chat_id's
        backend.telegram_bot.poll(chat_ID, question, answers, multiple_choice)
    except Exception as e:
        raise e
    return {"result": True}


@app.route('/send_poll_to_all/<question>/<answers>/<multiple_choice>', methods=['GET', 'POST'])
def send_poll_to_all(question, answers, multiple_choice):
    try:
        answers = answers.split(',')
        answers = [a for a in answers if len(a) > 0]
        # in the future will need to send to the poll function a list of chat_id's
        Result = db.session.query(Student).all()
        if Result == []:
            print("empty")
            return {"result": "empty"}
        chat_ID = []
        for user in Result:
            chat_ID.append(user.user_ID)
        print(chat_ID)
        backend.telegram_bot.poll(chat_ID, question, answers, multiple_choice)
    except Exception as e:
        db.session.remove()
        raise e
    return {"result": True}


@app.route('/send_to_specific_voters/<poll_id>/<answer>/<question>/<answers>/<multiple_choice>',
           methods=['GET', 'POST'])
def send_to_specific_voters(poll_id, answer, question, answers, multiple_choice):
    try:
        answers = answers.split(',')
        answers = [a for a in answers if len(a) > 0]
        # in the future will need to send to the poll function a list of chat_id's
        Result = db.session.query(Polls_answers).filter(Polls_answers.poll_ID == poll_id).all()
        chat_ID = []
        for result in Result:
            for ans in result.answers:
                # ans is type string
                if ans == answer:
                    chat_ID.append(result.user_ID)
        print(chat_ID)
        if chat_ID:
            backend.telegram_bot.poll(chat_ID, question, answers, multiple_choice)
        else:
            return {"result": "empty"}
    except Exception as e:
        db.session.remove()
        raise e
    return {"result": True}


@app.route('/add_poll', methods=['GET', 'POST'])
def add_poll(poll_id, question, answers, answers_counter, closed, multiple_choice,
             quiz, correct_answers, solution):
    try:
        poll = Polls(poll_id, question, answers, answers_counter, closed, multiple_choice,
                     quiz, correct_answers, solution)
        db.session.add(poll)
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e


@app.route('/add_answer', methods=['GET', 'POST'])
def add_answer(fake_ID, user_id, answers, is_correct):
    try:
        res = db.session.query(Mapping).filter(Mapping.fake_ID == fake_ID).first()
        poll_id = res.poll_ID
        answer = Polls_answers(poll_id, user_id, answers, is_correct)
        db.session.add(answer)
        db.session.commit()
        # add code for adding an answer to the answers_counter
        Result = db.session.query(Polls).filter(Polls.poll_ID == poll_id).first()
        for a in answers:
            counter = Result.answers_counter[a] + 1
            Result.answers_counter.updateItem(a, counter)
            db.session.commit()

    except Exception as e:
        db.session.remove()
        raise e


@app.route('/delete_poll', methods=['POST'])
def delete_poll(poll_id):
    try:
        Polls.query.filter_by(poll_ID=poll_id).delete()
        db.session.commit()
    except Exception as e:
        db.session.remove()
        raise e


@app.route('/auth_admin/<username>/<password>', methods=['GET', 'POST'])
def auth_admin(username, password):
    try:
        Result = db.session.query(Admins).filter(Admins.id == username)
        hashed_password = Result[0].Password
    except Exception as e:
        print("Exception is " + str(e))
        return {"result": False}
    flag = check_password_hash(hashed_password, password)
    if flag:
        # flask_login.login_user(Result[0])
        session["user_id"] = (Result[0].id + Result[0].Password)
        # user_id = session.get("user_id")
        # print(user_id)
        return jsonify({"result": True})
    else:
        return {"result": False}


@app.route("/cookie", methods=['GET', 'POST'])
def get_current_user():
    user_id = session.get("user_id")
    print(user_id)
    if not user_id:
        session.clear()
    # print(user_id)
    return {"result": user_id}


@app.route("/logout", methods=['GET', 'POST'])
def logout_user():
    try:
        '''Session.query.filter_by(id=sql_session_model.id).delete()
        db.session.commit()'''
        # session["user_id"] = None
        session.clear()
        # session.pop("user_id")
    except Exception as e:
        db.session.remove()
        raise e
    return {"result": True}


@app.route('/generate_hash')
def generate_hash(incoming_password):
    return generate_password_hash(incoming_password)


@app.route('/all_polls_data', methods=['GET', 'POST'])
def all_polls_data():
    polls = {}
    try:
        Result = db.session.query(Polls).all()
        print("wow1")
        i = 0
        for poll in Result:
            polls[i] = {
                "poll_ID": poll.poll_ID,
                "question": poll.question,
                "answers": poll.answers,
                "answers_counter": poll.answers_counter,
                "multiple_choice": poll.multiple_choice,
                "correct_answers": poll.correct_answers,
                "solution": poll.solution
            }
            i += 1

    except Exception as e:
        # print("error is fun!!!!")
        db.session.remove()
        raise e
    # print(polls)
    # print(type(polls))
    # print(len(polls))
    return polls


@app.route('/all_users_data', methods=['GET', 'POST'])
def all_users_data():
    users = {}

    try:
        Result = db.session.query(Student).all()
        i = 0
        for user in Result:
            users[i] = {
                "user_ID": user.user_ID,
                "name": user.name
            }
            i += 1

    except Exception as e:
        db.session.remove()
        raise e
    print(users)
    return users


# function that receives poll_ID and returns dict of answer and number of votes it got
@app.route('/poll_answers/<poll_id>', methods=['GET', 'POST'])
def poll_answers(poll_id):
    answers = {}
    try:
        Result = db.session.query(Polls).filter(Polls.poll_ID == poll_id).first()

        for i in range(len(Result.answers)):
            key = Result.answers[i]
            value = Result.answers_counter[i]
            answers[key] = value


    except Exception as e:
        db.session.remove()
        raise e
    print(answers)
    return answers


# function that receives user_ID and returns dict of poll_ID's and the specific user answers to the polls
@app.route('/specific_user_answers/<user_id>', methods=['GET', 'POST'])
def specific_user_answers(user_id):
    # poll_id, question, his answer
    data = {}
    try:
        Result = db.session.query(Polls_answers).filter(Polls_answers.user_ID == user_id).all()
        i = 0
        for res in Result:
            poll_id = res.poll_ID
            votes = res.answers
            Comeback = db.session.query(Polls).filter(Polls.poll_ID == poll_id).first()
            question = Comeback.question
            text_answers = []
            for ans in votes:
                text_answers.append(Comeback.answers[int(ans)])
            data[i] = {
                "poll_ID": poll_id,
                "question": question,
                "answers": text_answers
            }
            i += 1


    except Exception as e:
        db.session.remove()
        raise e
    print(data)
    return data


if __name__ == '__main__':  # python interpreter assigns "__main__" to the file you run
    # all_users_data()
    # poll_answers("5967495296991625252")
    # specific_user_answers("5045706840")
    # init_poll([5045706840], "asdas?", "fdsf , dfdf, 1, 2", True)
    # send_poll_to_all("pika", "yes , no", False)
    # send_to_specific_voters("5976421871120285710", "1", "Youuuu", "yes , no", False)
    #add_admin(username="daniel", password="pikapika")
    #add_admin("daniel", "pikapika")
    #delete("5045706840")
    #delete("1756044528")
    app.run(debug=True)
