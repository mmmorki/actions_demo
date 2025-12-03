class Book:
    def __init__(self, title, author, year):
        self.__title = title
        self.__author = author
        self.__year = year
        self.__available = True

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_year(self):
        return self.__year

    def is_available(self):
        return self.__available

    def mark_as_taken(self):
        self.__available = False

    def mark_as_returned(self):
        self.__available = True

    def __str__(self):
        status = "доступна" if self.__available else "выдана"
        return f"{self.__title} ({self.__author}, {self.__year}) - {status}"


class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition):
        super().__init__(title, author, year)
        self.pages = pages
        self.condition = condition

    def repair(self):
        if self.condition == "плохая":
            self.condition = "хорошая"
        elif self.condition == "хорошая":
            self.condition = "новая"

class EBook(Book):
    def __init__(self, title, author, year, file_size, format):
        super().__init__(title, author, year)
        self.file_size = file_size
        self.format = format

    def download(self):
        print(f"Книга {self.get_title()} загружается...")

    def __str__(self):
        base = super().__str__()
        return f"{base} | Размер: {self.file_size}MB, Формат: {self.format}"


class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []

    def borrow(self, book):
        if book.is_available():
            self.__borrowed_books.append(book)
            book.mark_as_taken()
            print(f"{self.name} взял(а) книгу: {book.get_title()}")
            return True
        else:
            print(f"Книга {book.get_title()} недоступна")
            return False

    def return_book(self, book):
        if book in self.__borrowed_books:
            self.__borrowed_books.remove(book)
            book.mark_as_returned()
            print(f"{self.name} вернул(а) книгу: {book.get_title()}")
            return True
        else:
            print(f"Эта книга не была взята {self.name}")
            return False

    def show_books(self):
        if not self.__borrowed_books:
            print(f"У {self.name} нет взятых книг")
        else:
            print(f"Книги {self.name}:")
            for book in self.__borrowed_books:
                print(f"  - {book.get_title()}")

    def get_borrowed_books(self):
        return self.__borrowed_books.copy()


class Librarian(User):
    def add_book(self, library, book):
        library.add_book(book)

    def remove_book(self, library, title):
        library.remove_book(title)

    def register_user(self, library, user):
        library.add_user(user)


class Library:
    def __init__(self):
        self.__books = []
        self.__users = []

    def add_book(self, book):
        self.__books.append(book)

    def remove_book(self, title):
        for i in range(len(self.__books)):
            book = self.__books[i]
            if book.get_title() == title:
                self.__books.pop(i)
                return True
        return False

    def add_user(self, user):
        if user not in self.__users:
            self.__users.append(user)

    def find_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                return book
        return None

    def show_all_books(self):
        if not self.__books:
            print("Библиотека пуста")
        else:
            print("Все книги в библиотеке:")
            for book in self.__books:
                print(f"  - {book}")

    def show_available_books(self):
        available = [book for book in self.__books if book.is_available()]
        if not available:
            print("Нет доступных книг")
        else:
            print("Доступные книги:")
            for book in available:
                print(f"  - {book}")

    def lend_book(self, title, user_name):
        book = self.find_book(title)
        user = None
        for u in self.__users:
            if u.name == user_name:
                user = u
                break

        if book is None:
            print(f"Книга '{title}' не найдена")
            return False
        if user is None:
            print(f"Пользователь '{user_name}' не найден")
            return False

        return user.borrow(book)

    def return_book(self, title, user_name):
        book = self.find_book(title)
        user = None
        for u in self.__users:
            if u.name == user_name:
                user = u
                break

        if book is None:
            print(f"Книга '{title}' не найдена")
            return False
        if user is None:
            print(f"Пользователь '{user_name}' не найден")
            return False

        return user.return_book(book)


lib = Library()

b1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
b2 = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
b3 = PrintedBook("Преступление и наказание", "Достоевский", 1866, 480,
"плохая")

user1 = User("Анна")
librarian = Librarian("Мария")

librarian.add_book(lib, b1)
librarian.add_book(lib, b2)
librarian.add_book(lib, b3)

librarian.register_user(lib, user1)

lib.lend_book("Война и мир", "Анна")

user1.show_books()

lib.return_book("Война и мир", "Анна")

b2.download()

b3.repair()

print(b3)
print(b2)
print(b1)
