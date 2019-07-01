import os, json
import unittest

from app import app, db

TEST_DB = 'test.db'


class BookTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['BASEDIR'] = os.path.dirname(os.path.abspath(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/test_book"
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        with app.app_context():
            db.drop_all()

    ###############
    #### tests ####
    ###############
    def create_book_helper(self):
        self.app.post('/api/v1/books',
                      data=json.dumps({'name': 'book', 'isbn': '1234', 'country': 'india', 'publisher': 'vishal',
                                       'authors': ['john doe'], 'number_of_pages': 123, 'release_date': '2019-01-01'}),
                      content_type='application/json')

    def test_create_book(self):
        response = self.app.post('/api/v1/books',
                                 data=json.dumps({'name':'book', 'isbn':'1234', 'country':'india', 'publisher':'vishal',
                                                  'authors': ['john doe'], 'number_of_pages': 123,
                                                  'release_date': '2019-01-01'}),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['status_code'], 201)
        self.assertEqual(data['data'][0].get('book').get('name'), 'book')

    def test_create_book_bad_request(self):
        response = self.app.post('/api/v1/books',
                                 data=json.dumps({'name':'book1','isbn': '1234', 'country':'india', 'publisher':'',
                                                  'number_of_pages': 123, 'release_date': '2019-01-01'}),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_code'], 400)

    def test_get_book(self):
        self.create_book_helper()

        response = self.app.get('/api/v1/books/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['data'][0].get('name'), 'book')

    def test_get_book_not_exists(self):
        response = self.app.get('/api/v1/books/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(len(data['data']), 0)

    def test_get_books(self):
        self.create_book_helper()

        response = self.app.get('/api/v1/books')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(len(data['data']), 1)

    def test_get_books_with_url_parameters(self):
        self.create_book_helper()

        response = self.app.get('/api/v1/books?name=book&country=india&release_date=2019&publisher=vishal')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(len(data['data']), 1)

    def test_get_books_with_url_parameters_not_exists(self):
        self.create_book_helper()

        response = self.app.get('/api/v1/books?name=mybook&country=india&release_date=2019&publisher=vishal')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(len(data['data']), 0)

    def test_update_book(self):
        self.create_book_helper()

        response = self.app.patch('/api/v1/books/1',
                                data=json.dumps({'name': 'book1', 'isbn': '12345', 'publisher': 'vishal kumar',
                                                 'number_of_pages': 230, 'country': 'India', 'release_date': '2019-05-01'}),
                                content_type='application/json'
                                )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], 'The book book was updated successfully')
        self.assertEqual(data['data'][0].get('name'), 'book1')
        self.assertEqual(data['data'][0].get('publisher'), 'vishal kumar')

    def test_delete_book_id_exists(self):
        self.create_book_helper()

        response = self.app.delete('/api/v1/books/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], 'The book book was deleted successfully')
        self.assertEqual(len(data['data']), 0)

    def test_delete_book_id_not_exists(self):
        response = self.app.delete('/api/v1/books/2')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], 'No book exists for id 2')
        self.assertEqual(len(data['data']), 0)

    def test_get_external_books(self):
        response = self.app.get('api/external-books?name=A Game of Thrones')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0].get('name'), 'A Game of Thrones')

    def test_get_external_books_no_url_param(self):
        response = self.app.get('api/external-books')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['status_code'], 400)
        self.assertEqual(data['message'], 'Please provide book name in URL parameters.')



if __name__ == "__main__":
    unittest.main()
