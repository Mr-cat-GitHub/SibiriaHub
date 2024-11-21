import csv
import os

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QScrollArea, QHBoxLayout, QLineEdit, \
    QMessageBox, QFileDialog
from PyQt6.QtCore import Qt, QSettings
from models import create_user_session, Book
from widgets.auth_widget import AuthWidget
from widgets.book_card_widget import BookCardWidget
from widgets.input_form_widget import InputFormWidget
from widgets.profile_widget import ProfileWidget
from widgets.theme_selector_widget import ThemeSelectorWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user = None
        # self.load_css()
        self.apply_saved_theme()
        self.init_auth_interface()
        self.theme_selector_widget = None  # Инициализация атрибута

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
        self.search_input.setPlaceholderText("Search")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_books)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        # Кнопка для добавления книг
        self.form_widget = InputFormWidget(self)

        # Кнопки профиля и выбора темы
        buttons_layout = QHBoxLayout()
        profile_button = QPushButton("Profile")
        profile_button.clicked.connect(self.show_profile)

        theme_button = QPushButton("Theme")
        theme_button.clicked.connect(self.open_theme_selector)

        # Устанавливаем кнопкам одинаковый размер
        buttons_layout.addWidget(profile_button, alignment=Qt.AlignmentFlag.AlignLeft)
        buttons_layout.addWidget(theme_button, alignment=Qt.AlignmentFlag.AlignRight)

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
            QMessageBox.warning(self, "Error")
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
        self.close_theme_selector()  # Закрыть селектор тем, если он открыт
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

    def load_css(self, file_name):
        """Загружает файл CSS и применяет его к приложению."""
        if not os.path.exists(file_name):
            print(f"Ошибка: файл {file_name} не найден.")
            return

        try:
            with open(file_name, "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"Ошибка загрузки CSS: {e}")

    def open_theme_selector(self):
        """Открывает виджет выбора темы."""
        if not hasattr(self, "theme_selector_widget") or self.theme_selector_widget is None:
            self.theme_selector_widget = ThemeSelectorWidget(self)
            self.theme_selector_widget.show()
        else:
            self.theme_selector_widget.show()

    def apply_saved_theme(self):
        """Применяет сохранённую тему при запуске."""
        settings = QSettings("SibirHub", "ThemeSettings")
        saved_theme = settings.value("theme", "dark")  # По умолчанию тёмная тема
        theme_files = {
            "dark": "css/dark_theme.css",
            "light": "css/light_theme.css",
            "pink_light": "css/pink_light_theme.css",
            "twilight": "css/twilight_theme.css",
        }

        if saved_theme in theme_files:
            self.load_css(theme_files[saved_theme])

    def close_theme_selector(self):
        """Закрывает виджет выбора темы, если он открыт."""
        if hasattr(self, "theme_selector_widget") and self.theme_selector_widget is not None:
            self.theme_selector_widget.close()
            self.theme_selector_widget.deleteLater()
            self.theme_selector_widget = None


