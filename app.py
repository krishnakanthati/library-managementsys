from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///library.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Member(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    bookID = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(25), nullable=False)
    date_issued = db.Column(db.DateTime, default=datetime.utcnow)
    date_returned = db.Column(db.DateTime, nullable=True)
    fee = db.Column(db.Float, default=0.0)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} - {self.bookID}"


class Book(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    bookID = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)

    def __repr__(self) -> str:
        return f"{self.bookID} - {self.title} - {self.sno}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        bookID = Book.query.filter_by(title=title).first().bookID
        lib = Member(title=title, name=name, bookID=bookID)
        db.session.add(lib)
        db.session.commit()
    books = Book.query.all()
    members = Member.query.all()
    return render_template('index.html', books=books, members=members)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        name = request.form['name']
        members = Member.query.filter_by(sno=sno).first()
        if (request.form.get('return') != None):
            members.date_returned = datetime.utcnow()
            members.fee = (members.date_returned -
                           members.date_issued).days * 5.0 + 5.0
        members.name = name
        db.session.add(members)
        db.session.commit()
        return redirect("/")
    members = Member.query.filter_by(sno=sno).first()
    return render_template('update.html', members=members)


@app.route('/import/<int:bookID>', methods=['GET', 'POST'])
def import_book(bookID):
    if request.method == 'POST':
        title = request.form['title']
        quantity = int(request.form['quantity'])
        book = Book(bookID=bookID, quantity=quantity, title=title)
        db.session.add(book)
        db.session.commit()
    return redirect("/")


@app.route('/delete/<int:sno>')
def delete(sno):
    book = Member.query.filter_by(sno=sno).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


@app.route('/books', methods=['GET', 'POST'])
def books():
    req = requests.get('https://frappe.io/api/method/frappe-library')
    data = json.loads(req.content)
    return render_template('books.html', message=data['message'])


if __name__ == "__main__":
    app.run(debug=True)
