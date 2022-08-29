from flask import Flask, render_template, request, redirect, url_for
from wtforms import StringField, PasswordField, SubmitField, validators, EmailField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

# Database Creation using SQLITE3
# import sqlite3
#
# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# cursor.execute(
#     "CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
#
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={"autoflush": False})


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120), unique=False, nullable=False)
    review = db.Column(db.Float, primary_key=False)

    def __repr__(self):
        return f'<Books: {self.title}'


# db.create_all()
# book1 = Books(title="Harry Potter", author="J. K. Rowling", review=9.3)
# db.session.add(book1)
# db.session.commit()
# Books.query.all()

app.secret_key = "some secret string"


@app.route('/')
def home():
    # print(all_books)'
    all_books = db.session.query(Books).all()

    return render_template('index.html', books=all_books)


@app.route('/delete/<int:post_id>')
def delete_book(post_id):
    book_to_delete = Books.query.get(post_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/edit_rating/<int:post_id>', methods=['GET', 'POST'])
def edit_rating(post_id):
    class MyForm(FlaskForm):
        id = StringField('Id', [validators.data_required()])
        review = StringField('Rating', [validators.data_required()])

    form = MyForm()

    if request.method == 'POST':
        book_to_update = Books.query.get(post_id)
        book_to_update.review = form.data["review"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit_rating.html", id=post_id)


@app.route("/add", methods=["GET", "POST"])
def add():
    class MyForm(FlaskForm):
        title = StringField('Book Name', [validators.data_required()])
        author = PasswordField('Book Author', [validators.data_required()])
        review = StringField('Rating', [validators.data_required()])

    form = MyForm()
    if request.method == 'POST':
        book1 = Books(title=form.data["title"], author=form.data["author"], review=form.data["review"])
        db.session.add(book1)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('add.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
