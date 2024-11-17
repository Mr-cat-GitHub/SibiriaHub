from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = None  # Сессия будет динамически устанавливаться


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))  # Связь с таблицей пользователей
    user = relationship("User", back_populates="books")  # Обратная связь с моделью User


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    profile = relationship("Profile", back_populates="user", uselist=False)
    books = relationship("Book", back_populates="user")  # Связь с книгами


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bio = Column(String, default="")
    avatar = Column(String, default="")  # путь к изображению
    user = relationship("User", back_populates="profile")


# Создание движка и базы данных
def create_user_session(username):
    """Создает сессию для базы данных конкретного пользователя."""
    global Session
    # Путь к базе данных пользователя
    db_path = f'sqlite:///data/library_{username}.db'
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)  # Устанавливаем глобальную сессию для пользователя
    return Session()
