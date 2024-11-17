from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget


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
        layout.addWidget(title_label)

        # Кнопки выбора темы
        buttons_layout = QVBoxLayout()

        # Тёмная тема
        dark_theme_button = QPushButton("Тёмная тема")
        dark_theme_button.clicked.connect(lambda: self.apply_theme("dark"))
        buttons_layout.addWidget(dark_theme_button)

        # Светлая тема
        light_theme_button = QPushButton("Светлая тема")
        light_theme_button.clicked.connect(lambda: self.apply_theme("light"))
        buttons_layout.addWidget(light_theme_button)

        # Светлая розовая тема
        pink_light_button = QPushButton("Розовая светлая тема")
        pink_light_button.clicked.connect(lambda: self.apply_theme("pink_light"))
        buttons_layout.addWidget(pink_light_button)

        # Тёмная розовая тема
        twilight_button = QPushButton("Сумеречная ночь")
        twilight_button.clicked.connect(lambda: self.apply_theme("twilight"))
        buttons_layout.addWidget(twilight_button)

        layout.addLayout(buttons_layout)

        # Кнопка "Назад"
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def apply_theme(self, theme):
        """Применяет выбранную тему и сохраняет её в настройках."""
        theme_files = {
            "dark": "css/dark_theme.css",
            "light": "css/light_theme.css",
            "pink_light": "css/pink_light_theme.css",
            "twilight": "css/twilight_theme.css",  # Проверьте путь
        }

        if theme in theme_files:
            file_path = theme_files[theme]
            self.parent().load_css(file_path)
            self.settings.setValue("theme", theme)
            print(f"Тема {theme} успешно применена.")  # Отладочный вывод
        else:
            print(f"Ошибка: тема {theme} не найдена.")

    def go_back(self):
        """Возвращает пользователя в главное окно."""
        self.parent().init_main_interface()
