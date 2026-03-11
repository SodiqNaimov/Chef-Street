import sqlalchemy
from sqlalchemy import create_engine, DateTime, Column, String, Integer, CHAR, TEXT, ForeignKey, select, and_, update, \
    Float, Text, BOOLEAN, TIME, Date, text, delete, insert, extract, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship, Session
import sqlite3
from tgbot.files.config import *
from typing import Optional
import sqlite3
# from datetime import datetime, date,
from sqlalchemy.sql import func
import pandas as pd
from tgbot.texts.text_reply import sum_pul

# database = sqlite3.connect(db_path)
# cursor = database.cursor()
engine = create_engine(f"sqlite:///{db_path}", echo=True)
import datetime
from datetime import datetime, timedelta, timezone
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
class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    branch_name : Mapped[str] = mapped_column(TEXT, nullable=True)
    order_number: Mapped[int] = mapped_column(nullable=False)
    get_order_from: Mapped[str]
    status: Mapped[str] = mapped_column(nullable=True)
    courier: Mapped[str] = mapped_column(nullable=True)
    payment_type: Mapped[str] = mapped_column(nullable=False)
    product_cost: Mapped[int]
    delivery_cost: Mapped[int]
    total_cost: Mapped[int]
    date: Mapped[Date] = mapped_column(DateTime, nullable=True)  # Date only (no time)
    ordered: Mapped[TIME] = mapped_column(TIME, nullable=False)
    cooked: Mapped[TIME] = mapped_column(TIME, nullable=True)
    delivered: Mapped[TIME] = mapped_column(TIME, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=True)
    m_id: Mapped[str] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(TEXT, nullable=True)
    address: Mapped[str]= mapped_column(TEXT, nullable=True)
    long: Mapped[str] = mapped_column(nullable=True)
    lang: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] =  mapped_column(String(15), nullable=True)
    distance: Mapped[float] = mapped_column(nullable=True)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, branch='{self.branch_name}', number={self.order_number})>"

class Admins(Base):
    __tablename__ = 'admins'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]= mapped_column(TEXT, nullable=True)
    name: Mapped[str] = mapped_column(TEXT, nullable=True)
class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str]= mapped_column(TEXT, nullable=True)
    branch_name : Mapped[str] = mapped_column(TEXT, nullable=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))  # Используем id как внешний ключ
    product_name: Mapped[str]
    product_item_cost: Mapped[int]
    count: Mapped[str]
    total_cost: Mapped[int]
    date: Mapped[Date] = mapped_column(Date, nullable=True)  # Date only (no time)

    # Relationship back to Order
    order = relationship("Order", back_populates="items")

