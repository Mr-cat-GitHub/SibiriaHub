from PyQt6.QtWidgets import QApplication
import sys
from widgets.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show_auth_interface()  # Сначала показываем аутентификацию
window.show()
sys.exit(app.exec())