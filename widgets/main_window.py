from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QScrollArea, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont
from widgets.book_card_widget import BookCardWidget
from widgets.input_form_widget import InputFormWidget
from models import Book, create_user_session
from widgets.auth_widget import AuthWidget
from widgets.profile_widget import ProfileWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = InputFormWidget(self)
        self.setWindowTitle("Siberia Hub - Book Cards")
        self.setGeometry(100, 100, 800, 600)
        self.user = None
        self.show_auth_interface()

    def show_auth_interface(self):
        self.auth_widget = AuthWidget(self)
        self.setCentralWidget(self.auth_widget)

    def load_main_interface(self, user):
        self.user = user
        self.init_main_interface()

    def init_main_interface(self):
        # Создаем основной виджет и макет
        container = QWidget()
        main_layout = QVBoxLayout()

        # Устанавливаем тему
        self.set_dark_theme()

        # Виджет прокрутки для карточек книг
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.card_container = QWidget()
        self.card_layout = QVBoxLayout()
        self.card_container.setLayout(self.card_layout)
        self.scroll_area.setWidget(self.card_container)
        main_layout.addWidget(self.scroll_area)

        # Поле поиска
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title, author, or year")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_books)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        # Добавляем форму и кнопку для добавления
        self.form_widget = InputFormWidget(self)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.form_widget)

        # Устанавливаем основной макет
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Загрузка данных книг
        self.load_books()

    def set_dark_theme(self):
        self.dark_theme = """
            QMainWindow {
                background-color: #2A2A2E;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #444;
                border-radius: 5px;
                font-size: 14px;
                background-color: #444;
                color: white;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #3A3A3F;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4A4A4F;
            }
            QTableWidget {
                background-color: #333;
                border: 1px solid #555;
                font-size: 14px;
                color: white;
            }
        """
        self.setStyleSheet(self.dark_theme)

    def load_books(self):
        """Загружает все книги из базы данных и отображает их как карточки."""
        session = create_user_session(self.user.username)  # Создаем сессию для текущего пользователя
        books = session.query(Book).all()
        for book in books:
            self.add_book_card(book)

    def add_book_card(self, book):
        """Добавляет карточку книги в интерфейс."""
        card = BookCardWidget(book, self)
        self.card_layout.addWidget(card)

    def delete_book_card(self, card_widget):
        """Удаляет карточку книги из интерфейса и базы данных."""
        session = create_user_session(self.user.username)  # Создаем сессию для текущего пользователя
        book = card_widget.book
        session.delete(book)
        session.commit()
        card_widget.setParent(None)  # Удаление виджета из макета

    def search_books(self):
        """Поиск книг и отображение результатов как карточек."""
        session = create_user_session(self.user.username)  # Создаем сессию для текущего пользователя
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
        for i in reversed(range(self.card_layout.count())):
            widget = self.card_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def refresh_cards(self):
        """Обновляет отображение карточек книг."""
        # Создаем сессию для текущего пользователя
        session = create_user_session(self.user.username)

        # Очистить существующие карточки
        for i in reversed(range(self.card_layout.count())):
            widget = self.card_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Загрузить книги из базы данных
        books = session.query(Book).all()
        for book in books:
            card = BookCardWidget(book, parent=self)
            self.card_layout.addWidget(card)

    def edit_book(self):
        """Функция редактирования книги."""
        self.parent.form_widget.populate_form(self.book)
