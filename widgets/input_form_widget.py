from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models import Book, create_user_session


class InputFormWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_book = None  # Хранение текущей книги для редактирования
        layout = QVBoxLayout()

        # Поля ввода данных
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author")
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Year")

        # Кнопка для добавления или сохранения книги
        self.add_button = QPushButton("Add Book")
        self.add_button.clicked.connect(self.add_or_update_book)

        # Добавление виджетов в макет
        layout.addWidget(QLabel("Book Information"))
        layout.addWidget(self.title_input)
        layout.addWidget(self.author_input)
        layout.addWidget(self.year_input)
        layout.addWidget(self.add_button)
        self.setLayout(layout)

    def add_or_update_book(self):
        """Добавляет новую книгу или обновляет существующую."""
        if not self.parent or not self.parent.user:
            QMessageBox.warning(self, "Error", "User is not authenticated.")
            return

        # Создаем сессию для текущего пользователя
        session = create_user_session(self.parent.user.username)

        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        year = self.year_input.text().strip()

        if not title or not author or not year.isdigit():
            QMessageBox.warning(self, "Invalid Input", "All fields must be filled correctly.")
            return

        if self.current_book:
            # Обновление существующей книги
            self.current_book.title = title
            self.current_book.author = author
            self.current_book.year = int(year)
            session.commit()
            self.parent.refresh_cards()  # Обновление интерфейса
            self.reset_form()
        else:
            # Добавление новой книги с привязкой к текущему пользователю
            new_book = Book(title=title, author=author, year=int(year), user_id=self.parent.user.id)
            session.add(new_book)
            session.commit()
            self.parent.add_book_card(new_book)
            self.reset_form()

    def populate_form(self, book):
        """Заполняет форму данными книги для редактирования."""
        self.current_book = book
        self.title_input.setText(book.title)
        self.author_input.setText(book.author)
        self.year_input.setText(str(book.year))
        self.add_button.setText("Save Changes")

    def reset_form(self):
        """Сбрасывает форму в исходное состояние."""
        self.current_book = None
        self.title_input.clear()
        self.author_input.clear()
        self.year_input.clear()
        self.add_button.setText("Add Book")
