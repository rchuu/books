from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book


@app.route('/')
def index():
    return redirect('/authors')


@app.route('/authors')
def authors():
    authors = Author.get_all()
    return render_template("authors.html", all_authors=authors)


@app.route('/create/authors', methods=['POST'])
def create_author():
    data = {
        "name": request.form['name'],
    }
    Author.save(data)
    # Dojo.save(request.form)
    return redirect('/authors')  # never render a post
    # return("success")


@app.route('/author/<int:id>')
def show_author(id):
    data = {
        "id": id
    }
    return render_template('showauthors.html', authors=Author.get_one_with_books(data), unfavorited_books=Book.show_unfavorited_books(data))


@app.route('/join/book', methods=['POST'])
def join_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_favorite(data)
    return redirect(f"/author/{request.form['author_id']}")
