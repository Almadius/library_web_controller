import tkinter as tk
from tkinter import messagebox, ttk
from library.book import Book
from library.member import Member
from library.library import Library
from datetime import datetime

library = Library()

def add_book():
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()
    copies = entry_copies.get()
    if title and author and year and copies:
        try:
            year = int(year)
            copies = int(copies)
            book = Book(title, author, year, copies)
            library.add_book(book)
            messagebox.showinfo("Успех", f"Книга '{title}' добавлена в библиотеку.")
        except ValueError:
            messagebox.showerror("Ошибка", "Год и количество экземпляров должны быть числом.")
    else:
        messagebox.showerror("Ошибка", "Заполните все поля.")

def remove_book():
    title = entry_remove_title.get()
    if title:
        if library.remove_book(title):
            messagebox.showinfo("Успех", f"Книга '{title}' удалена из библиотеки.")
        else:
            messagebox.showerror("Ошибка", f"Книга '{title}' не найдена в библиотеке.")
    else:
        messagebox.showerror("Ошибка", "Заполните название книги.")

def find_book():
    title = entry_find_title.get()
    if title:
        book = library.find_book(title)
        if book:
            messagebox.showinfo("Найдена книга", str(book))
        else:
            messagebox.showerror("Ошибка", f"Книга '{title}' не найдена.")
    else:
        messagebox.showerror("Ошибка", "Заполните название книги.")

def register_member():
    name = entry_member_name.get()
    member_id = entry_member_id.get()
    if name and member_id:
        try:
            member_id = int(member_id)
            member = Member(name, member_id)
            library.register_member(member)
            messagebox.showinfo("Успех", f"Пользователь '{name}' с ID {member_id} зарегистрирован в библиотеке.")
        except ValueError:
            messagebox.showerror("Ошибка", "ID пользователя должно быть числом.")
    else:
        messagebox.showerror("Ошибка", "Заполните все поля.")

def remove_member():
    member_id = entry_remove_member_id.get()
    if member_id:
        try:
            member_id = int(member_id)
            if library.remove_member(member_id):
                messagebox.showinfo("Успех", f"Пользователь с ID {member_id} удален из библиотеки.")
            else:
                messagebox.showerror("Ошибка", f"Пользователь с ID {member_id} не найден.")
        except ValueError:
            messagebox.showerror("Ошибка", "ID пользователя должно быть числом.")
    else:
        messagebox.showerror("Ошибка", "Заполните ID пользователя.")

def find_member():
    member_id = entry_find_member_id.get()
    if member_id:
        try:
            member_id = int(member_id)
            member = library.find_member(member_id)
            if member:
                messagebox.showinfo("Найден Пользователь", str(member))
            else:
                messagebox.showerror("Ошибка", f"Пользователь с ID {member_id} не найден.")
        except ValueError:
            messagebox.showerror("Ошибка", "ID пользователя должно быть числом.")
    else:
        messagebox.showerror("Ошибка", "Заполните ID пользователя.")

