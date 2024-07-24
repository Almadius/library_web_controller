from datetime import datetime, timedelta
from .book import Book
from .member import Member
from .database import Database

class Library:
    """Класс, представляющий библиотеку, управляющую книгами и пользователями."""

    def __init__(self):
        """Инициализирует библиотеку с базой данных."""
        self.db = Database()

    def add_book(self, book):
        """Добавляет книгу в библиотеку."""
        existing_book = self.db.fetchone("SELECT * FROM books WHERE title = ?", (book.title,))
        if existing_book:
            self.db.execute("UPDATE books SET copies = copies + ? WHERE title = ?", (book.copies, book.title))
        else:
            self.db.execute("INSERT INTO books (title, author, year, copies) VALUES (?, ?, ?, ?)", (book.title, book.author, book.year, book.copies))

    def remove_book(self, title):
        """Убирает книгу из библиотеки по названию."""
        book = self.db.fetchone("SELECT * FROM books WHERE title = ?", (title,))
        if book:
            if book[4] > 1:  # если количество экземпляров больше одного
                self.db.execute("UPDATE books SET copies = copies - 1 WHERE title = ?", (title,))
            else:
                self.db.execute("DELETE FROM books WHERE title = ?", (title,))
            return True
        return False

    def find_book(self, title):
        """Находит книгу в библиотеке по названию."""
        book = self.db.fetchone("SELECT * FROM books WHERE title = ?", (title,))
        if book:
            return Book(book[1], book[2], book[3], book[4])
        return None

    def find_books_by_author(self, author):
        """Находит книги в библиотеке по автору."""
        rows = self.db.fetchall("SELECT * FROM books WHERE author = ?", (author,))
        return [Book(row[1], row[2], row[3], row[4]) for row in rows]

    def register_member(self, member):
        """Регистрирует нового пользователя библиотеки."""
        self.db.execute("INSERT INTO members (name, email, password_hash) VALUES (?, ?, ?)",
                        (member.name, member.email, member.password_hash))

    def remove_member(self, member_id):
        """Убирает пользователя из библиотеки по ID."""
        member = self.db.fetchone("SELECT * FROM members WHERE id = ?", (member_id,))
        if member:
            self.db.execute("DELETE FROM members WHERE id = ?", (member_id,))
            return True
        return False

    def find_member(self, member_id):
        """Находит пользователя в библиотеке по ID."""
        member = self.db.fetchone("SELECT * FROM members WHERE id = ?", (member_id,))
        if member:
            return Member(member[1], member[0])
        return None

    def find_members_by_name(self, name):
        """Находит пользователей в библиотеке по имени."""
        rows = self.db.fetchall("SELECT * FROM members WHERE name = ?", (name,))
        return [Member(row[1], row[0]) for row in rows]

    def borrow_book(self, member_id, book_title):
        """Позволяет пользователям взять книгу на прокат."""
        member = self.find_member(member_id)
        book = self.find_book(book_title)

        if not member:
            raise ValueError(f"Пользователь с ID {member_id} не найден.")
        if not book:
            raise ValueError(f"Книга с названием '{book_title}' не найдена.")

        due_date = datetime.now() + timedelta(days=14)  # Прокат на 14 дней
        self.db.execute("INSERT INTO borrowed_books (member_id, book_id, due_date) VALUES (?, ?, ?)",
                        (member_id, book.title, due_date.strftime('%Y-%m-%d')))
        self.remove_book(book_title)
        print(f"Пользователь {member.name} взял книгу '{book.title}' на прокат до {due_date.strftime('%Y-%m-%d')}.")

    def return_book(self, member_id, book_title):
        """Позволяет пользователи вернуть книгу."""
        borrowed_book = self.db.fetchone("SELECT * FROM borrowed_books WHERE member_id = ? AND book_id = ?",
                                         (member_id, book_title))
        if borrowed_book:
            self.db.execute("DELETE FROM borrowed_books WHERE member_id = ? AND book_id = ?", (member_id, book_title))
            self.add_book(Book(book_title, "", 0, 1))  # Создаем книгу с одним экземпляром для возврата
            due_date = datetime.strptime(borrowed_book[2], '%Y-%m-%d')
            member = self.find_member(member_id)
            if datetime.now() > due_date:
                overdue_days = (datetime.now() - due_date).days
                fine = overdue_days * 1  # Допустим, штраф $1 за каждый день просрочки
                print(f"Пользователь {member.name} вернул книгу '{book_title}' с опозданием на {overdue_days} дней. Штраф: ${fine}.")
            else:
                print(f"Пользователь {member.name} вернул книгу '{book_title}' вовремя.")
        else:
            raise ValueError(f"Пользователь с ID {member_id} не брал книгу '{book_title}' на прокат.")

    def reserve_book(self, member_id, book_title):
        """Позволяет пользователям забронировать книгу."""
        member = self.find_member(member_id)
        book = self.find_book(book_title)

        if not member:
            raise ValueError(f"Пользователь с ID {member_id} не найден.")
        if not book:
            raise ValueError(f"Книга с названием '{book_title}' не найдена.")

        reservation_date = datetime.now()
        self.db.execute("INSERT INTO reservations (member_id, book_id, reservation_date) VALUES (?, ?, ?)",
                        (member_id, book.title, reservation_date.strftime('%Y-%m-%d')))
        print(f"Пользователь {member.name} забронировал книгу '{book.title}' на дату {reservation_date.strftime('%Y-%m-%d')}.")

    def cancel_reservation(self, member_id, book_title):
        """Позволяет пользователям отменить бронирование книги."""
        reservation = self.db.fetchone("SELECT * FROM reservations WHERE member_id = ? AND book_id = ?",
                                       (member_id, book_title))
        if reservation:
            self.db.execute("DELETE FROM reservations WHERE member_id = ? AND book_id = ?", (member_id, book_title))
            print(f"Бронирование книги '{book_title}' пользователем с ID {member_id} отменено.")
        else:
            raise ValueError(f"Пользователь с ID {member_id} не бронировал книгу '{book_title}'.")