from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QMessageBox


class ThemeSelectorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор темы")
        self.setGeometry(200, 200, 400, 300)  # Размер окна

        # Сохраняем настройки тем
        self.settings = QSettings("SibirHub", "ThemeSettings")

        # Инициализация интерфейса
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса виджета выбора темы."""
        layout = QVBoxLayout()
        layout.setSpacing(10)  # Отступы между элементами
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Выравнивание по верхнему краю

        # Заголовок
        title_label = QLabel("Select theme:")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Кнопки выбора темы
        buttons_layout = QVBoxLayout()

        themes = {
            "Dark theme": "dark",
            "Light theme": "light",
            "Pink-light theme": "pink_light",
            "Twilight theme": "twilight"
        }

        for label, theme_key in themes.items():
            button = QPushButton(label)
            button.setFixedHeight(40)  # Фиксированная высота кнопок
            button.clicked.connect(lambda checked, key=theme_key: self.apply_theme(key))
            buttons_layout.addWidget(button)

        layout.addLayout(buttons_layout)

        # Кнопка "Назад"
        back_button = QPushButton("Go back")
        back_button.setFixedHeight(40)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def apply_theme(self, theme):
        """Применяет выбранную тему и сохраняет её в настройках."""
        theme_files = {
            "dark": "css/dark_theme.css",
            "light": "css/light_theme.css",
            "pink_light": "css/pink_light_theme.css",
            "twilight": "css/twilight_theme.css",
        }

        if theme in theme_files:
            file_path = theme_files[theme]
            if self.parent() and hasattr(self.parent(), "load_css"):
                self.parent().load_css(file_path)
                self.settings.setValue("theme", theme)
                # QMessageBox.information(self, "Тема применена", f"Тема '{theme}' успешно применена.")
                print(f"Theme {theme} successfully applied")  # Отладочный вывод
            else:
                QMessageBox.warning(self, "Error", "Parent widget don`t support CSS load.")
        else:
            QMessageBox.critical(self, "Error", f"Theme '{theme}' not found.")
            print(f"Error: theme {theme} not found")

    def go_back(self):
        """Возвращает пользователя в главное окно."""
        if self.parent() and hasattr(self.parent(), "close_theme_selector"):
            self.parent().close_theme_selector()  # Закрываем текущий виджет
            self.parent().init_main_interface()  # Возвращаемся к главному интерфейсу

