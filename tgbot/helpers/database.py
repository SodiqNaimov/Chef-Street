import sqlalchemy
from sqlalchemy import create_engine,DateTime, Column, String, Integer, CHAR, TEXT, ForeignKey, select, and_, update, Float, Text,BOOLEAN
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
    address: Mapped[str] = mapped_column(TEXT, nullable=True)
    long: Mapped[str] = mapped_column(String(15), nullable=True)
    lat: Mapped[str] = mapped_column(String(15), nullable=True)
    joined_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=True)

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name_uz: Mapped[str] = mapped_column(String(), nullable=True)
    name_ru: Mapped[str] = mapped_column(String(), nullable=True)

    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

    def get_name(self, language='uz'):
        return self.name_uz if language == 'uz' else self.name_ru

    def __repr__(self):
        return f"<Category(id={self.id}, name_uz='{self.name_uz}', name_ru='{self.name_ru}')>"


class Locations(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(primary_key=True)
    name_uzb: Mapped[str] = mapped_column(TEXT, nullable=False)
    name_rus: Mapped[str] = mapped_column(TEXT, nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, nullable=True)

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    name_uz: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    description_uz: Mapped[str] = mapped_column(TEXT, nullable=True)
    description_ru: Mapped[str] = mapped_column(TEXT, nullable=True)
    image: Mapped[str] = mapped_column(TEXT, nullable=True)
    category: Mapped["Category"] = relationship(back_populates="products")

    def get_name(self, language='uz'):
        return self.name_uz if language == 'uz' else self.name_ru

    def get_description(self, language='uz'):
        if language == 'uz':
            return self.description_uz
        return self.description_ru

    def __repr__(self):
        return f"<Product(id={self.id}, name_uz='{self.name_uz}', name_ru='{self.name_ru}')>"

class Basket(Base):
    __tablename__ = 'basket'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]= mapped_column(TEXT, nullable=True)
    product_name_uz: Mapped[str] = mapped_column(TEXT, nullable=True)
    product_name_ru: Mapped[str] = mapped_column(TEXT, nullable=True)

    count: Mapped[int] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=True)
    total_price: Mapped[float] = mapped_column(nullable=True)

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
    def get_all_locations(self, active_only: bool = 1) -> list:
        """Retrieve all locations from the database, optionally filtering by active status"""
        query = self.session.query(Locations)
        if active_only:
            query = self.session.query(Locations.name_uzb, Locations.name_rus, Locations.lat, Locations.lon).filter(Locations.is_active == True).all()
        return query
    def get_categories(self, lang):
        """Get product categories in specified language.

        Args:
            lang: Language code ('uz', 'ru', or 'en')

        Returns:
            List of category names
        """
        lang = lang.lower()
        if lang not in ('uz', 'ru', 'en'):
            lang = 'en'  # Default to English

        column = getattr(Category, f"name_{lang}")
        print(column)
        try:
            categories = self.session.query(column).distinct().all()
            return [cat[0] for cat in categories if cat[0]]
        except SQLAlchemyError as e:
            print(f"Error fetching categories: {e}")
            return []

    def get_user_info(self, user_id: int):
        user = self.session.query(User).filter(User.user_id == str(user_id)).first()

        full_name = user.full_name if user and user.full_name else "No name"
        phone_number = user.phone_number if user and user.phone_number else None

        return full_name, phone_number
    def get_product_names_by_category(
            self,
            category_id,
            lang
    ) :
        """Get only product names for a specific category in the specified language.

        Args:
            session: SQLAlchemy session
            category_id: ID of the category
            lang: Language code ('uz' or 'ru')

        Returns:
            List of product names (empty list if no products found)
        """
        lang = lang.lower()
        if lang not in ('uz', 'ru'):
            lang = 'uz'  # Default to Uzbek

        try:
            # Select only the name column in the requested language
            name_column = Product.name_uz if lang == 'uz' else Product.name_ru
            names = self.session.query(name_column) \
                .filter(Product.category_id == category_id) \
                .all()

            # Extract names from result tuples
            return [name[0] for name in names if name[0]]

        except Exception as e:
            print(f"Error fetching product names: {e}")
            return []
    def get_category_id_by_name(self, name, lang):
        """Get category ID by its name in specified language.

        Args:
            session: SQLAlchemy session
            name: Category name to search for
            lang: Language code ('uz', 'ru', or 'en')

        Returns:
            Category ID if found, None otherwise
        """
        lang = lang.lower()
        if lang not in ('uz', 'ru', 'en'):
            lang = 'uz'  # Default to Uzbek

        try:
            name_column = getattr(Category, f"name_{lang}")
            category = self.session.query(Category.id).filter(name_column == name).first()
            return category[0] if category else None
        except (SQLAlchemyError, AttributeError) as e:
            print(f"Error finding category: {e}")
            return None
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

    def delete_basket_data(self, user_id):
        with self.session.begin():
            # Using SQLAlchemy Core style
            self.session.query(Basket).filter_by(user_id=user_id).delete()
            self.session.commit()

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

    def get_user_basket(self, user_id, lang):
        """Get all items in user's basket using SQLAlchemy.

        Args:
            user_id: Telegram user ID

        Returns:
            List of tuples containing (product_name, count, price, total_price)
            Empty list if basket is empty or user not found
        """
        session = self.session
        print(lang)
        try:
            if lang == 'uz':
                product_name_column = Basket.product_name_uz
            else:
                product_name_column = Basket.product_name_ru
            print(product_name_column)
            print(product_name_column.label("product_name"))
            # Using SQLAlchemy Core style query
            stmt = select(
                product_name_column.label("product_name"),
                Basket.count,
                Basket.price,
                Basket.total_price
            ).where(
                Basket.user_id == str(user_id)
            )

            result = session.execute(stmt).fetchall()
            print(result)
            return [
                (row.product_name, row.count, row.price, row.total_price)
                for row in result
            ]

        except SQLAlchemyError as e:
            print(f"Error fetching basket items: {e}")
            return []
        finally:
            session.close()
    def get_products_by_name(self, name, lang):

        if lang == "uz":
            product = self.session.query(Product.name_uz, Product.price, Product.image, Product.id, Product.name_ru).filter(
                Product.name_uz == name
            ).first()
        elif lang == "ru":
            product = self.session.query(Product.name_ru, Product.price, Product.image, Product.id, Product.name_uz).filter(
                Product.name_ru == name
            ).first()
        if product:
            name = product[0]  # Имя продукта
            price = "{:,.0f}".format(product[1]).replace(",", " ")  # Форматируем цену
            image = product[2]  # Ссылка на изображение
            id = product[3]
            name_ru = product[4]
            return name, price, image, id,name_ru
        else:
            return False
    def get_product_by_id(self, product_id, lang):
        if lang == "uz":
            product = self.session.query(Product.name_uz, Product.price, Product.image, Product.id, Product.name_ru).filter(
                Product.id == product_id
            ).first()
        elif lang == "ru":
            product = self.session.query(Product.name_ru, Product.price, Product.image, Product.id, Product.name_uz).filter(
                Product.id == product_id
            ).first()

        if product:
            name = product[0]  # Product name in the selected language
            price = "{:,.0f}".format(product[1]).replace(",", " ")  # Formatted price
            print(price)
            image = product[2]  # Image URL
            product_id = product[3]  # Product ID
            name_ru = product[4]
            return {
                'name': name,
                'price': price,
                'image': image,
                'id': product_id,
                'name_ru': name_ru


            }
        else:
            return None
    def insert_basket(self, user_id, product_name_uz,count, price, total_price, product_name_ru):
        basket = Basket(
            user_id=user_id,
            product_name_uz=product_name_uz,
            product_name_ru=product_name_ru,

            count=count,
            price=price,
            total_price=total_price
        )
        self.session.add(basket)
        self.session.commit()
    def update_basket_item(self, user_id, product_name,
                           count, total_price, lang):
        if lang == 'uz':
            product_name_column = Basket.product_name_uz
        else:
            product_name_column = Basket.product_name_ru
        self.session.execute(
            update(Basket)
            .where(and_(Basket.user_id == user_id, product_name_column.label("product_name") == product_name))
            .values(count=count, total_price=total_price)
        )
        self.session.commit()
# SQLite()