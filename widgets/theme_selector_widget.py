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
        title_label = QLabel("Выберите тему:")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Кнопки выбора темы
        buttons_layout = QVBoxLayout()

        themes = {
            "Тёмная тема": "dark",
            "Светлая тема": "light",
            "Розовая светлая тема": "pink_light",
            "Сумеречная ночь": "twilight"
        }

        for label, theme_key in themes.items():
            button = QPushButton(label)
            button.setFixedHeight(40)  # Фиксированная высота кнопок
            button.clicked.connect(lambda checked, key=theme_key: self.apply_theme(key))
            buttons_layout.addWidget(button)

        layout.addLayout(buttons_layout)

        # Кнопка "Назад"
        back_button = QPushButton("Назад")
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
                print(f"Тема {theme} успешно применена.")  # Отладочный вывод
            else:
                QMessageBox.warning(self, "Ошибка", "Родительский виджет не поддерживает загрузку CSS.")
        else:
            QMessageBox.critical(self, "Ошибка", f"Тема '{theme}' не найдена.")
            print(f"Ошибка: тема {theme} не найдена.")

    def go_back(self):
        """Возвращает пользователя в главное окно."""
        if self.parent() and hasattr(self.parent(), "close_theme_selector"):
            self.parent().close_theme_selector()  # Закрываем текущий виджет
            self.parent().init_main_interface()  # Возвращаемся к главному интерфейсу

