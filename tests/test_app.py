import unittest
from flask import Flask
from flask_testing import TestCase
from web.app import app, library

class TestLibraryManagementSystem(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        # Set up a blank slate for each test
        library.db.execute("DELETE FROM borrowed_books")
        library.db.execute("DELETE FROM reservations")
        library.db.execute("DELETE FROM members")
        library.db.execute("DELETE FROM books")

    def tearDown(self):
        # Clean up any leftover data
        self.setUp()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Library Management System', response.data)

    def test_add_book(self):
        response = self.client.post('/add_book', data=dict(
            title='Test Book',
            author='Test Author',
            year=2021,
            copies=3
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Книга 'Test Book' добавлена в библиотеку.", response.data)

    def test_register_member(self):
        response = self.client.post('/register_member', data=dict(
            name='Test Member',
            member_id=1
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Пользователь 'Test Member' с ID 1 зарегистрирован в библиотеке.", response.data)

    def test_borrow_book(self):
        self.client.post('/add_book', data=dict(
            title='Test Book',
            author='Test Author',
            year=2021,
            copies=1
        ), follow_redirects=True)
        self.client.post('/register_member', data=dict(
            name='Test Member',
            member_id=1
        ), follow_redirects=True)
        response = self.client.post('/borrow_book', data=dict(
            member_id=1,
            title='Test Book'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Книга 'Test Book' выдана пользователю с ID 1.", response.data)

    def test_return_book(self):
        self.client.post('/add_book', data=dict(
            title='Test Book',
            author='Test Author',
            year=2021,
            copies=1
        ), follow_redirects=True)
        self.client.post('/register_member', data=dict(
            name='Test Member',
            member_id=1
        ), follow_redirects=True)
        self.client.post('/borrow_book', data=dict(
            member_id=1,
            title='Test Book'
        ), follow_redirects=True)
        response = self.client.post('/return_book', data=dict(
            member_id=1,
            title='Test Book'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Книга 'Test Book' возвращена пользователем с ID 1.", response.data)

    def test_reserve_book(self):
        self.client.post('/add_book', data=dict(
            title='Test Book',
            author='Test Author',
            year=2021,
            copies=1
        ), follow_redirects=True)
        self.client.post('/register_member', data=dict(
            name='Test Member',
            member_id=1
        ), follow_redirects=True)
        response = self.client.post('/reserve_book', data=dict(
            member_id=1,
            title='Test Book'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Книга 'Test Book' забронирована пользователем с ID 1.", response.data)

    def test_cancel_reservation(self):
        self.client.post('/add_book', data=dict(
            title='Test Book',
            author='Test Author',
            year=2021,
            copies=1
        ), follow_redirects=True)
        self.client.post('/register_member', data=dict(
            name='Test Member',
            member_id=1
        ), follow_redirects=True)
        self.client.post('/reserve_book', data=dict(
            member_id=1,
            title='Test Book'
        ), follow_redirects=True)
        response = self.client.post('/cancel_reservation', data=dict(
            member_id=1,
            title='Test Book'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Бронирование книги 'Test Book' пользователем с ID 1 отменено.", response.data)

if __name__ == '__main__':
    unittest.main()
