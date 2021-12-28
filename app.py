from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:porat2410@localhost/Namba'

db=SQLAlchemy(app)

class Student(db.Model):
    __tablename__='users'
    username=db.Column(db.String(40),primary_key=True)

    def __init__(self,username):
        self.username=username


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username= request.form['username']
    student=Student(username)
    db.session.add(student)
    db.session.commit()

    return render_template('success.html', data=username)

@app.route('/delete', methods=['POST'])
def delete():
    username1= request.form['username1']
    #student=Student(username)
    #db.session.(student)
    Student.query.filter_by(username=username1).delete()
    db.session.commit()

    return render_template('success.html', data=username1)



if __name__ == '__main__':  #python interpreter assigns "__main__" to the file you run
    app.run(debug=True)