def borrow_book():
    member_id = entry_borrow_member_id.get()
    title = entry_borrow_title.get()
    if member_id and title:
        try:
            member_id = int(member_id)
            library.borrow_book(member_id, title)
            messagebox.showinfo("Успех", f"Книга '{title}' выдана пользователю с ID {member_id}.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    else:
        messagebox.showerror("Ошибка", "Заполните все поля.")

def return_book():
    member_id = entry_return_member_id.get()
    title = entry_return_title.get()
    if member_id and title:
        try:
            member_id = int(member_id)
            library.return_book(member_id, title)
            messagebox.showinfo("Успех", f"Книга '{title}' возвращена пользователем с ID {member_id}.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    else:
        messagebox.showerror("Ошибка", "Заполните все поля.")

def reserve_book():
    member_id = entry_reserve_member_id.get()
    title = entry_reserve_title.get()
    if member_id and title:
        try:
            member_id = int(member_id)
            library.reserve_book(member_id, title)
            messagebox.showinfo("Успех", f"Книга '{title}' забронирована пользователем с ID {member_id}.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    else:
        messagebox.showerror("Ошибка", "Заполните все поля.")

def cancel_reservation():
    member_id = entry_cancel_reservation_member_id.get()
    title = entry_cancel_reservation_title.get()
    if member_id and title:
        try:
            member_id = int(member_id)
            library.cancel_reservation(member_id, title)
            messagebox.showinfo("Успех", f"Бронирование книги '{title}' пользователем с ID {member_id} отменено.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    else:
        messagebox.showerror("Ошибка", "Заполните все поля.")

app = tk.Tk()
app.title("Library Management System")

notebook = ttk.Notebook(app)
notebook.pack(pady=10, expand=True)

# Вкладка для добавления книги
tab_add_book = ttk.Frame(notebook)
notebook.add(tab_add_book, text="Добавить книгу")

label_title = tk.Label(tab_add_book, text="Название книги")
label_title.grid(row=0, column=0)
entry_title = tk.Entry(tab_add_book)
entry_title.grid(row=0, column=1)

label_author = tk.Label(tab_add_book, text="Автор")
label_author.grid(row=1, column=0)
entry_author = tk.Entry(tab_add_book)
entry_author.grid(row=1, column=1)

label_year = tk.Label(tab_add_book, text="Год издания")
label_year.grid(row=2, column=0)
entry_year = tk.Entry(tab_add_book)
entry_year.grid(row=2, column=1)

label_copies = tk.Label(tab_add_book, text="Количество экземпляров")
label_copies.grid(row=3, column=0)
entry_copies = tk.Entry(tab_add_book)
entry_copies.grid(row=3, column=1)

button_add_book = tk.Button(tab_add_book, text="Добавить книгу", command=add_book)
button_add_book.grid(row=4, columnspan=2)

# Вкладка для удаления книги
tab_remove_book = ttk.Frame(notebook)
notebook.add(tab_remove_book, text="Удалить книгу")

label_remove_title = tk.Label(tab_remove_book, text="Название книги")
label_remove_title.grid(row=0, column=0)
entry_remove_title = tk.Entry(tab_remove_book)
entry_remove_title.grid(row=0, column=1)

button_remove_book = tk.Button(tab_remove_book, text="Удалить книгу", command=remove_book)
button_remove_book.grid(row=1, columnspan=2)

# Вкладка для поиска книги
tab_find_book = ttk.Frame(notebook)
notebook.add(tab_find_book, text="Найти книгу")

label_find_title = tk.Label(tab_find_book, text="Название книги")
label_find_title.grid(row=0, column=0)
entry_find_title = tk.Entry(tab_find_book)
entry_find_title.grid(row=0, column=1)

button_find_book = tk.Button(tab_find_book, text="Найти книгу", command=find_book)
button_find_book.grid(row=1, columnspan=2)

# Вкладка для регистрации пользователя
tab_register_member = ttk.Frame(notebook)
notebook.add(tab_register_member, text="Зарегистрировать пользователя")

label_member_name = tk.Label(tab_register_member, text="Имя пользователя")
label_member_name.grid(row=0, column=0)
entry_member_name = tk.Entry(tab_register_member)
entry_member_name.grid(row=0, column=1)

label_member_id = tk.Label(tab_register_member, text="ID пользователя")
label_member_id.grid(row=1, column=0)
entry_member_id = tk.Entry(tab_register_member)
entry_member_id.grid(row=1, column=1)

button_register_member = tk.Button(tab_register_member, text="Зарегистрировать пользователя", command=register_member)
button_register_member.grid(row=2, columnspan=2)

# Вкладка для удаления пользователя
tab_remove_member = ttk.Frame(notebook)
notebook.add(tab_remove_member, text="Удалить пользователя")

label_remove_member_id = tk.Label(tab_remove_member, text="ID пользователя")
label_remove_member_id.grid(row=0, column=0)
entry_remove_member_id = tk.Entry(tab_remove_member)
entry_remove_member_id.grid(row=0, column=1)

button_remove_member = tk.Button(tab_remove_member, text="Удалить пользователя", command=remove_member)
button_remove_member.grid(row=1, columnspan=2)

# Вкладка для поиска пользователя
tab_find_member = ttk.Frame(notebook)
notebook.add(tab_find_member, text="Найти пользователя")

label_find_member_id = tk.Label(tab_find_member, text="ID пользователя")
label_find_member_id.grid(row=0, column=0)
entry_find_member_id = tk.Entry(tab_find_member)
entry_find_member_id.grid(row=0, column=1)

button_find_member = tk.Button(tab_find_member, text="Найти пользователя", command=find_member)
button_find_member.grid(row=1, columnspan=2)

# Вкладка для проката книги
tab_borrow_book = ttk.Frame(notebook)
notebook.add(tab_borrow_book, text="Взять книгу на прокат")

label_borrow_member_id = tk.Label(tab_borrow_book, text="ID пользователя")
label_borrow_member_id.grid(row=0, column=0)
entry_borrow_member_id = tk.Entry(tab_borrow_book)
entry_borrow_member_id.grid(row=0, column=1)

label_borrow_title = tk.Label(tab_borrow_book, text="Название книги")
label_borrow_title.grid(row=1, column=0)
entry_borrow_title = tk.Entry(tab_borrow_book)
entry_borrow_title.grid(row=1, column=1)

button_borrow_book = tk.Button(tab_borrow_book, text="Взять книгу на прокат", command=borrow_book)
button_borrow_book.grid(row=2, columnspan=2)

# Вкладка для возврата книги
tab_return_book = ttk.Frame(notebook)
notebook.add(tab_return_book, text="Вернуть книгу")

label_return_member_id = tk.Label(tab_return_book, text="ID пользователя")
label_return_member_id.grid(row=0, column=0)
entry_return_member_id = tk.Entry(tab_return_book)
entry_return_member_id.grid(row=0, column=1)

label_return_title = tk.Label(tab_return_book, text="Название книги")
label_return_title.grid(row=1, column=0)
entry_return_title = tk.Entry(tab_return_book)
entry_return_title.grid(row=1, column=1)

button_return_book = tk.Button(tab_return_book, text="Вернуть книгу", command=return_book)
button_return_book.grid(row=2, columnspan=2)

# Вкладка для бронирования книги
tab_reserve_book = ttk.Frame(notebook)
notebook.add(tab_reserve_book, text="Забронировать книгу")

label_reserve_member_id = tk.Label(tab_reserve_book, text="ID пользователя")
label_reserve_member_id.grid(row=0, column=0)
entry_reserve_member_id = tk.Entry(tab_reserve_book)
entry_reserve_member_id.grid(row=0, column=1)

label_reserve_title = tk.Label(tab_reserve_book, text="Название книги")
label_reserve_title.grid(row=1, column=0)
entry_reserve_title = tk.Entry(tab_reserve_book)
entry_reserve_title.grid(row=1, column=1)

button_reserve_book = tk.Button(tab_reserve_book, text="Забронировать книгу", command=reserve_book)
button_reserve_book.grid(row=2, columnspan=2)

# Вкладка для отмены бронирования книги
tab_cancel_reservation = ttk.Frame(notebook)
notebook.add(tab_cancel_reservation, text="Отменить бронирование книги")

label_cancel_reservation_member_id = tk.Label(tab_cancel_reservation, text="ID пользователя")
label_cancel_reservation_member_id.grid(row=0, column=0)
entry_cancel_reservation_member_id = tk.Entry(tab_cancel_reservation)
entry_cancel_reservation_member_id.grid(row=0, column=1)

label_cancel_reservation_title = tk.Label(tab_cancel_reservation, text="Название книги")
label_cancel_reservation_title.grid(row=1, column=0)
entry_cancel_reservation_title = tk.Entry(tab_cancel_reservation)
entry_cancel_reservation_title.grid(row=1, column=1)

button_cancel_reservation = tk.Button(tab_cancel_reservation, text="Отменить бронирование", command=cancel_reservation)
button_cancel_reservation.grid(row=2, columnspan=2)

app.mainloop()
