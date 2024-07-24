import argparse
from library.book import Book
from library.member import Member
from library.library import Library

library = Library()

def add_book(args):
    book = Book(args.title, args.author, args.year, args.copies)
    library.add_book(book)
    print(f"Книга '{book.title}' добавлена в библиотеку.")

def remove_book(args):
    if library.remove_book(args.title):
        print(f"Книга '{args.title}' удалена из библиотеки.")
    else:
        print(f"Книга '{args.title}' не найдена в библиотеке.")

def find_book(args):
    book = library.find_book(args.title)
    if book:
        print(f"Найдена книга: {book}")
    else:
        print(f"Книга '{args.title}' не найдена.")

def find_books_by_author(args):
    books = library.find_books_by_author(args.author)
    if books:
        print(f"Найдены книги автора '{args.author}':")
        for book in books:
            print(book)
    else:
        print(f"Книги автора '{args.author}' не найдены.")

def register_member(args):
    member = Member(args.name, args.id)
    library.register_member(member)
    print(f"Пользователь '{member.name}' с ID {member.member_id} зарегистрирован в библиотеке.")

def remove_member(args):
    if library.remove_member(args.id):
        print(f"Пользователь с ID {args.id} удален из библиотеки.")
    else:
        print(f"Пользователь с ID {args.id} не найден.")

def find_member(args):
    member = library.find_member(args.id)
    if member:
        print(f"Найден пользователь: {member}")
    else:
        print(f"Пользователь с ID {args.id} не найден.")

def find_members_by_name(args):
    members = library.find_members_by_name(args.name)
    if members:
        print(f"Найдены пользователи с именем '{args.name}':")
        for member in members:
            print(member)
    else:
        print(f"Пользователи с именем '{args.name}' не найдены.")

def borrow_book(args):
    try:
        library.borrow_book(args.member_id, args.title)
    except ValueError as e:
        print(e)

def return_book(args):
    try:
        library.return_book(args.member_id, args.title)
    except ValueError as e:
        print(e)

def reserve_book(args):
    try:
        library.reserve_book(args.member_id, args.title)
    except ValueError as e:
        print(e)

def cancel_reservation(args):
    try:
         library.cancel_reservation(args.member_id, args.title)
    except ValueError as e:
        print(e)


def main():
    parser = argparse.ArgumentParser(description="Library Management System")

    subparsers = parser.add_subparsers()

    # Add book
    parser_add_book = subparsers.add_parser('add_book', help='Добавить книгу в библиотеку')
    parser_add_book.add_argument('title', type=str, help='Название книги')
    parser_add_book.add_argument('author', type=str, help='Автор книги')
    parser_add_book.add_argument('year', type=int, help='Год издания книги')
    parser_add_book.add_argument('--copies', type=int, default=1, help='Количество экземпляров книги')
    parser_add_book.set_defaults(func=add_book)

    # Remove book
    parser_remove_book = subparsers.add_parser('remove_book', help='Удалить книгу из библиотеки')
    parser_remove_book.add_argument('title', type=str, help='Название книги')
    parser_remove_book.set_defaults(func=remove_book)

    # Find book
    parser_find_book = subparsers.add_parser('find_book', help='Найти книгу в библиотеке')
    parser_find_book.add_argument('title', type=str, help='Название книги')
    parser_find_book.set_defaults(func=find_book)

    # Find books by author
    parser_find_books_by_author = subparsers.add_parser('find_books_by_author', help='Найти книги в библиотеке по автору')
    parser_find_books_by_author.add_argument('author', type=str, help='Автор книги')
    parser_find_books_by_author.set_defaults(func=find_books_by_author)

    # Register member
    parser_register_member = subparsers.add_parser('register_member', help='Зарегистрировать пользователя библиотеки')
    parser_register_member.add_argument('name', type=str, help='Имя пользователя')
    parser_register_member.add_argument('id', type=int, help='ID пользователя')
    parser_register_member.set_defaults(func=register_member)

    # Remove member
    parser_remove_member = subparsers.add_parser('remove_member', help='Удалить пользователя из библиотеки')
    parser_remove_member.add_argument('id', type=int, help='ID пользователя')
    parser_remove_member.set_defaults(func=remove_member)

    # Find member
    parser_find_member = subparsers.add_parser('find_member', help='Найти пользователя в библиотеке')
    parser_find_member.add_argument('id', type=int, help='ID пользователя')
    parser_find_member.set_defaults(func=find_member)

    # Find members by name
    parser_find_members_by_name = subparsers.add_parser('find_members_by_name', help='Найти пользователей в библиотеке по имени')
    parser_find_members_by_name.add_argument('name', type=str, help='Имя пользователя')
    parser_find_members_by_name.set_defaults(func=find_members_by_name)

    # Borrow book
    parser_borrow_book = subparsers.add_parser('borrow_book', help='Взять книгу на прокат')
    parser_borrow_book.add_argument('member_id', type=int, help='ID пользователя')
    parser_borrow_book.add_argument('title', type=str, help='Название книги')
    parser_borrow_book.set_defaults(func=borrow_book)

    # Return book
    parser_return_book = subparsers.add_parser('return_book', help='Вернуть книгу')
    parser_return_book.add_argument('member_id', type=int, help='ID пользователя')
    parser_return_book.add_argument('title', type=str, help='Название книги')
    parser_return_book.set_defaults(func=return_book)

    # Reserve book
    parser_reserve_book = subparsers.add_parser('reserve_book', help='Забронировать книгу')
    parser_reserve_book.add_argument('member_id', type=int, help='ID пользователя')
    parser_reserve_book.add_argument('title', type=str, help='Название книги')
    parser_reserve_book.set_defaults(func=reserve_book)

    # Cancel reservation
    parser_cancel_reservation = subparsers.add_parser('cancel_reservation', help='Отменить бронирование книги')
    parser_cancel_reservation.add_argument('member_id', type=int, help='ID пользователя')
    parser_cancel_reservation.add_argument('title', type=str, help='Название книги')
    parser_cancel_reservation.set_defaults(func=cancel_reservation)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
