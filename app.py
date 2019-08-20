from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/cello_teachers'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zujevjaijeckei:318bfd2b64b892ffc968951535c9fec3699ad807221b919d97a104b749492cd1@ec2-54-235-92-244.compute-1.amazonaws.com:5432/d69qud2rp3o086'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    teacher = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, teacher, rating, comments):
        self.customer = customer
        self.teacher = teacher
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['cellist']
        teacher = request.form['teacher']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, teacher, rating, comments)
        if customer == '' or teacher == '':
            return render_template('index.html', message='Please enter required fields')

        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, teacher, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, teacher, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.debug = True
    app.run()
