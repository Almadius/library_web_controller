class Book:
    """Класс, представляющий книгу в библиотеке."""

    def __init__(self, title, author, year, copies=1):
        """
        Инициализирует объект книги.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :param copies: Количество экземпляров книги.
        """
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies

    def __str__(self):
        """
        Возвращает строковое представление книги.

        :return: Строковое представление книги.
        """
        return f"{self.title} by {self.author} ({self.year}) - {self.copies} copies"
