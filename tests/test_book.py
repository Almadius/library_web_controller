import unittest
from library.book import Book

class TestBook(unittest.TestCase):

    def test_book_creation(self):
        book = Book("1984", "George Orwell", 1949)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "George Orwell")
        self.assertEqual(book.year, 1949)

    def test_book_str(self):
        book = Book("1984", "George Orwell", 1949)
        self.assertEqual(str(book), "1984 by George Orwell (1949)")

if __name__ == '__main__':
    unittest.main()
