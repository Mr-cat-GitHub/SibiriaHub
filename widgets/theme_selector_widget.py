from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QSettings


class ThemeSelectorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор темы")
        self.setGeometry(200, 200, 300, 200)

        # Сохраняем настройки тем
        self.settings = QSettings("SibirHub", "ThemeSettings")

        # Инициализация интерфейса
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса виджета выбора темы."""
        layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel("Выберите тему:")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #FFA726;")  # Оранжевый заголовок
        layout.addWidget(title_label)

        # Кнопки выбора темы
        buttons_layout = QHBoxLayout()

        # Тёмная тема
        dark_theme_button = QPushButton("Тёмная тема")
        dark_theme_button.clicked.connect(lambda: self.apply_theme("dark"))
        buttons_layout.addWidget(dark_theme_button)

        # Светлая тема
        light_theme_button = QPushButton("Светлая тема")
        light_theme_button.clicked.connect(lambda: self.apply_theme("light"))
        buttons_layout.addWidget(light_theme_button)

        layout.addLayout(buttons_layout)

        # Кнопка возврата
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def apply_theme(self, theme):
        """Применяет выбранную тему и сохраняет её в настройках."""
        if theme == "dark":
            self.parent().set_dark_theme()
            self.settings.setValue("theme", "dark")  # Сохраняем выбор темы
            QMessageBox.information(self, "Тема", "Тёмная тема применена.")
        elif theme == "light":
            self.parent().set_light_theme()
            self.settings.setValue("theme", "light")  # Сохраняем выбор темы
            QMessageBox.information(self, "Тема", "Светлая тема применена.")

    def go_back(self):
        """Возвращает пользователя в главное окно."""
        self.parent().init_main_interface()
        self.close()
