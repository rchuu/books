from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author, book  # importing that ninja class


class Book:
    db = 'books_schema'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_who_favorited = []  # why this?

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(cls.db).query_db(query)
        books = []

        for row in results:
            books.append(cls(row))
        return books

    @classmethod
    def save(cls, data):
        query = """INSERT INTO books(title, num_of_pages) 
        VALUES (%(title)s,%(num_of_pages)s);"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def show_unfavorited_books(cls, data):
        query = """SELECT * FROM books
        WHERE books.id NOT IN 
        (SELECT book_id FROM favorites
        WHERE author_id = %(id)s);
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        books = []

        for row in result:
            books.append(cls(row))
        return books

    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * FROM books 
        LEFT JOIN favorites 
        ON books.id = favorites.book_id 
        LEFT JOIN authors 
        ON authors.id = favorites.author_id 
        WHERE books.id = %(id)s;"""

        result = connectToMySQL(cls.db).query_db(query, data)

        books = cls(result[0])  # making the book into its own class

        # translating the data from into these different rows - appending it to authors who favorited it
        for row in result:
            if row['authors.id'] == None:  # if there is no author id, there is no favorite authors
                break
            data = {
                "id": row['authors.id'],
                "name": row['name'],
                "created_at": row['authors.created_at'],
                "updated_at": row['authors.updated_at']
            }
            books.authors_who_favorited.append(author.Author(data))
        return books
