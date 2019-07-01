# in-built libs
import json

# 3rd party libs
import requests
from sqlalchemy.sql import extract
from flask import Flask, jsonify, request

# project libs
from app.models import db, Book
from config import Config

# initialize the app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# endpoint to get external books
@app.route('/api/external-books')
def get_external_books():
    # check if the name from url parameter exists, if not return failure
    if request.args.get('name') is None:
        return jsonify(message='Please provide book name in URL parameters.', status_code=400, status='failure')
    # get the name from url params
    book_name = request.args.get('name')
    # IceandFireAPI url
    url = "https://www.anapioficeandfire.com/api/books/?name="+book_name
    # get the response from url
    response = requests.get(url)
    json_data = json.loads(response.text)
    data = []
    # process if status code is 200
    if response.status_code == 200:
        for entry in json_data:
                item = {}
                item['name'] = entry.get('name')
                item['isbn'] = entry.get('isbn')
                item['authors'] = entry.get('authors')
                item['number_of_pages'] = entry.get('number_of_pages')
                item['publisher'] = entry.get('publisher')
                item['country'] = entry.get('country')
                item['release_date'] = entry.get('release_date')
                data.append(item)
        status = 'success'
    else:
        status = 'failure'
    return jsonify(status_code=response.status_code, status=status, data=data)


# endpoint to create book
@app.route('/api/v1/books', methods = ['POST'])
def create_book():
    # check if json body is valid
    if not valid(request.json):
        return jsonify(status_code=400, status='failure', data=[])

    # get json body and create book
    name = request.json.get('name')
    isbn = request.json.get('isbn')
    authors = request.json.get('authors')
    pages = request.json.get('number_of_pages')
    publisher = request.json.get('publisher')
    country = request.json.get('country')
    release_date = request.json.get('release_date')
    book = Book(name=name, isbn=isbn, authors=authors, number_of_pages=pages, publisher=publisher,
                country=country, release_date=release_date)
    # add the book to database and commit the transaction
    db.session.add(book)
    db.session.commit()
    return jsonify(status_code=201, status='success', data=[{'book': book.to_json()}])


# endpoint to get all books
@app.route("/api/v1/books", methods=["GET"])
def get_all_books():
    # Get all books if url params don't exist else filter on url params
    if not request.args:
        books = Book.query.all()
    else:
        if 'release_date' in request.args:
            year = str(request.args['release_date'])
        name = request.args['name']
        country = request.args['country']
        publisher = request.args['publisher']
        books = Book.query.filter(Book.name==name).filter(Book.country==country).filter(Book.publisher==publisher) \
            .filter(extract('year', Book.release_date) == year).all()
    all_books = [book.to_json() for book in books]
    return jsonify(status_code=200, status='success', data=all_books)


# endpoint to get individual book
@app.route("/api/v1/books/<id>", methods=["GET"])
def get_book_details(id):
    book = Book.query.get(id)
    if not book:
        data = []
    else:
        data = [book.to_json()]
    return jsonify(status_code=200, status='success', data=data)


# endpoint to update individiual book
@app.route("/api/v1/books/<id>", methods=["PATCH"])
def update_book(id):
    # query the book id and then update
    book = Book.query.get(id)
    old_name = book.name
    if 'name' in request.json:
        book.name = request.json['name']
    if 'isbn' in request.json:
        book.isbn = request.json['isbn']
    if 'publisher' in request.json:
        book.publisher = request.json['publisher']
    if 'number_of_pages' in request.json:
        book.number_of_pages = request.json['number_of_pages']
    if 'country' in request.json:
        book.country = request.json['country']
    if 'release_date' in request.json:
        book.release_date = request.json['release_date']

    db.session.commit()
    return jsonify(status_code=200, status='success', data=[book.to_json()],
                   message="The book %s was updated successfully" % old_name)


# endpoint to delete book
@app.route("/api/v1/books/<id>", methods=["DELETE"])
def delete_book(id):
    # query the book id and delete from db
    book = Book.query.get(id)
    if not book:
        message = 'No book exists for id {}'.format(id)
    else:
        db.session.delete(book)
        message = "The book {} was deleted successfully".format(book.name)
    db.session.commit()

    return jsonify(status_code=200, status='success', data=[], message=message)


def valid(data):
    for key, value in data.items():
        if not value:
            return False
    return True
