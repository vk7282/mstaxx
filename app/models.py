from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    isbn = db.Column(db.String(80), unique=True, nullable=False, index=True)
    authors = db.Column(ARRAY(db.String), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    number_of_pages = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(80), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'isbn': self.isbn,
            'authors': self.authors,
            'country': self.country,
            'number_of_pages': self.number_of_pages,
            'publisher': self.publisher,
            'release_date': str(self.release_date)
        }

