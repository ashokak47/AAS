from flask import Flask, request, render_template, redirect, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
import requests

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'enquiry.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
db.init_app(app)


class Enquiry(db.Model):
    __tablename__ = "enquiry"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    message = db.Column(db.String(200))
    enq_datetime = db.Column(db.String(20))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/inner')
def inner():
    return render_template('inner-page.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio-details.html')


@app.route('/enquiry', methods=['GET', 'POST'])
def enquiry():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        msg = request.form.get('message')
        enq_datetime = datetime.now()
        # print(name,email,message,subject,enq_datetime)
        data = Enquiry(name=name, email=email, subject=subject, message=msg, enq_datetime=enq_datetime)
        db.session.add(data)
        db.session.commit()
        flash('Your message has been sent successfully. Our team will contact you soon. Thank you.', 'success')
        sms = "Name : "+name+",Email:"+email+",Message:"+msg
        requests.post("https://ntfy.sh/AAS", data=sms.encode(encoding='utf-8'))
        return redirect('/')
    else:
        data = db.session.query(Enquiry).all()
        return render_template('enquiry.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
