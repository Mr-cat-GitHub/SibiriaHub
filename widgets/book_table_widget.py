# widgets/book_table_widget.py
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from models import Book, session


class BookTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(0, 4, parent)
        self.setHorizontalHeaderLabels(["ID", "Title", "Author", "Year"])
        self.parent = parent
        self.load_data()

    def load_data(self):
        """Загружает данные из базы и отображает их в таблице."""
        self.setRowCount(0)
        books = session.query(Book).all()
        for book in books:
            self.add_table_row(book)

    def add_table_row(self, book):
        """Добавляет строку в таблицу с данными книги."""
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.setItem(row_position, 0, QTableWidgetItem(str(book.id)))
        self.setItem(row_position, 1, QTableWidgetItem(book.title))
        self.setItem(row_position, 2, QTableWidgetItem(book.author))
        self.setItem(row_position, 3, QTableWidgetItem(str(book.year)))

    def search_books(self, search_text):
        """Поиск книг по названию, автору или году."""
        self.setRowCount(0)
        books = session.query(Book).filter(
            (Book.title.ilike(f'%{search_text}%')) |
            (Book.author.ilike(f'%{search_text}%')) |
            (Book.year.ilike(f'%{search_text}%'))
        ).all()
        for book in books:
            self.add_table_row(book)

    def delete_book(self):
        """Удаление выбранной книги с подтверждением."""
        selected_row = self.currentRow()
        if selected_row >= 0:
            reply = QMessageBox.question(
                self, "Confirm Deletion",
                "Are you sure you want to delete this book?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                book_id = int(self.item(selected_row, 0).text())
                book = session.query(Book).get(book_id)
                if book:
                    session.delete(book)
                    session.commit()
                self.removeRow(selected_row)
