import sys
from PyQt6.QtWidgets import QApplication
from widgets.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())
