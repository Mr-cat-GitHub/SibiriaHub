from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from models import Profile, create_user_session


class ProfileWidget(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Создаем сессию для конкретного пользователя
        session = create_user_session(self.user.username)

        # Получаем профиль пользователя
        profile = self.user.profile
        if not profile:
            profile = Profile(user_id=self.user.id, bio="No bio yet", avatar="")
            session.add(profile)
            session.commit()

        # Отображение профиля
        layout.addWidget(QLabel(f"Username: {self.user.username}"))
        layout.addWidget(QLabel(f"Bio: {profile.bio}"))

        edit_button = QPushButton("Edit Profile")
        edit_button.clicked.connect(self.edit_profile)

        layout.addWidget(edit_button)
        self.setLayout(layout)

    def edit_profile(self):
        QMessageBox.information(self, "Edit Profile", "Editing profile is not yet implemented.")
