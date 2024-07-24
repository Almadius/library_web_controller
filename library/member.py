from werkzeug.security import generate_password_hash, check_password_hash

class Member:
    """Класс, представляющий пользователя библиотеки."""

    def __init__(self, name, email, password=None, member_id=None, password_hash=None):
        """
        Инициализирует объект пользователя библиотеки.

        :param name: Имя пользователя.
        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param member_id: ID пользователя.
        :param password_hash: Хеш пароля пользователя.
        """
        self.name = name
        self.email = email
        self.member_id = member_id
        if password_hash:
            self.password_hash = password_hash
        else:
            self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Проверяет пароль пользователя.

        :param password: Пароль для проверки.
        :return: True, если пароль верный, иначе False.
        """
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        """
        Возвращает строковое представление пользователя библиотеки.

        :return: Строковое представление пользователя библиотеки.
        """
        return f"{self.name} (ID: {self.member_id})"
