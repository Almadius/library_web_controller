import unittest
from library.book import Book
from library.member import Member
from library.library import Library


class TestLibrary(unittest.TestCase):

    def test_add_and_find_book(self):
        library = Library()
        book = Book("1984", "George Orwell", 1949)
        library.add_book(book)
        found_book = library.find_book("1984")
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book.title, "1984")

    def test_remove_book(self):
        library = Library()
        book = Book("1984", "George Orwell", 1949)
        library.add_book(book)
        self.assertTrue(library.remove_book("1984"))
        self.assertIsNone(library.find_book("1984"))

    def test_register_and_find_member(self):
        library = Library()
        member = Member("Alice", 1)
        library.register_member(member)
        found_member = library.find_member(1)
        self.assertIsNotNone(found_member)
        self.assertEqual(found_member.name, "Alice")

    def test_remove_member(self):
        library = Library()
        member = Member("Alice", 1)
        library.register_member(member)
        self.assertTrue(library.remove_member(1))
        self.assertIsNone(library.find_member(1))

    def test_borrow_and_return_book(self):
        library = Library()
        book = Book("1984", "George Orwell", 1949)
        member = Member("Alice", 1)
        library.add_book(book)
        library.register_member(member)

        library.borrow_book(1, "1984")
        self.assertIsNone(library.find_book("1984"))

        library.return_book(1)
        self.assertIsNotNone(library.find_book("1984"))


if __name__ == '__main__':
    unittest.main()
