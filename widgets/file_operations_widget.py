import csv

from models import create_user_session, Book


class FileOperationsWidget:
    def __init__(self, user):
        self.user = user

    def export_to_csv(self):
        """Экспортирует книги пользователя в CSV."""
        session = create_user_session(self.user.username)
        books = session.query(Book).filter_by(user_id=self.user.id).all()

        with open(f"{self.user.username}_books.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Author", "Year"])
            for book in books:
                writer.writerow([book.title, book.author, book.year])
