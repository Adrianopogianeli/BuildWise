from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.String(20), nullable=False)

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pub_date = request.form['publication_date']
        new_book = Book(title=title, author=author, publication_date=pub_date)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book = Book.query.get(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.publication_date = request.form['publication_date']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', book=book)

@app.route('/delete/<int:id>')
def delete(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # to run in container  host='0.0.0.0' ,port=8080
        app.run(debug=True, host='0.0.0.0' ,port=8080)
