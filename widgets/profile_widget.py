from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from models import Profile, create_user_session


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

        # Отображение профиля
        layout.addWidget(QLabel(f"Username: {self.user.username}"))
        layout.addWidget(QLabel(f"Bio: {profile.bio}"))

        # Кнопки
        go_back_button = QPushButton("Go Back")
        go_back_button.clicked.connect(self.go_back)
        layout.addWidget(go_back_button)

        self.setLayout(layout)

    def go_back(self):
        """Возвращает пользователя к основному интерфейсу."""
        if hasattr(self.parent, 'init_main_interface'):
            self.parent.init_main_interface()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось вернуться к основному интерфейсу.")
