from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog, QMessageBox
import csv
from models import Book, session


class FileOperationsWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QHBoxLayout()

        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)
        import_button = QPushButton("Import from CSV")
        import_button.clicked.connect(self.import_from_csv)

        layout.addWidget(export_button)
        layout.addWidget(import_button)
        self.setLayout(layout)

    def export_to_csv(self):
        """Экспортирует данные в CSV файл."""
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV files (*.csv)")
        if path:
            with open(path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Title", "Author", "Year"])
                for row in range(self.table_widget.rowCount()):
                    row_data = [
                        self.table_widget.item(row, col).text() for col in range(self.table_widget.columnCount())
                    ]
                    writer.writerow(row_data)
            QMessageBox.information(self, "Export Complete", "Data exported to CSV file successfully.")

    def import_from_csv(self):
        """Импортирует данные из CSV файла."""
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV files (*.csv)")
        if path:
            with open(path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Пропуск заголовка
                for row in reader:
                    if len(row) == 4:
                        new_book = Book(title=row[1], author=row[2], year=int(row[3]))
                        session.add(new_book)
                        session.commit()
                        self.table_widget.add_table_row(new_book)
            QMessageBox.information(self, "Import Complete", "Data imported from CSV file successfully.")
