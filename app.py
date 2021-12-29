from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit(id, name):

    student=Student(id, name)
    db.session.add(student)
    db.session.commit()



@app.route('/delete', methods=['POST'])
def delete(id):

    Student.query.filter_by(user_ID=id).delete()
    db.session.commit()



if __name__ == '__main__':  #python interpreter assigns "__main__" to the file you run
    app.run(debug=True)