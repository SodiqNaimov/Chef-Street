import sqlalchemy
from sqlalchemy import create_engine,DateTime, Column, String, Integer, CHAR, TEXT, ForeignKey, select, and_, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship, Session
import sqlite3
from tgbot.files.config import *
from typing import Optional
import sqlite3
# from datetime import datetime, date
from sqlalchemy.sql import func
# database = sqlite3.connect(db_path)
# cursor = database.cursor()
engine = create_engine(f"sqlite:///{db_path}", echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[str]= mapped_column(TEXT, nullable=True)
    full_name: Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] =  mapped_column(String(15), nullable=True)
    lang: Mapped[str] = mapped_column(String(170), nullable=True)
    joined_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=True)


class SQLite:
    def __init__(self):
        self.engine = create_engine(f"sqlite:///{db_path}", echo=True)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close(self):
        self.session.close()

    def register_user(self, user_id, lang, name):
        user = User(
            user_id=user_id,
            full_name=name,
            lang = lang,
        )
        self.session.add(user)
        self.session.commit()


    def get_user_info(self, user_id: int):
        user = self.session.query(User).filter(User.user_id == str(user_id)).first()

        full_name = user.full_name if user and user.full_name else "No name"
        phone_number = user.phone_number if user and user.phone_number else None

        return full_name, phone_number

    def update_user(self, user_id, update_data):
        """
        Update user fields dynamically using a dictionary.

        :param user_id: ID of the user to update
        :param update_data: Dictionary of fields to update
        :return: Updated user object or None if user not found
        """
        try:
            user = self.session.query(User).filter_by(user_id=user_id).first()
            if not user:
                return None  # User not found
            for key, value in update_data.items():
                if hasattr(user, key):  # Ensure the attribute exists in the model
                    setattr(user, key, value)

            self.session.commit()
            return user  # Return the updated user object

        except SQLAlchemyError as e:
            self.session.rollback()  # Rollback in case of an error
            print(f"Error updating user {user_id}: {e}")  # Log the error
            return None  # Return None to indicate failure

    def is_registered(self, user_id):
        return self.session.query(User.user_id).filter_by(user_id=user_id).first() is not None

    def select_all_count(self):
        user = self.session.query(User.user_id).all()
        return user


    # def get_user_info(self):
    #     user = self.session.query(User.name, User.phone_number).all()
    #     return user
    def get_user_lang(self, user_id):
        with self.session as session:
            user = session.query(User.lang).filter_by(user_id=user_id).first()
            return user.lang if user else "en"
    def send_user_message(self):
        user = self.session.query(User.user_id).all()
        return user

    def update_user(self, user_id, update_data):
        """
        Update user fields dynamically using a dictionary.

        :param user_id: ID of the user to update
        :param update_data: Dictionary of fields to update
        :return: Updated user object or None if user not found
        """
        try:
            user = self.session.query(User).filter_by(user_id=user_id).first()
            if not user:
                return None  # User not found
            for key, value in update_data.items():
                if hasattr(user, key):  # Ensure the attribute exists in the model
                    setattr(user, key, value)

            self.session.commit()
            return user  # Return the updated user object

        except SQLAlchemyError as e:
            self.session.rollback()  # Rollback in case of an error
            print(f"Error updating user {user_id}: {e}")  # Log the error
            return None  # Return None to indicate failure


# SQLite()