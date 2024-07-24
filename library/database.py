import sqlite3

class Database:
    def __init__(self, db_name="library.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    copies INTEGER NOT NULL
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password_hash TEXT NOT NULL
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS borrowed_books (
                    member_id INTEGER,
                    book_id INTEGER,
                    due_date TEXT,
                    FOREIGN KEY(member_id) REFERENCES members(id),
                    FOREIGN KEY(book_id) REFERENCES books(id),
                    PRIMARY KEY(member_id, book_id)
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    member_id INTEGER,
                    book_id INTEGER,
                    reservation_date TEXT,
                    FOREIGN KEY(member_id) REFERENCES members(id),
                    FOREIGN KEY(book_id) REFERENCES books(id),
                    PRIMARY KEY(member_id, book_id)
                )
            """)

    def execute(self, query, params=()):
        with self.connection:
            return self.connection.execute(query, params)

    def fetchall(self, query, params=()):
        with self.connection:
            cursor = self.connection.execute(query, params)
            return cursor.fetchall()

    def fetchone(self, query, params=()):
        with self.connection:
            cursor = self.connection.execute(query, params)
            return cursor.fetchone()

    def close(self):
        self.connection.close()