class SQLite:
    def __init__(self):
        self.engine = create_engine(f"sqlite:///{db_path}", echo=True)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close(self):
        self.session.close()
    def get_all_admin_id(self):
        # Ensure order_number is a single value, not a tuple
        row = self.session.query(Admins.user_id).all()
        return row
    def register_user(self, user_id, lang, name):
        user = User(
            user_id=user_id,
            full_name=name,
            lang = lang,
        )
        self.session.add(user)
        self.session.commit()
    def update_user_address(self, address, longitude, latitude, user_id):
        try:
            user = self.session.query(User).filter(User.user_id == user_id).first()
            if not user:
                return False  # user not found

            user.address = str(address)
            user.long = str(longitude)
            user.lat = str(latitude)

            self.session.commit()
            return True

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error updating user address: {e}")
            raise
    def register_admin(self, user_id,  name):
        user = Admins(
            user_id=user_id,
            name=name
        )
        self.session.add(user)
        self.session.commit()
    def generate_today_stats(self, branch_names):
        """Generate today's statistics for specified branches"""
        uzbek_tz = timezone(timedelta(hours=5))
        today = datetime.now(uzbek_tz).date()
        import io
        try:
            # Query today's delivered orders
            stmt = select(Order).where(
                and_(
                    Order.date == today,
                    or_(*[Order.branch_name == name for name in branch_names])
                )
            )

            orders = self.session.scalars(stmt).all()

            if not orders:
                return None

            # Prepare data with total cost
            data = []
            for order in orders:
                total_cost = order.product_cost + order.delivery_cost
                data.append({
                    'date': order.date.strftime('%d.%m.%Y'),
                    'branch': order.branch_name,
                    'operator': order.get_order_from,
                    'courier': order.courier,
                    'phone': order.phone_number,
                    'payment_type': order.payment_type,
                    'product_cost': order.product_cost,
                    'delivery_cost': order.delivery_cost,
                    'total_cost': total_cost,  # Added total cost
                    'ordered': order.ordered.strftime('%H:%M'),
                    'delivered': order.delivered.strftime('%H:%M') if order.delivered else '',
                    'order_number': order.order_number

                })

            df = pd.DataFrame(data)
            result_files = {}

            # Process each branch
            for branch_name in branch_names:
                branch_df = df[df['branch'] == branch_name]

                if branch_df.empty:
                    continue

                # Create Excel file in memory
                output = io.BytesIO()

                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    # Create renamed DataFrame
                    detailed_df = branch_df[[
                        'date', 'operator', 'courier', 'phone',
                        'payment_type', 'product_cost', 'delivery_cost',
                        'total_cost', 'ordered', 'delivered', 'order_number'
                    ]].rename(columns={
                        'date': 'Sana',
                        'operator': 'Operator',
                        'payment_type': "To'lov turi",
                        'phone': 'Telefon',
                        'courier': 'Kuryer',
                        'product_cost': 'Mahsulot narxi',
                        'delivery_cost': 'Yetkazish narxi',
                        'total_cost': 'Jami summa',
                        'ordered': 'Buyurtma vaqti',
                        'delivered': 'Yetkazildi',
                        'order_number': 'Buyurtma raqami'
                    })

                    # Write detailed data
                    detailed_df.to_excel(writer, sheet_name='Bugungi Statistika', index=False)

                    # Calculate custom summary values
                    summary_data = [
                        ("📊 Jami buyurtmalar soni", "{:,.0f}".format(len(branch_df)).replace(",", " ")),
                        ("💰 O'rtacha mahsulot narxi",
                         "{:,.0f}".format(branch_df['product_cost'].mean()).replace(",", " ") + " so'm"),
                        ("📦 Jami mahsulot narxi",
                         "{:,.0f}".format(branch_df['product_cost'].sum()).replace(",", " ") + " so'm"),
                        ("🚚 O'rtacha yetkazish narxi",
                         "{:,.0f}".format(branch_df['delivery_cost'].mean()).replace(",", " ") + " so'm"),
                        ("📦 Jami yetkazish narxi",
                         "{:,.0f}".format(branch_df['delivery_cost'].sum()).replace(",", " ") + " so'm"),
                        ("💵 O'rtacha jami summa",
                         "{:,.0f}".format(branch_df['total_cost'].mean()).replace(",", " ") + " so'm"),
                        ("🏦 Jami summa",
                         "{:,.0f}".format(branch_df['total_cost'].sum()).replace(",", " ") + " so'm"),
                    ]

                    summary_df = pd.DataFrame(summary_data, columns=["Ko'rsatkich", "Qiymat"])

                    # Write below the detailed table
                    start_row = len(detailed_df) + 3
                    summary_df.to_excel(writer, sheet_name='Bugungi Statistika', startrow=start_row, index=False)

                output.seek(0)
                result_files[branch_name] = {
                    'file': output,
                    'filename': f"{branch_name.replace(' ', '_')}_bugun_{today.strftime('%d.%m.%Y')}.xlsx",
                    'count': len(branch_df)
                }

            return result_files if result_files else None

        except Exception as e:
            print(f"Xatolik: {str(e)}")
            return None
    def generate_stats_for_date_branch(self, branch_names, input_date):
        """Generate statistics for a specific date for specified branches"""
        uzbek_tz = timezone(timedelta(hours=5))
        try:
            # Convert input string to date object
            target_date = datetime.strptime(input_date, '%d.%m.%Y').date()
        except ValueError:
            return None  # Invalid date format

        import io
        try:
            # Query orders for the specified date
            stmt = select(Order).where(
                and_(
                    Order.date == target_date,
                    or_(*[Order.branch_name == name for name in branch_names])
                )
            )

            orders = self.session.scalars(stmt).all()

            if not orders:
                return None

            # Prepare data with total cost
            data = []
            for order in orders:
                total_cost = order.product_cost + order.delivery_cost
                data.append({
                    'date': order.date.strftime('%d.%m.%Y'),
                    'branch': order.branch_name,
                    'operator': order.get_order_from,
                    'courier': order.courier,
                    'phone': order.phone_number,
                    'payment_type': order.payment_type,
                    'product_cost': order.product_cost,
                    'delivery_cost': order.delivery_cost,
                    'total_cost': total_cost,
                    'ordered': order.ordered.strftime('%H:%M'),
                    'delivered': order.delivered.strftime('%H:%M') if order.delivered else '',
                    'order_number': order.order_number
                })

            df = pd.DataFrame(data)
            result_files = {}

            # Process each branch
            for branch_name in branch_names:
                branch_df = df[df['branch'] == branch_name]

                if branch_df.empty:
                    continue

                # Create Excel file in memory
                output = io.BytesIO()

                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    # Create renamed DataFrame
                    detailed_df = branch_df[[
                        'date', 'operator', 'courier', 'phone',
                        'payment_type', 'product_cost', 'delivery_cost',
                        'total_cost', 'ordered', 'delivered', 'order_number'
                    ]].rename(columns={
                        'date': 'Sana',
                        'operator': 'Operator',
                        'payment_type': "To'lov turi",
                        'phone': 'Telefon',
                        'courier': 'Kuryer',
                        'product_cost': 'Mahsulot narxi',
                        'delivery_cost': 'Yetkazish narxi',
                        'total_cost': 'Jami summa',
                        'ordered': 'Buyurtma vaqti',
                        'delivered': 'Yetkazildi',
                        'order_number': 'Buyurtma raqami'
                    })

                    # Write detailed data
                    detailed_df.to_excel(writer, sheet_name='Statistika', index=False)

                    # Calculate custom summary values
                    summary_data = [
                        ("📊 Jami buyurtmalar soni", "{:,.0f}".format(len(branch_df)).replace(",", " ")),
                        ("💰 O'rtacha mahsulot narxi",
                         "{:,.0f}".format(branch_df['product_cost'].mean()).replace(",", " ") + " so'm"),
                        ("📦 Jami mahsulot narxi",
                         "{:,.0f}".format(branch_df['product_cost'].sum()).replace(",", " ") + " so'm"),
                        ("🚚 O'rtacha yetkazish narxi",
                         "{:,.0f}".format(branch_df['delivery_cost'].mean()).replace(",", " ") + " so'm"),
                        ("📦 Jami yetkazish narxi",
                         "{:,.0f}".format(branch_df['delivery_cost'].sum()).replace(",", " ") + " so'm"),
                        ("💵 O'rtacha jami summa",
                         "{:,.0f}".format(branch_df['total_cost'].mean()).replace(",", " ") + " so'm"),
                        ("🏦 Jami summa",
                         "{:,.0f}".format(branch_df['total_cost'].sum()).replace(",", " ") + " so'm"),
                    ]

                    summary_df = pd.DataFrame(summary_data, columns=["Ko'rsatkich", "Qiymat"])

                    # Write below the detailed table
                    start_row = len(detailed_df) + 3
                    summary_df.to_excel(writer, sheet_name='Statistika', startrow=start_row, index=False)

                output.seek(0)
                result_files[branch_name] = {
                    'file': output,
                    'filename': f"{branch_name.replace(' ', '_')}_{target_date.strftime('%d.%m.%Y')}.xlsx",
                    'count': len(branch_df)
                }

            return result_files if result_files else None

        except Exception as e:
            print(f"Xatolik: {str(e)}")
            return None
    def generate_branch_stats_with_period(self, branch_names, start_date, end_date,bot, message):
        # Set Uzbekistan timezone (UTC+5)
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # Set Uzbekistan timezone (UTC+5)
        uzbek_tz = timezone(timedelta(hours=5))
        now = datetime.now(uzbek_tz)

        try:
            # Query orders for all specified branches within the provided period
            stmt = select(Order).where(
                and_(
                    Order.date >= start_date,
                    Order.date <= end_date,
                    or_(*[Order.branch_name == name for name in branch_names])
                )
            )

            orders = self.session.scalars(stmt).all()

            # Prepare data with total cost
            data = []
            for order in orders:
                try:
                    branch_value = getattr(order, 'branch_name',
                                           getattr(order, 'branch',
                                                   getattr(order, 'branchName', None)))

                    # Calculate total cost
                    total_cost = order.product_cost + order.delivery_cost

                    data.append({
                        'date': order.date,
                        'branch': branch_value,
                        'get_order_from': order.get_order_from,
                        'courier': order.courier,
                        'phone_number': order.phone_number,
                        'payment_type': order.payment_type,
                        'product_cost': order.product_cost,
                        'delivery_cost': order.delivery_cost,
                        'total_cost': total_cost,  # Added total cost
                        'status': order.status,
                        'ordered': order.ordered,
                        'cooked': order.cooked,
                        'delivered': order.delivered,
                        'order_number': order.order_number
                    })
                except Exception as e:
                    print(f"Error processing order {order.id}: {str(e)}")
                    continue

            if not data:
                print("No orders found matching criteria")
                return []

            df = pd.DataFrame(data)

            # Generate separate Excel files for each branch
            result_files = []
            for branch_name in branch_names:
                try:
                    branch_df = df[df['branch'] == branch_name]

                    if branch_df.empty:
                        print(f"No orders found for branch: {branch_name}")
                        continue

                    # Create detailed stats with Uzbek column names
                    detailed_stats = branch_df[[
                        'date', 'get_order_from', 'courier', 'phone_number',
                        'payment_type', 'product_cost', 'delivery_cost',
                        'total_cost', 'ordered', 'cooked', 'delivered', 'order_number'
                    ]].rename(columns={
                        'date': 'Sana',
                        'get_order_from': 'Operator',
                        'payment_type': "To'lov turi",
                        'phone_number': 'Telefon raqami',
                        'courier': 'Kuryer',
                        'product_cost': 'Mahsulot narxi',
                        'delivery_cost': 'Yetkazish narxi',
                        'total_cost': 'Jami summa',  # Uzbek translation for total cost
                        'ordered': 'Buyurtma vaqti',
                        'cooked': 'Tayyorlandi',
                        'delivered': 'Yetkazildi',
                        'order_number': 'Buyurtma raqami'
                    })

                    # Create summary stats with total cost
                    summary_stats = branch_df.groupby('get_order_from').agg({
                        'phone_number': 'count',
                        'product_cost': 'sum',
                        'delivery_cost': 'sum',
                        'total_cost': 'sum'  # Added total cost to summary
                    }).rename(columns={
                        'phone_number': 'Buyurtmalar soni',
                        'product_cost': 'Jami mahsulot narxi',
                        'delivery_cost': 'Jami yetkazish narxi',
                        'total_cost': 'Jami summa'  # Uzbek translation
                    }).reset_index()

                    # Write to Excel
                    filename = f"{branch_name}_statistika_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.xlsx".replace(
                        '/', '_')
                    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
                        # Write the detailed stats
                        detailed_stats.to_excel(writer, sheet_name='Statistika', index=False)

                        # Prepare summary data
                        summary_data = [
                            ("📊 Jami buyurtmalar soni", f"{len(branch_df):,}".replace(",", " ")),
                            ("💰 O'rtacha mahsulot narxi",
                             f"{branch_df['product_cost'].mean():,.0f}".replace(",", " ") + " so'm"),
                            ("📦 Jami mahsulot narxi",
                             f"{branch_df['product_cost'].sum():,.0f}".replace(",", " ") + " so'm"),
                            ("🚚 O'rtacha yetkazish narxi",
                             f"{branch_df['delivery_cost'].mean():,.0f}".replace(",", " ") + " so'm"),
                            ("📦 Jami yetkazish narxi",
                             f"{branch_df['delivery_cost'].sum():,.0f}".replace(",", " ") + " so'm"),
                            ("💵 O'rtacha jami summa",
                             f"{branch_df['total_cost'].mean():,.0f}".replace(",", " ") + " so'm"),
                            ("🏦 Jami summa",
                             f"{branch_df['total_cost'].sum():,.0f}".replace(",", " ") + " so'm"),
                        ]

                        summary_df = pd.DataFrame(summary_data, columns=["Ko'rsatkich", "Qiymat"])

                        # Write below the detailed data
                        start_row = len(detailed_stats) + 3
                        summary_df.to_excel(writer, sheet_name='Statistika', startrow=start_row, index=False)

                    result_files.append(filename)
                    print(f"{branch_name} uchun statistika yaratildi: {filename}")

                    # Send the file to the user
                    with open(filename, 'rb') as file:
                        bot.send_document(message.chat.id, file)

                except Exception as e:
                    print(f"{branch_name} filialida xatolik: {str(e)}")
                    continue

            return result_files

        except Exception as e:
            print(f"Statistika yaratishda xatolik: {str(e)}")
            return []
    def send_monthly_summary(self, branch_names, bot, message):
        from datetime import datetime, timedelta, timezone
        import pandas as pd
        from sqlalchemy import extract
        chat_id = message.chat.id
        uzbek_tz = timezone(timedelta(hours=5))
        now = datetime.now(uzbek_tz)
        current_month = now.month
        current_year = now.year

        try:
            stmt = select(Order).where(
                and_(
                    extract('month', Order.date) == current_month,
                    extract('year', Order.date) == current_year,
                    or_(*[Order.branch_name == name for name in branch_names])
                )
            )

            orders = self.session.scalars(stmt).all()

            if not orders:
                bot.send_message(chat_id, f"Ushbu oyda <b>{branch_names[0]}</b> uchun hech qanday buyurtma topilmadi.")
                return

            df_data = []
            for order in orders:
                branch_value = getattr(order, 'branch_name',
                                       getattr(order, 'branch', getattr(order, 'branchName', None)))
                total_cost = order.product_cost + order.delivery_cost
                df_data.append({
                    'branch': branch_value,
                    'product_cost': order.product_cost,
                    'delivery_cost': order.delivery_cost,
                    'total_cost': total_cost
                })

            df = pd.DataFrame(df_data)

            for branch_name in branch_names:
                branch_df = df[df['branch'] == branch_name]

                if branch_df.empty:
                    bot.send_message(chat_id, f"'{branch_name}' filialida bu oyda buyurtmalar topilmadi.")
                    continue

                order_count = len(branch_df)
                total_product = branch_df['product_cost'].sum()
                total_delivery = branch_df['delivery_cost'].sum()
                total_summa = branch_df['total_cost'].sum()

                avg_product = int(total_product / order_count) if order_count else 0
                avg_delivery = int(total_delivery / order_count) if order_count else 0

                text = (
                    f"📊 Oy yakunlari ({branch_name}):\n\n"
                    f"🧾 Buyurtmalar сони: {order_count}\n"
                    f"💰 Умумий буюртмалар суммаси: {total_summa:,} so'm\n"
                    f"📦 Ўртача буюртма нархи: {avg_product:,} so'm\n"
                    f"🚚 Умумий етказиб бериш суммаси: {total_delivery:,} so'm\n"
                    f"🚕 Ўртача етказиб бериш нархи: {avg_delivery:,} so'm"
                )

                bot.send_message(chat_id, text)

        except Exception as e:
            bot.send_message(chat_id, f"Oylik statistika chiqarishda xatolik: {str(e)}")
    def send_period_summary(self, branch_names,  start_date, end_date, bot, message):
        """
        start_date and end_date must be `datetime.date` objects
        """
        from datetime import timezone, timedelta
        import pandas as pd
        from sqlalchemy import and_, or_
        chat_id = message.chat.id
        uzbek_tz = timezone(timedelta(hours=5))

        try:
            # Convert to datetime with timezones
            start_datetime = datetime.combine(start_date, datetime.min.time(), tzinfo=uzbek_tz)
            end_datetime = datetime.combine(end_date, datetime.max.time(), tzinfo=uzbek_tz)

            stmt = select(Order).where(
                and_(
                    Order.date >= start_datetime,
                    Order.date <= end_datetime,
                    or_(*[Order.branch_name == name for name in branch_names])
                )
            )

            orders = self.session.scalars(stmt).all()

            if not orders:
                bot.send_message(chat_id,
                                 f"{start_date} dan {end_date} gacha bo'lgan oraliqda {branch_names[0]} uchun hech qanday buyurtma topilmadi.")
                return

            df_data = []
            for order in orders:
                branch_value = getattr(order, 'branch_name',
                                       getattr(order, 'branch', getattr(order, 'branchName', None)))
                total_cost = order.product_cost + order.delivery_cost
                df_data.append({
                    'branch': branch_value,
                    'product_cost': order.product_cost,
                    'delivery_cost': order.delivery_cost,
                    'total_cost': total_cost
                })

            df = pd.DataFrame(df_data)

            for branch_name in branch_names:
                branch_df = df[df['branch'] == branch_name]

                if branch_df.empty:
                    bot.send_message(chat_id,
                                     f"{branch_name} filialida {start_date} dan {end_date} gacha buyurtmalar topilmadi.")
                    continue

                order_count = len(branch_df)
                total_product = branch_df['product_cost'].sum()
                total_delivery = branch_df['delivery_cost'].sum()
                total_summa = branch_df['total_cost'].sum()

                avg_product = int(total_product / order_count) if order_count else 0
                avg_delivery = int(total_delivery / order_count) if order_count else 0

                text = (
                    f"📊 Statistika ({branch_name})\n"
                    f"🗓 Sana: {start_date.strftime('%Y-%m-%d')} ➡ {end_date.strftime('%Y-%m-%d')}\n\n"
                    f"🧾 Buyurtmalar сони: {order_count}\n"
                    f"💰 Умумий буюртмалар суммаси: {total_summa:,} so'm\n"
                    f"📦 Ўртача буюртма нархи: {avg_product:,} so'm\n"
                    f"🚚 Умумий етказиб бериш суммаси: {total_delivery:,} so'm\n"
                    f"🚕 Ўртача етказиб бериш нархи: {avg_delivery:,} so'm"
                )

                bot.send_message(chat_id, text)

        except Exception as e:
            bot.send_message(chat_id, f"Oraliqdagi statistika chiqarishda xatolik: {str(e)}")
    def send_daily_summary_branch(self, branch_names, bot, message, input_date):
        """Generate and send summary statistics for a specific date"""
        from datetime import datetime, timezone, timedelta
        import pandas as pd
        chat_id = message.chat.id
        uzbek_tz = timezone(timedelta(hours=5))

        try:
            # Convert input string to date object
            target_date = datetime.strptime(input_date, '%d.%m.%Y').date()
        except ValueError:
            bot.send_message(chat_id, "⚠️ Noto'g'ri sana formati! Iltimos, DD.MM.YYYY formatida kiriting.")
            return

        try:
            stmt = select(Order).where(
                and_(
                    Order.date == target_date,
                    or_(*[Order.branch_name == name for name in branch_names])
                )
            )

            orders = self.session.scalars(stmt).all()

            if not orders:
                bot.send_message(chat_id,
                                 f"{input_date} sanasida <b>{branch_names[0]}</b> uchun hech qanday buyurtma topilmadi.")
                return

            df_data = []
            for order in orders:
                branch_value = getattr(order, 'branch_name',
                                       getattr(order, 'branch', getattr(order, 'branchName', None)))
                total_cost = order.product_cost + order.delivery_cost
                df_data.append({
                    'branch': branch_value,
                    'product_cost': order.product_cost,
                    'delivery_cost': order.delivery_cost,
                    'total_cost': total_cost
                })

            df = pd.DataFrame(df_data)

            for branch_name in branch_names:
                branch_df = df[df['branch'] == branch_name]

                if branch_df.empty:
                    bot.send_message(chat_id, f"'{branch_name}' filialida {input_date} sanasida buyurtmalar topilmadi.")
                    continue

                order_count = len(branch_df)
                total_product = branch_df['product_cost'].sum()
                total_delivery = branch_df['delivery_cost'].sum()
                total_summa = branch_df['total_cost'].sum()

                avg_product = int(total_product / order_count) if order_count else 0
                avg_delivery = int(total_delivery / order_count) if order_count else 0

                text = (
                    f"📊 Kunlik statistika ({branch_name}):\n"
                    f"📅 Sana: {input_date}\n\n"
                    f"🧾 Buyurtmalar soni: {order_count}\n"
                    f"💰 Umumiy buyurtmalar summası: {total_summa:,} so'm\n"
                    f"📦 O'rtacha buyurtma narxi: {avg_product:,} so'm\n"
                    f"🚚 Umumiy yetkazib berish summası: {total_delivery:,} so'm\n"
                    f"🚕 O'rtacha yetkazib berish narxi: {avg_delivery:,} so'm"
                )

                bot.send_message(chat_id, text)

        except Exception as e:
            bot.send_message(chat_id, f"Kunlik statistika chiqarishda xatolik: {str(e)}")
    def send_last_10days_summary_branch(self, branch_names, bot, message):
        """Generate and send summary statistics for the last 10 days"""
        from datetime import datetime, timedelta, timezone
        import pandas as pd
        chat_id = message.chat.id
        uzbek_tz = timezone(timedelta(hours=5))
        now = datetime.now(uzbek_tz)
        ten_days_ago = (now - timedelta(days=10)).date()
        today = now.date()

        try:
            stmt = select(Order).where(
                and_(
                    Order.date >= ten_days_ago,
                    Order.date <= today,
                    or_(*[Order.branch_name == name for name in branch_names])
                )
            )

            orders = self.session.scalars(stmt).all()

            if not orders:
                bot.send_message(chat_id,
                                 f"So'nggi 10 kun ichida <b>{branch_names[0]}</b> uchun hech qanday buyurtma topilmadi.")
                return

            df_data = []
            for order in orders:
                branch_value = getattr(order, 'branch_name',
                                       getattr(order, 'branch', getattr(order, 'branchName', None)))
                total_cost = order.product_cost + order.delivery_cost
                df_data.append({
                    'branch': branch_value,
                    'product_cost': order.product_cost,
                    'delivery_cost': order.delivery_cost,
                    'total_cost': total_cost,
                    'date': order.date.strftime('%d.%m.%Y')  # Adding date for reference
                })

            df = pd.DataFrame(df_data)

            for branch_name in branch_names:
                branch_df = df[df['branch'] == branch_name]

                if branch_df.empty:
                    bot.send_message(chat_id, f"'{branch_name}' filialida so'nggi 10 kun ichida buyurtmalar topilmadi.")
                    continue

                order_count = len(branch_df)
                total_product = branch_df['product_cost'].sum()
                total_delivery = branch_df['delivery_cost'].sum()
                total_summa = branch_df['total_cost'].sum()

                avg_product = int(total_product / order_count) if order_count else 0
                avg_delivery = int(total_delivery / order_count) if order_count else 0

                text = (
                    f"📊 So'nggi 10 kunlik statistika ({branch_name}):\n\n"
                    f"📅 {ten_days_ago.strftime('%d.%m.%Y')} - {today.strftime('%d.%m.%Y')}\n\n"
                    f"🧾 Buyurtmalar soni: {order_count}\n"
                    f"💰 Umumiy buyurtmalar summası: {total_summa:,} so'm\n"
                    f"📦 O'rtacha buyurtma narxi: {avg_product:,} so'm\n"
                    f"🚚 Umumiy yetkazib berish summası: {total_delivery:,} so'm\n"
                    f"🚕 O'rtacha yetkazib berish narxi: {avg_delivery:,} so'm"
                )

                bot.send_message(chat_id, text)

        except Exception as e:
            bot.send_message(chat_id, f"So'nggi 10 kunlik statistika chiqarishda xatolik: {str(e)}")
    def send_today_summary(self, branch_names,bot, message):
        from datetime import datetime, timedelta, timezone
        import pandas as pd
        chat_id = message.chat.id
        uzbek_tz = timezone(timedelta(hours=5))
        today = datetime.now(uzbek_tz).date()

        try:
            stmt = select(Order).where(
                and_(
                    extract('day', Order.date) == today.day,
                    extract('month', Order.date) == today.month,
                    extract('year', Order.date) == today.year,
                    or_(*[Order.branch_name == name for name in branch_names])
                )
            )

            orders = self.session.scalars(stmt).all()
            print(orders)
            if not orders:
                bot.send_message(chat_id, "Bugungi kunga oid buyurtmalar topilmadi.")
                return

            df_data = []
            for order in orders:
                branch_value = getattr(order, 'branch_name',
                                       getattr(order, 'branch', getattr(order, 'branchName', None)))
                total_cost = order.product_cost + order.delivery_cost
                df_data.append({
                    'branch': branch_value,
                    'product_cost': order.product_cost,
                    'delivery_cost': order.delivery_cost,
                    'total_cost': total_cost
                })

            df = pd.DataFrame(df_data)

            for branch_name in branch_names:
                branch_df = df[df['branch'] == branch_name]

                if branch_df.empty:
                    bot.send_message(chat_id, f"Bugun '{branch_name}' filialida buyurtmalar topilmadi.")
                    continue

                order_count = len(branch_df)
                total_product = branch_df['product_cost'].sum()
                total_delivery = branch_df['delivery_cost'].sum()
                total_summa = branch_df['total_cost'].sum()

                avg_product = int(total_product / order_count) if order_count else 0
                avg_delivery = int(total_delivery / order_count) if order_count else 0

                text = (
                    f"📊 Bugungi statistika ({branch_name}):\n\n"
                    f"🧾 Buyurtmalar сони: {order_count}\n"
                    f"💰 Умумий буюртмалар суммаси: {total_summa:,} so'm\n"
                    f"📦 Ўртача буюртма нархи: {avg_product:,} so'm\n"
                    f"🚚 Умумий етказиб бериш суммаси: {total_delivery:,} so'm\n"
                    f"🚕 Ўртача етказиб бериш нархи: {avg_delivery:,} so'm"
                )

                bot.send_message(chat_id, text)

        except Exception as e:
            bot.send_message(chat_id, f"Statistika chiqarishda xatolik: {str(e)}")
    def generate_last_10days_stats_fillials(self, branch_names):
        """Generate statistics for the last 10 days for specified branches"""
        uzbek_tz = timezone(timedelta(hours=5))
        today = datetime.now(uzbek_tz).date()
        ten_days_ago = today - timedelta(days=10)
        import io

        try:
            # Query orders from last 10 days
            stmt = select(Order).where(
                and_(
                    Order.date >= ten_days_ago,
                    Order.date <= today,
                    or_(*[Order.branch_name == name for name in branch_names])
                )
            )

            orders = self.session.scalars(stmt).all()

            if not orders:
                return None

            # Prepare data with total cost
            data = []
            for order in orders:
                total_cost = order.product_cost + order.delivery_cost
                data.append({
                    'date': order.date.strftime('%d.%m.%Y'),
                    'branch': order.branch_name,
                    'operator': order.get_order_from,
                    'courier': order.courier,
                    'phone': order.phone_number,
                    'payment_type': order.payment_type,
                    'product_cost': order.product_cost,
                    'delivery_cost': order.delivery_cost,
                    'total_cost': total_cost,
                    'ordered': order.ordered.strftime('%H:%M'),
                    'delivered': order.delivered.strftime('%H:%M') if order.delivered else '',
                    'order_number': order.order_number
                })

            df = pd.DataFrame(data)
            result_files = {}

            # Process each branch
            for branch_name in branch_names:
                branch_df = df[df['branch'] == branch_name]

                if branch_df.empty:
                    continue

                # Create Excel file in memory
                output = io.BytesIO()

                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    # Create renamed DataFrame
                    detailed_df = branch_df[[
                        'date', 'operator', 'courier', 'phone',
                        'payment_type', 'product_cost', 'delivery_cost',
                        'total_cost', 'ordered', 'delivered', 'order_number'
                    ]].rename(columns={
                        'date': 'Sana',
                        'operator': 'Operator',
                        'payment_type': "To'lov turi",
                        'phone': 'Telefon',
                        'courier': 'Kuryer',
                        'product_cost': 'Mahsulot narxi',
                        'delivery_cost': 'Yetkazish narxi',
                        'total_cost': 'Jami summa',
                        'ordered': 'Buyurtma vaqti',
                        'delivered': 'Yetkazildi',
                        'order_number': 'Buyurtma raqami'
                    })

                    # Write detailed data
                    detailed_df.to_excel(writer, sheet_name='10 Kunlik Statistika', index=False)

                    # Calculate custom summary values
                    summary_data = [
                        ("📊 Jami buyurtmalar soni", "{:,.0f}".format(len(branch_df)).replace(",", " ")),
                        ("💰 O'rtacha mahsulot narxi",
                         "{:,.0f}".format(branch_df['product_cost'].mean()).replace(",", " ") + " so'm"),
                        ("📦 Jami mahsulot narxi",
                         "{:,.0f}".format(branch_df['product_cost'].sum()).replace(",", " ") + " so'm"),
                        ("🚚 O'rtacha yetkazish narxi",
                         "{:,.0f}".format(branch_df['delivery_cost'].mean()).replace(",", " ") + " so'm"),
                        ("📦 Jami yetkazish narxi",
                         "{:,.0f}".format(branch_df['delivery_cost'].sum()).replace(",", " ") + " so'm"),
                        ("💵 O'rtacha jami summa",
                         "{:,.0f}".format(branch_df['total_cost'].mean()).replace(",", " ") + " so'm"),
                        ("🏦 Jami summa",
                         "{:,.0f}".format(branch_df['total_cost'].sum()).replace(",", " ") + " so'm"),
                    ]

                    summary_df = pd.DataFrame(summary_data, columns=["Ko'rsatkich", "Qiymat"])

                    # Write below the detailed table
                    start_row = len(detailed_df) + 3
                    summary_df.to_excel(writer, sheet_name='10 Kunlik Statistika', startrow=start_row, index=False)

                output.seek(0)
                result_files[branch_name] = {
                    'file': output,
                    'filename': f"{branch_name.replace(' ', '_')}_10_kunlik_{today.strftime('%d.%m.%Y')}.xlsx",
                    'count': len(branch_df)
                }

            return result_files if result_files else None

        except Exception as e:
            print(f"Xatolik: {str(e)}")
            return None
    def insert_user_address(self, user_id, address, longitude, latitude):
        try:
            stmt = insert(User).values(
                user_id=user_id,
                address=str(address),
                long=str(longitude),
                lat=str(latitude)
            )

            self.session.execute(stmt)
            self.session.commit()
            return True

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error inserting user address: {e}")
            raise
    def get_all_locations(self, active_only: bool = 1) -> list:
        """Retrieve all locations from the database, optionally filtering by active status"""
        query = self.session.query(Locations)
        if active_only:
            query = self.session.query(Locations.name_uzb, Locations.name_rus, Locations.lat, Locations.lon).filter(Locations.is_active == True).all()
        return query
    def update_user_phone(self, user_id, phone):
        """Updates the text field by order_number"""
        processing = self.session.query(User).filter_by(user_id=user_id).first()
        if processing:
            processing.phone_number = phone
            self.session.commit()
            return True
        return False
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
    def get_order_number(self):
        """Atomically get the next order number to prevent duplicates."""
        # Start a transaction and lock the database for writing
        self.session.execute(text("BEGIN IMMEDIATE"))

        # Get the current max
        result = self.session.execute(
            text("SELECT MAX(order_number) FROM orders")
        ).scalar()

        next_number = (result or 0) + 1

        # Commit to release the lock
        self.session.commit()

        return next_number
    def get_user_full_address(self, user_id):
        """Get user's full address with coordinates using SQLAlchemy.

        Args:
            user_id: Telegram user ID

        Returns:
            Tuple of (address, longitude, latitude) if found, None otherwise
        """
        session = self.session
        try:
            # Using SQLAlchemy Core style query
            stmt = select(
                User.address,
                User.long,
                User.lat
            ).where(
                User.user_id == str(user_id)
            )

            result = session.execute(stmt).first()

            if result:
                return (result.address, result.long, result.lat)
            return None

        except SQLAlchemyError as e:
            print(f"Error fetching user address: {e}")
            return None
        finally:
            session.close()
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
    def get_order_number_total_cost(self, order_number):
        courier = self.session.query(Order.total_cost, Order.product_cost).filter_by(order_number=order_number).first()
        return courier
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
    def add_order(self,branch_name, order_number, get_order_from, status, payment_type, product_cost, delivery_cost, ordered_time, order_date, m_id, comment, address, long, lang, phone_number, distance, total_cost):
        date_obj = datetime.strptime(order_date, '%Y-%m-%d').date()

        # Convert time string to time object
        time_obj = datetime.strptime(ordered_time, '%H:%M').time()
        clean_product_cost = int(total_cost.replace(' ', ''))
        try:
            clean_delivery_cost = int(delivery_cost.replace(' ', ''))
        except Exception as e:
            print(e)
        orders = Order(
            branch_name=branch_name,
            order_number=order_number,
            get_order_from=get_order_from,
            status = status,
            payment_type=payment_type,
            product_cost=product_cost,
            delivery_cost = clean_delivery_cost,
            ordered=time_obj,  # Combine date and time
            date=date_obj,
            m_id=m_id,
            comment = comment,
            address=address,
            long=long,
            lang=lang,
            phone_number = phone_number,
            distance=distance,
            total_cost = clean_product_cost
        )
        self.session.add(orders)
        self.session.commit()

    def add_order_pickup(self, branch_name, order_number, get_order_from, status, payment_type, product_cost, delivery_cost,
                  ordered_time, order_date, m_id, comment, address, long, lang, phone_number, distance, total_cost):
        date_obj = datetime.strptime(order_date, '%Y-%m-%d').date()

        # Convert time string to time object
        time_obj = datetime.strptime(ordered_time, '%H:%M').time()
        clean_product_cost = int(total_cost.replace(' ', ''))
        orders = Order(
            branch_name=branch_name,
            order_number=order_number,
            get_order_from=get_order_from,
            status=status,
            payment_type=payment_type,
            product_cost=product_cost,
            delivery_cost=0,
            ordered=time_obj,  # Combine date and time
            date=date_obj,
            m_id=m_id,
            comment=comment,
            address=address,
            long=long,
            lang=lang,
            phone_number=phone_number,
            distance=distance,
            total_cost=clean_product_cost
        )
        self.session.add(orders)
        self.session.commit()
    def get_products_by_name(self, name, lang):

        if lang == "uz":
            product = self.session.query(Product.name_uz, Product.price, Product.image, Product.id, Product.name_ru, Product.description_uz).filter(
                Product.name_uz == name
            ).first()
        elif lang == "ru":
            product = self.session.query(Product.name_ru, Product.price, Product.image, Product.id, Product.name_uz, Product.description_ru).filter(
                Product.name_ru == name
            ).first()
        if product:
            name = product[0]  # Имя продукта
            price = "{:,.0f}".format(product[1]).replace(",", " ")  # Форматируем цену
            image = product[2]  # Ссылка на изображение
            id = product[3]
            name_ru = product[4]
            description = product[5]
            return name, price, image, id,name_ru, description
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
    def get_order_number_total_cost(self, order_number):
        courier = self.session.query(Order.total_cost, Order.product_cost).filter_by(order_number=order_number).first()
        return courier

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
    def get_count_user_basket(self, user_id, product_name, lang):
        if lang == 'uz':
            product_name_column = Basket.product_name_uz
        else:
            product_name_column = Basket.product_name_ru
        """Get product count from user's basket"""
        result = self.session.query(Basket.count).filter(
            Basket.user_id == user_id,
            product_name_column.label("product_name") == product_name
        ).first()

        return result[0] if result else 0
    def get_product_info_b(self, lang: str, product_name: str):
        """
        Get product info in specified language
        Returns: (product_name, description, price, image) or None if not found
        """
        lang = lang.lower()
        valid_langs = {'uz', 'ru', 'en'}
        if lang not in valid_langs:
            lang = 'en'  # Default to English

        product = self.session.query(
            getattr(Product, f"name_{lang}"),
            Product.price,
            Product.image
        ).filter(
            getattr(Product, f"name_{lang}") == product_name
        ).first()

        print(f"DEBUG: get_product_info_b({lang}, {product_name}) -> {product}")

        return product if product else None
    def update_data_savat(self, total_price, count, product, user, lang):
        try:
            if lang == 'uz':
                product_name_column = Basket.product_name_uz
            else:
                product_name_column = Basket.product_name_ru
            stmt = (
                update(Basket)
                .where(and_(product_name_column.label("product_name") == product, Basket.user_id == user))
                .values(total_price=total_price, count=count)
            )
            self.session.execute(stmt)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error updating basket data: {e}")
    def del_from_basket_one_product(self, user, product, lang):
        try:
            # Determine the correct column based on language
            if lang == 'uz':
                product_name_column = Basket.product_name_uz
            else:
                product_name_column = Basket.product_name_ru
            stmt = delete(Basket).where(and_(Basket.user_id == user,  product_name_column.label("product_name") == product))
            self.session.execute(stmt)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error deleting product from basket: {e}")
    def get_user_address(self, user_id):
        row = self.session.query(User.address).filter_by(user_id=user_id).first()
        return row.address if row else None
    def get_join_stats_today(self, today):
        return self.session.query(func.count(User.user_id)).filter(func.date(User.joined_date) == today).scalar()
    def get_join_stats_date_joins(self, date):
        return self.session.query(func.count(User.user_id)).filter(User.joined_date >= date).scalar()

    def get_total_users(self):
        return self.session.query(func.count(User.user_id)).scalar()
    def get_user_info_rasilka_excel(self):
        return self.session.query(
            User.phone_number,
            User.joined_date,
            User.address,
            User.long,

            User.lang,

        ).all()
    def add_categories_db(self, name_uz,  name_ru):
        category = Category(
            name_uz=name_uz,
            name_ru=name_ru
        )
        self.session.add(category)
        self.session.commit()

    def get_category_choosed(self, lang, category_name):
        if lang == "uz":
            category = self.session.query(Category).filter(
                (Category.name_uz == category_name)
            ).first()
        elif lang == "ru":
            category = self.session.query(Category).filter(
                (Category.name_ru == category_name)
            ).first()
        return category
    def delete_products(self, category_id):
        self.session.query(Product).filter_by(category_id=category_id).delete()
        self.session.commit()
    def delete_categories(self, category_id):
        self.session.query(Category).filter_by(id=category_id).delete()
        self.session.commit()
    def update_category_name(self, lang: str, new_name: str, current_name: str):
        """Update category name in specified language using SQLAlchemy.

        Args:
            lang: Language code ('uz' or 'ru')
            new_name: New category name
            current_name: Current category name to replace

        Returns:
            bool: True if update succeeded, False otherwise
        """
        session = self.session
        try:
            # Determine which column to update based on language
            column_to_update = Category.name_uz if lang == 'uz' else Category.name_ru

            # Create update statement
            stmt = (
                update(Category)
                .where(column_to_update == current_name)
                .values({column_to_update: new_name})
                .execution_options(synchronize_session="fetch")
            )

            # Execute the update
            result = session.execute(stmt)
            session.commit()



        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error updating category name: {e}")
            return False
        finally:
            session.close()
    def delete_products_by_name(self, name_uz):
        self.session.query(Product).filter_by(name_uz=name_uz).delete()
        self.session.commit()
    def add_products(self, category_id, name_uz, name_ru, price, image):
        product = Product(
            category_id=category_id,
            name_ru=name_ru,
            name_uz=name_uz,
            price=price,
            image=image

        )
        self.session.add(product)
        self.session.commit()
    def update_product(self, product_name, lang, update_data):
        """
        Update product fields dynamically using a dictionary.

        :param product_name: Name of the product to update
        :param lang: Language identifier for the column selection
        :param update_data: Dictionary of fields to update
        :return: Updated product object or None if product not found
        """
        try:
            name_column = getattr(Product, f"name_{lang}")

            product = self.session.query(Product).filter(name_column == product_name).first()
            if not product:
                return None  # Product not found

            for key, value in update_data.items():
                if hasattr(product, key):  # Ensure the attribute exists in the model
                    setattr(product, key, value)

            self.session.commit()
            return product  # Return the updated product object

        except SQLAlchemyError as e:
            self.session.rollback()  # Rollback in case of an error
            print(f"Error updating product {product_name}: {e}")  # Better to use logging
            return None  # Return None to indicate failure
    def add_order_items(self,order_id, product_name,product_item_cost, count, total_cost, user_id,branch_name, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()

        # # Convert time string to time object
        # clean_product_cost = int(product_item_cost.replace(' ', ''))
        # clean_delivery_cost = int(total_cost.replace(' ', ''))
        orders_item = OrderItem(
            order_id=order_id,
            product_name=product_name,
            product_item_cost=product_item_cost,
            count = count,
            total_cost=total_cost,
            user_id=user_id,
            branch_name=branch_name,
            date=date_obj
        )
        self.session.add(orders_item)
        self.session.commit()
    def get_sales_for_period(self, branch_name, start_dt, end_dt):
        """Core query for both reports"""
        return self.session.query(
            OrderItem.branch_name,
            OrderItem.product_name,
            func.sum(OrderItem.count).label('total_count'),
            func.max(OrderItem.product_item_cost).label('product_item_cost'),
            func.sum(OrderItem.total_cost).label('total_cost')
        ).filter(
            OrderItem.branch_name == branch_name,
            OrderItem.date >= start_dt,
            OrderItem.date <= end_dt,
        ).group_by(
            OrderItem.branch_name,
            OrderItem.product_name
        ).all()
    def get_sales_by_branch_and_date(self, branch_name):
        """Get sales for current full month (1st to last day)"""
        now = datetime.utcnow()
        first_day = datetime(now.year, now.month, 1)
        last_day = datetime(now.year, now.month + 1, 1) - timedelta(seconds=1)

        return self.get_sales_for_period(branch_name, first_day, last_day)
    def get_todays_sales_by_branch(self, branch_name):
        """Get today's sales for a specific branch.

        Args:
            branch_name: Name of the branch to filter by

        Returns:
            List of tuples containing (branch_name, product_name, total_count, product_item_cost, total_cost)
        """
        from datetime import datetime
        import pytz
        from sqlalchemy.exc import SQLAlchemyError
        from sqlalchemy import func

        utc_now = datetime.utcnow()
        uzbekistan_timezone = pytz.timezone('Asia/Tashkent')
        local_time = pytz.utc.localize(utc_now).astimezone(uzbekistan_timezone)
        today_date = local_time.date()

        try:
            results = self.session.query(
                OrderItem.branch_name,
                OrderItem.product_name,
                func.sum(OrderItem.count).label('total_count'),
                func.max(OrderItem.product_item_cost).label('product_item_cost'),  # ✅ to‘g‘rilandi
                func.sum(OrderItem.total_cost).label('total_cost')
            ).filter(
                OrderItem.branch_name == branch_name,
                func.date(OrderItem.date) == str(today_date),  # ☑️ extra safety with only date
            ).group_by(
                OrderItem.branch_name,
                OrderItem.product_name
            ).all()

            return results

        except SQLAlchemyError as e:
            print(f"Error fetching today's sales: {e}")
            return []
    def get_last_10_days_sales_by_branch(self, branch_name):
        from datetime import datetime, timedelta
        import pytz
        from sqlalchemy import func

        """Get sales for the last 10 days for a specific branch.

        Args:
            branch_name: Name of the branch to filter by

        Returns:
            String containing the formatted sales report
        """
        from sqlalchemy.exc import SQLAlchemyError

        # Define timezone
        utc_now = datetime.utcnow()
        uzbekistan_timezone = pytz.timezone('Asia/Tashkent')
        local_time = pytz.utc.localize(utc_now).astimezone(uzbekistan_timezone)
        today_date = local_time.date()

        # Get the date 10 days ago
        ten_days_ago = today_date - timedelta(days=10)

        try:
            # Query sales data for the last 10 days
            results = self.session.query(
                OrderItem.branch_name,
                OrderItem.product_name,
                func.sum(OrderItem.count).label('total_count'),
                func.max(OrderItem.product_item_cost).label('product_item_cost'),
                func.sum(OrderItem.total_cost).label('total_cost')
            ).filter(
                OrderItem.branch_name == branch_name,
                OrderItem.date >= ten_days_ago,
                OrderItem.date <= today_date
            ).group_by(
                OrderItem.branch_name,
                OrderItem.product_name
            ).order_by(OrderItem.date.asc()).all()

            # Format the results into the required report
            total_sales = 0
            report = f"📆 {ten_days_ago} > {today_date}\n\nOriginal {branch_name}\n\n"

            report += f"Jami ketgan mahsulotlar soni: {sum(r.total_count for r in results)}\n\n"

            for index, row in enumerate(results):
                product_name = row.product_name
                total_count = row.total_count
                product_item_cost = row.product_item_cost
                total_cost = row.total_cost
                report += f"{index + 1}) {product_name}\n"
                report += f"{total_count} x {product_item_cost:,.0f} so'm = {total_cost:,.0f} so'm\n\n".replace(",",
                                                                                                                " ")

                total_sales += total_cost

            # Calculate average price
            average_price = total_sales / sum(r.total_count for r in results) if results else 0
            report += f"Jami: {total_sales:,.0f} so'm\n".replace(",", " ")
            report += f"O'rtacha narx: {average_price:,.0f} so'm".replace(",", " ")

            return report

        except SQLAlchemyError as e:
            print(f"Error fetching sales data: {e}")
            return "Error fetching sales data."
    def get_product_onedate_filter(self, branch_name, user_input_date):
        from datetime import datetime
        import pytz


        # Accept both `08-04-2025` and `08.04.2025`
        try:
            if "-" in user_input_date:
                selected_date = datetime.strptime(user_input_date, "%d-%m-%Y").date()
            elif "." in user_input_date:
                selected_date = datetime.strptime(user_input_date, "%d.%m.%Y").date()
            else:
                return "❌ Noto‘g‘ri sana formati. Iltimos, '08-04-2025' yoki '08.04.2025' ko‘rinishida kiriting."

            # Query sales data for that specific date
            results = self.session.query(
                OrderItem.branch_name,
                OrderItem.product_name,
                func.sum(OrderItem.count).label('total_count'),
                func.max(OrderItem.product_item_cost).label('product_item_cost'),
                func.sum(OrderItem.total_cost).label('total_cost')
            ).filter(
                OrderItem.branch_name == branch_name,
                OrderItem.date == selected_date
            ).group_by(
                OrderItem.branch_name,
                OrderItem.product_name
            ).order_by(OrderItem.product_name.asc()).all()

            total_sales = 0
            total_items = sum(r.total_count for r in results)
            report = f"📆 {selected_date.strftime('%d-%m-%Y')}\n\n{branch_name}\n\n"
            report += f"Jami ketgan mahsulotlar soni: {total_items}\n\n"

            for index, row in enumerate(results):
                report += f"{index + 1}) {row.product_name}\n"
                report += f"{row.total_count} x {row.product_item_cost:,.0f} so'm = {row.total_cost:,.0f} so'm\n\n".replace(
                    ",", " ")
                total_sales += row.total_cost

            average_price = total_sales / total_items if total_items else 0
            report += f"Jami: {total_sales:,.0f} so'm\n".replace(",", " ")
            report += f"O'rtacha narx: {average_price:,.0f} so'm".replace(",", " ")

            return report

        except ValueError:
            return "❌ Sana noto‘g‘ri. Iltimos, '08-04-2025' yoki '08.04.2025' shaklida yozing."
        except SQLAlchemyError as e:
            print(f"Error fetching sales data: {e}")
            return "Xatolik yuz berdi, ma’lumotlar olinmadi."

    def get_sales_by_date_range(
            self,
            branch_name: str,
            start_date: datetime.date,
            end_date: datetime.date
    ):
        session = self.session
        try:
            results = session.query(
                OrderItem.branch_name,
                OrderItem.product_name,
                func.sum(OrderItem.count).label('count'),
                func.max(OrderItem.product_item_cost).label('price'),
                func.sum(OrderItem.total_cost).label('total')
            ).filter(
                OrderItem.branch_name == branch_name,
                OrderItem.date >= start_date,
                OrderItem.date <= end_date
            ).group_by(
                OrderItem.branch_name,
                OrderItem.product_name
            ).all()

            order_count = sum(item[2] for item in results)
            total_revenue = sum(item[4] for item in results)

            return {
                'orders': results,
                'requested_period': (start_date, end_date),
                'actual_period': (start_date, end_date),
                'order_count': order_count,
                'total_revenue': total_revenue
            }
        finally:
            session.close()
    def get_products(self, lang):
        """Get product categories in specified language.

        Args:
            lang: Language code ('uz', 'ru', or 'en')

        Returns:
            List of category names
        """
        lang = lang.lower()
        if lang not in ('uz', 'ru', 'en'):
            lang = 'en'  # Default to English

        column = getattr(Product, f"name_{lang}")
        print(column)
        try:
            categories = self.session.query(column).distinct().all()
            return [cat[0] for cat in categories if cat[0]]
        except SQLAlchemyError as e:
            print(f"Error fetching categories: {e}")
            return []
    def get_sales_by_branch_and_date_range_max(self, branch_name, start_date, end_date):

        from datetime import datetime
        from sqlalchemy import func, and_

        start_date = f'{start_date} 00:00:00'
        end_date = f'{end_date} 23:59:59'

        results = self.session.query(
            OrderItem.branch_name,
            OrderItem.product_name,
            func.sum(OrderItem.count).label('total_count'),
            func.max(OrderItem.product_item_cost).label('product_item_cost'),
            func.sum(OrderItem.total_cost).label('total_cost'),
            func.max(OrderItem.date).label('date')
        ).filter(
            and_(
                OrderItem.branch_name == branch_name,
                OrderItem.date >= start_date,
                OrderItem.date <= end_date
            )
        ).group_by(
            OrderItem.branch_name, OrderItem.product_name
        ).all()
        max_date = max((row.date for row in results), default=None)

        return max_date

    def generate_branch_stats(self, branch_names):
        # Set Uzbekistan timezone (UTC+5)
        uzbek_tz = timezone(timedelta(hours=5))
        now = datetime.now(uzbek_tz)
        current_month = now.month
        current_year = now.year

        try:
            # Query orders for all specified branches
            stmt = select(Order).where(
                and_(
                    extract('month', Order.date) == current_month,
                    extract('year', Order.date) == current_year,
                    or_(*[Order.branch_name == name for name in branch_names])
                )
            )

            orders = self.session.scalars(stmt).all()

            # Prepare data with total cost
            data = []
            for order in orders:
                try:
                    branch_value = getattr(order, 'branch_name',
                                           getattr(order, 'branch',
                                                   getattr(order, 'branchName', None)))

                    # Calculate total cost
                    total_cost = order.product_cost + order.delivery_cost

                    data.append({
                        'date': order.date,
                        'branch': branch_value,
                        'get_order_from': order.get_order_from,
                        'courier': order.courier,
                        'phone_number': order.phone_number,
                        'payment_type': order.payment_type,
                        'product_cost': order.product_cost,
                        'delivery_cost': order.delivery_cost,
                        'total_cost': total_cost,
                        'status': order.status,
                        'ordered': order.ordered,
                        'cooked': order.cooked,
                        'delivered': order.delivered,
                        'order_number': order.order_number
                    })
                except Exception as e:
                    print(f"Error processing order {order.id}: {str(e)}")
                    continue

            if not data:
                print("No orders found matching criteria")
                return []

            df = pd.DataFrame(data)

            # Generate separate Excel files for each branch
            result_files = []
            for branch_name in branch_names:
                try:
                    branch_df = df[df['branch'] == branch_name]

                    if branch_df.empty:
                        print(f"No orders found for branch: {branch_name}")
                        continue

                    # Create detailed stats with Uzbek column names
                    detailed_stats = branch_df[[
                        'date', 'get_order_from', 'courier', 'phone_number',
                        'payment_type', 'product_cost', 'delivery_cost',
                        'total_cost', 'ordered', 'cooked', 'delivered', 'order_number'
                    ]].rename(columns={
                        'date': 'Sana',
                        'get_order_from': 'Operator',
                        'payment_type': "To'lov turi",
                        'phone_number': 'Telefon raqami',
                        'courier': 'Kuryer',
                        'product_cost': 'Mahsulot narxi',
                        'delivery_cost': 'Yetkazish narxi',
                        'total_cost': 'Jami summa',
                        'ordered': 'Buyurtma vaqti',
                        'cooked': 'Tayyorlandi',
                        'delivered': 'Yetkazildi',
                        'order_number': 'Buyurtma raqami'
                    })



                    # Create final summary data with formatted numbers
                    if not branch_df.empty:
                        summary_data = [
                            ("📊 Jami buyurtmalar soni", "{:,.0f}".format(len(branch_df)).replace(",", " ")),
                            ("💰 O'rtacha mahsulot narxi",
                             "{:,.0f}".format(branch_df['product_cost'].mean()).replace(",", " ") + " so'm"),
                            ("📦 Jami mahsulot narxi",
                             "{:,.0f}".format(branch_df['product_cost'].sum()).replace(",", " ") + " so'm"),
                            ("🚚 O'rtacha yetkazish narxi",
                             "{:,.0f}".format(branch_df['delivery_cost'].mean()).replace(",", " ") + " so'm"),
                            ("📦 Jami yetkazish narxi",
                             "{:,.0f}".format(branch_df['delivery_cost'].sum()).replace(",", " ") + " so'm"),
                            ("💵 O'rtacha jami summa",
                             "{:,.0f}".format(branch_df['total_cost'].mean()).replace(",", " ") + " so'm"),
                            ("🏦 Jami summa",
                             "{:,.0f}".format(branch_df['total_cost'].sum()).replace(",", " ") + " so'm"),
                        ]
                    else:
                        summary_data = [
                            ("📊 Jami buyurtmalar soni", "0"),
                            ("💰 O'rtacha mahsulot narxi", "0 so'm"),
                            ("📦 Jami mahsulot narxi", "0 so'm"),
                            ("🚚 O'rtacha yetkazish narxi", "0 so'm"),
                            ("📦 Jami yetkazish narxi", "0 so'm"),
                            ("💵 O'rtacha jami summa", "0 so'm"),
                            ("🏦 Jami summa", "0 so'm"),
                        ]

                    # Convert summary data to DataFrame
                    summary_df = pd.DataFrame(summary_data, columns=["Ko'rsatkich", "Qiymat"])

                    filename = f"{branch_name}_statistika.xlsx".replace('/', '_')
                    with pd.ExcelWriter(filename, engine='openpyxl', mode='w') as writer:
                        detailed_stats.to_excel(writer, sheet_name='Statistika', index=False)
                        start_row = len(detailed_stats) + 3  # leave 2 rows of spacing
                        summary_df.to_excel(writer, sheet_name='Statistika', startrow=start_row, index=False)

                    result_files.append(filename)
                    print(f"{branch_name} uchun statistika yaratildi: {filename}")

                except Exception as e:
                    print(f"{branch_name} filialida xatolik: {str(e)}")
                    continue

            return result_files

        except Exception as e:
            print(f"Statistika yaratishda xatolik: {str(e)}")
            return []
    def get_all_admin_names(self) -> list[str]:
        admins = self.session.query(Admins).all()
        return [admin.name for admin in admins if admin.name]
    def delete_admin_by_name(self, name: str) -> bool:
        admin = self.session.query(Admins).filter_by(name=name).first()
        if admin:
            self.session.delete(admin)
            self.session.commit()
            return True
        return False


# SQLite()