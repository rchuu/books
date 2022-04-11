from flask_app import app
from flask import render_template, redirect, request
from flask_app.models import author, book


@app.route('/books')
def books():
    books = book.Book.get_all()
    return render_template("books.html", all_books=books)


@app.route('/create/books', methods=['POST'])
def create_book():
    data = {
        "title": request.form['title'],
        "num_of_pages": request.form['num_of_pages']
    }
    book_id = book.Book.save(data)  # why the book_id?
    return redirect('/books')


@app.route('/book/<int:id>')
def showbooks(id):
    data = {
        "id": id
    }
    return render_template('showbooks.html', book=book.Book.get_by_id(data), unfavorited_authors=author.Author.unfavorited_authors(data))


@app.route('/join/author', methods=['POST'])
def join_author():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    author.Author.add_favorite(data)
    # return redirect('/')
    return redirect(f"/book/{request.form['book_id']}")
