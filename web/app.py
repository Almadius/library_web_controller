import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from library.book import Book
from library.member import Member
from library.library import Library

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

library = Library()

class User(UserMixin):
    def __init__(self, member):
        self.id = member.member_id
        self.name = member.name
        self.email = member.email

@login_manager.user_loader
def load_user(user_id):
    member_data = library.db.fetchone("SELECT * FROM members WHERE id = ?", (user_id,))
    if member_data:
        return User(Member(member_data[1], member_data[0], member_data[2], member_data[3]))
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Attempting login with email: {email} and password: {password}")  # Отладка

        member_data = library.db.fetchone("SELECT * FROM members WHERE email = ?", (email,))
        if member_data:
            print(f"User found: {member_data}")  # Отладка
            member = Member(member_data[1], email=member_data[2], password=None, password_hash=member_data[3], member_id=member_data[0])
            if member.check_password(password):
                print("Password check passed")  # Отладка
                user = User(member)
                login_user(user)
                return redirect(url_for('index'))
            else:
                print("Password check failed")  # Отладка
                flash('Invalid password.', 'danger')
        else:
            print("User not found")  # Отладка
            flash('Email not found.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if name and email and password:
            member = Member(name, email, password)
            library.register_member(member)
            flash(f"Пользователь '{name}' зарегистрирован в библиотеке.", 'success')
            return redirect(url_for('login'))
        else:
            flash("Заполните все поля.", 'danger')
    return render_template('register.html')

@app.route('/books')
@login_required
def show_books():
    books = library.db.fetchall("SELECT * FROM books")
    return render_template('books.html', books=books)

@app.route('/members')
@login_required
def show_members():
    members = library.db.fetchall("SELECT * FROM members")
    return render_template('members.html', members=members)

@app.route('/add_book')
@login_required
def show_add_book():
    return render_template('add_book.html')

@app.route('/add_book', methods=['POST'])
@login_required
def add_book():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    copies = request.form['copies']
    if title and author and year and copies:
        try:
            year = int(year)
            copies = int(copies)
            book = Book(title, author, year, copies)
            library.add_book(book)
            flash(f"Книга '{title}' добавлена в библиотеку.", 'success')
        except ValueError:
            flash("Год и количество экземпляров должны быть числом.", 'danger')
    else:
        flash("Заполните все поля.", 'danger')
    return redirect(url_for('show_add_book'))

@app.route('/register_member')
@login_required
def show_register_member():
    return render_template('register_member.html')

@app.route('/register_member', methods=['POST'])
@login_required
def register_member():
    name = request.form['name']
    member_id = request.form['member_id']
    email = request.form['email']
    password = request.form['password']
    if name and member_id and email and password:
        try:
            member_id = int(member_id)
            member = Member(name, member_id, email, password)
            library.register_member(member)
            flash(f"Пользователь '{name}' с ID {member_id} зарегистрирован в библиотеке.", 'success')
        except ValueError:
            flash("ID Пользователя должно быть числом.", 'danger')
    else:
        flash("Заполните все поля.", 'danger')
    return redirect(url_for('show_register_member'))

@app.route('/borrow_book')
@login_required
def show_borrow_book():
    return render_template('borrow_book.html')

@app.route('/borrow_book', methods=['POST'])
@login_required
def borrow_book():
    member_id = request.form['member_id']
    title = request.form['title']
    if member_id and title:
        try:
            member_id = int(member_id)
            library.borrow_book(member_id, title)
            flash(f"Книга '{title}' выдана пользователю с ID {member_id}.", 'success')
        except ValueError as e:
            flash(str(e), 'danger')
    else:
        flash("Заполните все поля.", 'danger')
    return redirect(url_for('show_borrow_book'))

@app.route('/return_book')
@login_required
def show_return_book():
    return render_template('return_book.html')

@app.route('/return_book', methods=['POST'])
@login_required
def return_book():
    member_id = request.form['member_id']
    title = request.form['title']
    if member_id and title:
        try:
            member_id = int(member_id)
            library.return_book(member_id, title)
            flash(f"Книга '{title}' возвращена пользователем с ID {member_id}.", 'success')
        except ValueError as e:
            flash(str(e), 'danger')
    else:
        flash("Заполните все поля.", 'danger')
    return redirect(url_for('show_return_book'))

@app.route('/reserve_book')
@login_required
def show_reserve_book():
    return render_template('reserve_book.html')

@app.route('/reserve_book', methods=['POST'])
@login_required
def reserve_book():
    member_id = request.form['member_id']
    title = request.form['title']
    if member_id and title:
        try:
            member_id = int(member_id)
            library.reserve_book(member_id, title)
            flash(f"Книга '{title}' забронирована пользователем с ID {member_id}.", 'success')
        except ValueError as e:
            flash(str(e), 'danger')
    else:
        flash("Заполните все поля.", 'danger')
    return redirect(url_for('show_reserve_book'))

@app.route('/cancel_reservation')
@login_required
def show_cancel_reservation():
    return render_template('cancel_reservation.html')

@app.route('/cancel_reservation', methods=['POST'])
@login_required
def cancel_reservation():
    member_id = request.form['member_id']
    title = request.form['title']
    if member_id and title:
        try:
            member_id = int(member_id)
            library.cancel_reservation(member_id, title)
            flash(f"Бронирование книги '{title}' пользователем с ID {member_id} отменено.", 'success')
        except ValueError as e:
            flash(str(e), 'danger')
    else:
        flash("Заполните все поля.", 'danger')
    return redirect(url_for('show_cancel_reservation'))

if __name__ == '__main__':
    app.run(debug=True)
