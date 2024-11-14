from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QFont
from models import Book, create_user_session


class BookCardWidget(QWidget):
    def __init__(self, book, parent=None):
        super().__init__(parent)
        self.book = book
        self.parent = parent

        # Основной макет карточки
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Стили для карточки
        self.setStyleSheet("""
            QWidget {
                background-color: #2A2A2E;
                border-radius: 10px;
                border: 1px solid #3E3E42;
                padding: 10px;
                width: 25px;  /* Фиксированная ширина */
                height: 25px; /* Фиксированная высота */
            }
            QLabel {
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3A3A3F;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 12px;
                font-size: 12px;
                width: 25px; /* Ширина кнопок */
            }
            QPushButton:hover {
                background-color: #4A4A4F;
            }
        """)

        # Заголовок книги
        title_label = QLabel(f"Title: {book.title}")
        title_label.setFont(QFont("Arial", 12))
        layout.addWidget(title_label)

        # Автор
        author_label = QLabel(f"Author: {book.author}")
        layout.addWidget(author_label)

        # Год издания
        year_label = QLabel(f"Year: {book.year}")
        layout.addWidget(year_label)

        # Кнопки управления
        button_layout = QHBoxLayout()
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit_book)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_book)

        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def edit_book(self):
        """Редактирование книги."""
        self.parent.form_widget.populate_form(self.book)

    def delete_book(self):
        """Удаление книги."""
        # Создаем сессию для текущего пользователя
        session = create_user_session(self.parent.user.username)

        reply = QMessageBox.question(
            self, "Confirm Deletion",
            "Are you sure you want to delete this book?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            # Повторно загружаем объект из новой сессии
            book = session.query(Book).get(self.book.id)
            if book:
                session.delete(book)
                session.commit()
                self.parent.refresh_cards()  # Обновляем карточки после удаления
