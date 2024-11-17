from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QLineEdit
from models import Profile, create_user_session
from werkzeug.security import generate_password_hash
import os
from PyQt6.QtWidgets import QMessageBox
import os
from PyQt6.QtWidgets import QMessageBox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class ProfileWidget(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Получаем профиль пользователя
        session = create_user_session(self.user.username)
        profile = session.query(Profile).filter_by(user_id=self.user.id).first()
        if not profile:
            profile = Profile(user_id=self.user.id, bio="No bio yet", avatar="")
            session.add(profile)
            session.commit()

        # Отображение текущего профиля
        layout.addWidget(QLabel(f"Current Username: {self.user.username}"))
        layout.addWidget(QLabel(f"Bio: {profile.bio}"))

        # Поля для смены имени пользователя
        layout.addWidget(QLabel("Change Username:"))
        self.new_username_input = QLineEdit()
        self.new_username_input.setPlaceholderText("New Username")
        layout.addWidget(self.new_username_input)

        change_username_button = QPushButton("Change Username")
        change_username_button.clicked.connect(self.change_username)
        layout.addWidget(change_username_button)

        # Поля для смены пароля
        layout.addWidget(QLabel("Change Password:"))
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("New Password")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.new_password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)

        change_password_button = QPushButton("Change Password")
        change_password_button.clicked.connect(self.change_password)
        layout.addWidget(change_password_button)

        # Кнопка для возврата
        go_back_button = QPushButton("Go Back")
        go_back_button.clicked.connect(self.go_back)
        layout.addWidget(go_back_button)

        self.setLayout(layout)

    def change_username(self):
        """Смена имени пользователя через переименование базы данных."""
        new_username = self.new_username_input.text().strip()

        if not new_username:
            QMessageBox.warning(self, "Error", "New username cannot be empty.")
            return

        current_db_path = f"data/library_{self.user.username}.db"
        new_db_path = f"data/library_{new_username}.db"

        if os.path.exists(new_db_path):
            QMessageBox.warning(self, "Error", "Username is already taken. Please choose another.")
            return

        try:
            # Завершаем текущую сессию
            session = create_user_session(self.user.username)
            session.close()

            # Переименование файла базы данных
            os.rename(current_db_path, new_db_path)

            # Создаём новую сессию для работы с обновлённым файлом
            new_engine = create_engine(f"sqlite:///{new_db_path}")
            Session = sessionmaker(bind=new_engine)
            session = Session()

            # Загружаем пользователя по ID
            user = session.query(type(self.user)).filter_by(id=self.user.id).first()

            if user:
                # Обновляем имя пользователя
                user.username = new_username
                session.commit()

                # Обновляем текущую сессию пользователя
                self.user.username = new_username
                self.parent.user.username = new_username

                # Удаляем старый файл базы данных
                if os.path.exists(current_db_path):
                    os.remove(current_db_path)

                QMessageBox.information(self, "Success",
                                        "Username changed successfully. Please restart the application for changes to take effect.")
            else:
                QMessageBox.warning(self, "Error", "Failed to find user in the database after renaming.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to rename database: {str(e)}")

    def change_password(self):
        """Смена пароля пользователя."""
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "Both password fields must be filled.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        session = create_user_session(self.user.username)
        user = session.query(type(self.user)).filter_by(id=self.user.id).first()
        if user:
            user.password = generate_password_hash(new_password)
            session.commit()
            QMessageBox.information(self, "Success", "Password changed successfully.")
            self.new_password_input.clear()
            self.confirm_password_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Failed to change the password. Please try again.")

    def go_back(self):
        """Возвращает пользователя к основному интерфейсу."""
        if hasattr(self.parent, 'init_main_interface'):
            self.parent.init_main_interface()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось вернуться к основному интерфейсу.")
