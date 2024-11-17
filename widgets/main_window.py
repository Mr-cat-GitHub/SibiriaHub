import csv

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QScrollArea, QHBoxLayout, QLineEdit, \
    QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
from models import create_user_session, Book
from widgets.auth_widget import AuthWidget
from widgets.book_card_widget import BookCardWidget
from widgets.input_form_widget import InputFormWidget
from widgets.profile_widget import ProfileWidget
from widgets.file_operations_widget import FileOperationsWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user = None
        self.load_stylesheet()
        self.init_auth_interface()

    def init_auth_interface(self):
        """Отображает интерфейс авторизации."""
        self.auth_widget = AuthWidget(self)
        self.setCentralWidget(self.auth_widget)

    def init_main_interface(self):
        """Инициализирует основной интерфейс после авторизации."""
        self.setWindowTitle("Sibir Hub")
        self.setGeometry(100, 100, 800, 600)

        # Основной контейнер
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)

        # Поле поиска книг
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск книг по названию, автору или году")
        search_button = QPushButton("Поиск")
        search_button.clicked.connect(self.search_books)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        # Кнопка для добавления книг
        self.form_widget = InputFormWidget(self)

        # Кнопки профиля и экспорта
        buttons_layout = QHBoxLayout()
        profile_button = QPushButton("Профиль")
        profile_button.clicked.connect(self.show_profile)

        buttons_layout.addWidget(profile_button)

        # Область для карточек книг
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.book_container = QWidget()
        self.book_layout = QVBoxLayout(self.book_container)
        self.scroll_area.setWidget(self.book_container)

        # Добавляем виджеты в основной интерфейс
        self.layout.addLayout(search_layout)
        self.layout.addWidget(self.form_widget)
        self.layout.addLayout(buttons_layout)
        self.layout.addWidget(self.scroll_area)
        self.setCentralWidget(self.container)

        self.load_books()

    def load_books(self):
        """Загружает книги текущего пользователя."""
        if not self.user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не авторизован.")
            return

        session = create_user_session(self.user.username)
        books = session.query(Book).filter_by(user_id=self.user.id).all()
        for book in books:
            self.add_book_card(book)

    def add_book_card(self, book):
        """Добавляет карточку книги в интерфейс."""
        card = BookCardWidget(book, self)
        self.book_layout.addWidget(card)

    def search_books(self):
        """Поиск книг и отображение результатов."""
        session = create_user_session(self.user.username)
        search_text = self.search_input.text().strip().lower()
        self.clear_cards()
        books = session.query(Book).filter(
            (Book.title.ilike(f"%{search_text}%")) |
            (Book.author.ilike(f"%{search_text}%")) |
            (Book.year.ilike(f"%{search_text}%"))
        ).all()
        for book in books:
            self.add_book_card(book)

    def clear_cards(self):
        """Удаляет все карточки из интерфейса."""
        while self.book_layout.count():
            widget = self.book_layout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

    def show_profile(self):
        """Открывает виджет профиля."""
        profile_widget = ProfileWidget(self.user, self)
        self.setCentralWidget(profile_widget)

    def load_main_interface(self, user):
        """Загружает основной интерфейс после авторизации."""
        self.user = user
        self.init_main_interface()

    def refresh_cards(self):
        """Обновляет карточки книг, загружая их заново из базы данных."""
        if not self.user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не авторизован.")
            return

        session = create_user_session(self.user.username)

        # Очищаем текущие карточки
        while self.book_layout.count():
            widget = self.book_layout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

        # Загружаем книги заново
        books = session.query(Book).filter_by(user_id=self.user.id).all()
        for book in books:
            self.add_book_card(book)

    def go_back(self):
        """Возвращает пользователя к основному интерфейсу."""
        self.parent.init_main_interface()  # Замените init_ui на init_main_interface

    def load_stylesheet(self):
        """Загружает CSS из файла и применяет к приложению."""
        try:
            with open("style.css", "r") as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            print("CSS файл не найден.")
