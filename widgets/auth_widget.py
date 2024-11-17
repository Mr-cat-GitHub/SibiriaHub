from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models import User, create_user_session

from werkzeug.security import generate_password_hash, check_password_hash


class AuthWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.username_input = None
        self.password_input = None
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Кнопки
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)

        layout.addWidget(QLabel("Authorization"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def login(self):
        """Авторизация пользователя."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Both fields are required.")
            return

        try:
            session = create_user_session(username)
            user = session.query(User).filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                QMessageBox.information(self, "Success", f"Welcome, {user.username}!")
                self.parent.load_main_interface(user)
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password.")
        except ValueError:
            QMessageBox.warning(self, "Error", "User not found.")

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        # Создаем сессию для нового пользователя
        session = create_user_session(username)
        if session.query(User).filter_by(username=username).first():
            QMessageBox.warning(self, "Error", "Username already exists!")
            return

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()

        QMessageBox.information(self, "Success", "Registration successful! Please login.")

    def reload_user_session(self):
        """Перезагружает текущую сессию пользователя после изменения имени."""
        session = create_user_session(self.user.username)
        self.user = session.query(type(self.user)).filter_by(username=self.user.username).first()
