from telebot import TeleBot
from telebot.types import *  # ReplyKeyboardRemove, CallbackQuery

# for state
from telebot.states.sync.context import StateContext

from tgbot.helpers.small_function import statistics_join, return_data, set_user_lang, set_user_flag_lang, check_admin_pr
from tgbot.states.state import Panel

# messages
from tgbot.texts.admin_message import *

# for use keyboards
from tgbot.helpers.keyboards import *  # , inline_markup
from tgbot.texts.text_reply import *

# for use database
from tgbot.helpers.database import SQLite

import pandas as pd
import time
def open_admin(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    admin_ids_raw = db.get_all_admin_id()
    admin_ids = [int(admin_id[0]) for admin_id in admin_ids_raw]  # превращаем в [123, 456, ...]
    print(admin_ids)
    if message.from_user.id in admin_ids:
        print('yes')
        bot.send_message(
            message.from_user.id,
            welcome_admin_text.format(message.from_user.first_name),
            reply_markup=reply_markup(admin_btn, 2)
        )
        state.set(Panel.open_admin_st)
def users_count(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    today, week, month = statistics_join()
    all_users = db.get_total_users()

    text = (f"Bugungi botga a'zo bo'lganlar soni: <b>{today}</b>\n\n"
            f"Haftalik botga a'zo bo'lganlar soni: <b>{week}</b>\n\n"
            f"Oylik botga a'zo bo'lganlar soni: <b>{month}</b>\n\n"
            f"Umumiy Foydalanuvchilar soni: <b>{all_users}</b>ta")

    bot.send_message(message.chat.id, text)
    open_admin(message, bot, state)
def information_about_user(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    rows = db.get_user_info_rasilka_excel()

    # Create a DataFrame from the query results
    df = pd.DataFrame(rows,
                      columns=['Mijoz telefon raqami', "Mijoz obuna bo'lgan sanasi", "Mijoz Addressi", "Longitude",
                               "Latitude"])

    # Format phone numbers as strings in "XXX-XXX-XXXX" format
    df['Mijoz telefon raqami'] = df['Mijoz telefon raqami'].astype(str).str.replace(r'(\d{3})(\d{3})(\d{4})',
                                                                                    r'\1-\2-\3')
    # Create an Excel writer with customizations
    excel_file = 'info.xlsx'
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = workbook.add_worksheet('Welcome')

    # Define cell formats for header, data, and index
    header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
    data_format = workbook.add_format({'bg_color': '#FFFFFF'})
    index_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})

    # Write the header, index, and data to the worksheet
    header_row = df.columns.tolist()
    data_rows = df.values.tolist()
    worksheet.write_row(0, 1, header_row, header_format)
    for row_num, row_data in enumerate(data_rows, start=1):
        worksheet.write_row(row_num, 1, row_data, data_format)

    # Write the index column starting from 1
    index_col = df.index.tolist()
    worksheet.write_column(1, 0, [i + 1 for i in index_col], index_format)

    # Set column widths based on content
    for i, column in enumerate(df.columns, start=1):
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        worksheet.set_column(i, i, column_width)

    # Close the writer after saving
    writer.close()

    # Close the database connection

    # Send the Excel file
    with open(excel_file, 'rb') as file:
        bot.send_document(message.chat.id, file)

    open_admin(message, bot, state)

def send_rassilka(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, rasilka_txt, reply_markup=reply_markup(["⬅️ Ortga"], 1))
    state.set(Panel.send_rassilka_st)


def back_send_rassilka(message: Message, bot: TeleBot, state: StateContext):
    open_admin(message, bot, state)


def rassilka(message: Message, bot: TeleBot, state: StateContext):
    state.add_data(m_id=message.message_id)
    if message.caption:
        state.add_data(m_caption=message.caption)
    bot.reply_to(message, "Shu xabarni yuborishni tasdiqlaysizmi?")
    bot.send_message(message.from_user.id, "Tasdiqlash?", reply_markup=reply_markup(["✅ Ha", "❌ Yo'q"], 1))
    state.set(Panel.confirm_rasilka_st)


def confirm_rasilka(message: Message, bot: TeleBot, state: StateContext):
    if message.text == "❌ Yo'q":
        open_admin(message, bot, state)
    else:
        m_id = return_data(message, bot, 'm_id')
        try:
            m_caption = return_data(message, bot, 'm_caption')
        except Exception as e:
            print(e)
        print(m_caption)
        db = SQLite()
        rows = db.send_user_message()
        success = 0
        removed = 0
        start_time = time.time()
        for user_id in rows:
            try:
                success += 1
                if m_caption:
                    bot.copy_message(user_id, from_chat_id=message.chat.id, message_id=m_id,
                                     caption=m_caption)
                else:
                    bot.copy_message(user_id, from_chat_id=message.chat.id, message_id=m_id)
            except Exception as e:
                removed += 1
                # print(removed)
                print(e)
        execution_time = time.time() - start_time
        minutes, seconds = divmod(execution_time, 60)
        all_send_users = success - removed

        bot.send_message(message.chat.id, f"✅ Xabar <b>{all_send_users}</b> ta foydalanuvchiga yetkazildi.\n\n"
                                          f"❌ <b>{removed}</b> ta foydalanuvchi botni bloklagan\n\n🕐 Reklamaga yuborishda jami ketgan vaqt:  <b>{int(minutes)} minut</b> <b>{round(seconds, 2)} second </b> vaqt ketdi")

        open_admin(message, bot, state)

def categories_and_products(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "Quyidagilardan birini tanlang",
                     reply_markup=reply_markup(categories_and_products_btn, 2))
    state.set(Panel.categories_and_products_st)

def categories_func(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "Quyidagilardan birini tanlang",
                     reply_markup=reply_markup(categories_panel_btn, 2))
    state.set(Panel.categories_func_st)


def back_categories_func(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "Quyidagilardan birini tanlang",
                     reply_markup=reply_markup(categories_and_products_btn, 2))
    state.set(Panel.categories_and_products_st)

def add_categories(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, f"Kategoriyaning {uz_ru_flags[0]} nomini yuboring",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.add_categories_st)


def back_add_categories(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "Quyidagilardan birini tanlang",
                     reply_markup=reply_markup(categories_panel_btn, 2))
    state.set(Panel.categories_func_st)
def add_categories_ru(message: Message, bot: TeleBot, state: StateContext):
    state.add_data(categorie_uz=message.text)
    bot.send_message(message.from_user.id, f"Kategoriyaning {uz_ru_flags[1]} nomini yuboring",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.add_categories_ru)
def back_add_categories_ru(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, f"Kategoriyaning {uz_ru_flags[0]} nomini yuboring",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.add_categories_st)


def add_categories_to_database(message: Message, bot: TeleBot, state: StateContext):
    categorie_uz = return_data(message, bot, 'categorie_uz')
    db = SQLite()
    db.add_categories_db(categorie_uz, message.text)
    bot.send_message(message.from_user.id, f"Yangi {categorie_uz}/{message.text} kategoriyasi qo'shildi")
    state.delete()
    open_admin(message, bot, state)

def delete_categories(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "O'chirmoqchi bo'lgan kategoriyani tanlang.",
                     reply_markup=admin_categories('uz'))
    state.set(Panel.delete_categories_st)


def ask_delete_categories(message: Message, bot: TeleBot, state: StateContext):
    state.add_data(categories=message.text)
    bot.send_message(message.from_user.id, f"{message.text} kategoriyasini o'chirmoqchimisiz?",
                     reply_markup=reply_markup(confirm_or_not, 2))
    state.set(Panel.ask_delete_categories_st)
def confirm_or_not_func(message: Message, bot: TeleBot, state: StateContext):
    if message.text == "❌ Yo'q":
        bot.send_message(message.from_user.id, "O'chirmoqchi bo'lgan kategoriyani tanlang.",
                         reply_markup=admin_categories('uz'))
        state.set(Panel.delete_categories_st)
    else:
        db = SQLite()
        rows = db.get_category_choosed('uz', return_data(message, bot, 'categories'))
        db.delete_products(rows.id)
        db.delete_categories(rows.id)
        bot.send_message(message.from_user.id,
                         f"<b>{return_data(message, bot, 'categories')}</b> kategoriyasi o'chirildi.")
        state.delete()

        open_admin(message, bot, state)

def change_categories(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    categories = db.get_categories('uz')
    if categories:
        bot.send_message(message.from_user.id, "O'zgartirmoqchi bo'lgan kategoriyaning tilini tanlang.",
                         reply_markup=reply_markup(lang_msg_with_btn, 2))
        state.set(Panel.change_categories_st)
    else:
        bot.send_message(message.from_user.id, "Sizda hali kategoriya mavjud emas.",
                         reply_markup=reply_markup(categories_panel_btn, 2))
        state.set(Panel.categories_func_st)


def change_categories_lang(message: Message, bot: TeleBot, state: StateContext):
    if message.text in lang_msg:
        lang = set_user_lang(message.text)
        state.add_data(lang=lang)
        bot.send_message(message.from_user.id, "O'zgartirmoqchi bo'lgan kategoriyani tanlang",
                         reply_markup=admin_categories(lang))
        state.set(Panel.change_categories_lang_st)

def back_add_change_categories_lang(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "O'zgartirmoqchi bo'lgan kategoriyaning tilini tanlang.",
                     reply_markup=reply_markup(lang_msg_with_btn, 2))
    state.set(Panel.change_categories_st)
def ask_new_name(message: Message, bot: TeleBot, state: StateContext):
    state.add_data(categories=message.text)
    lang = set_user_flag_lang(return_data(message, bot, 'lang'))
    bot.send_message(message.from_user.id, f"{message.text} uchun {lang} nomini yuboring.",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.ask_new_name_st)
def back_ask_new_name(message: Message, bot: TeleBot, state: StateContext):
    lang = return_data(message, bot, 'lang')
    bot.send_message(message.from_user.id, "O'zgartirmoqchi bo'lgan kategoriyani tanlang",
                     reply_markup=admin_categories(lang))
    state.set(Panel.change_categories_lang_st)


def change_ask_new_name(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    lang = return_data(message, bot, 'lang')
    categories = return_data(message, bot, 'categories')

    db.update_category_name(lang, message.text, categories)
    bot.send_message(message.from_user.id, f"{categories} nomi {message.text} ga o'zgardi")
    state.delete()
    open_admin(message, bot, state)
def products_admin(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "Quyidagilardan birini tanlang",
                     reply_markup=reply_markup(products_panel_btn, 2))
    state.set(Panel.products_admin_st)
def delete_products(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "O'chirmoqchi bo'lgan mahsulot nomini tanlang.",
                     reply_markup=admin_products('uz'))
    state.set(Panel.delete_products_st)


def ask_delete_products(message: Message, bot: TeleBot, state: StateContext):
    state.add_data(product_name=message.text)
    bot.send_message(message.from_user.id, f"{message.text} mahsulotini o'chirmoqchimisiz?",
                     reply_markup=reply_markup(confirm_or_not, 2))
    state.set(Panel.ask_delete_products_st)


def confirm_delete_pr_not_products(message: Message, bot: TeleBot, state: StateContext):
    if message.text == "❌ Yo'q":
        bot.send_message(message.from_user.id, "O'chirmoqchi bo'lgan mahsulot nomini tanlang.",
                         reply_markup=admin_products('uz'))
        state.set(Panel.delete_products_st)
    else:
        db = SQLite()
        db.delete_products_by_name(return_data(message, bot, 'product_name'))
        bot.send_message(message.from_user.id,
                         f"{return_data(message, bot, 'product_name')} mahsuloti bazadan o'chirildi")
        state.delete()
        open_admin(message, bot, state)
def back_products_add_admin(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "Quyidagilardan birini tanlang",
                     reply_markup=reply_markup(products_panel_btn, 2))
    state.set(Panel.products_admin_st)
def products_add_admin(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "Mahsulot qo'shish uchun kategoriyalardan birini tanlang",
                     reply_markup=admin_categories('uz'))
    state.set(Panel.products_add_admin_st)

def add_product_name(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    rows = db.get_category_choosed('uz', message.text)

    state.add_data(categories=rows.id)
    bot.send_message(message.from_user.id, f"Mahsulot uchun {uz_ru_flags[0]} nomini kiriting",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.add_product_name_st)

def back_add_product_name(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "Mahsulot qo'shish uchun kategoriyalardan birini tanlang",
                     reply_markup=admin_categories('uz'))
    state.set(Panel.products_add_admin_st)


def add_product_name_ru(message: Message, bot: TeleBot, state: StateContext):
    state.add_data(product_name_uz=message.text)
    bot.send_message(message.from_user.id, f"Mahsulot uchun {uz_ru_flags[1]} nomini kiriting",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.add_product_name_ru_st)


def back_add_product_name_ru(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, f"Mahsulot uchun {uz_ru_flags[0]} nomini kiriting",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.add_product_name_st)
def add_price_product(message: Message, bot: TeleBot, state: StateContext):
    state.add_data(product_name_ru=message.text)
    bot.send_message(message.from_user.id, "Mahsulotning narxini kiriting",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.add_price_product_st)


def back_add_price_product(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, f"Mahsulot uchun {uz_ru_flags[1]} nomini kiriting",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.add_product_name_ru_st)

def add_image_product(message: Message, bot: TeleBot, state: StateContext):
    if message.text.isdigit():
        state.add_data(price=message.text)
        bot.send_message(message.from_user.id, "Mahsulotning rasmini yuboring",
                         reply_markup=reply_markup(back_btn['uz'], 1))
        state.set(Panel.add_image_product_st)
    else:
        bot.send_message(message.from_user.id, "Iltimos mahsulot narxini faqat raqamlarda yuboring",
                         reply_markup=reply_markup(back_btn['uz'], 1))
        state.set(Panel.add_product_name_ru_st)


def back_add_image_product(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "Mahsulotning narxini kiriting",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.add_price_product_st)

def add_products_database(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    with state.data() as data:
        categories = data.get('categories')
        product_name_uz = data.get('product_name_uz')
        product_name_ru = data.get('product_name_ru')
        price = data.get('price')

    db.add_products(categories, product_name_uz, product_name_ru, price, message.photo[-1].file_id)
    bot.send_message(message.from_user.id, f"Yangi <b>{product_name_uz}/{product_name_ru}</b> mahsuloti qo'shildi.")
    state.delete()
    open_admin(message, bot, state)
def change_products(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "O'zgartirmoqchi bo'lgan mahsulotingizning tilini tanlang",
                     reply_markup=reply_markup(lang_msg_with_btn, 2))
    state.set(Panel.change_products_st)


def choose_lange_change_product(message: Message, bot: TeleBot, state: StateContext):
    if message.text in lang_msg:
        lang = set_user_lang(message.text)
        state.add_data(lang=lang)
        bot.send_message(message.from_user.id, "Quyidagi mahsulotlardan birini tanlang",
                         reply_markup=admin_products(lang))
        state.set(Panel.choose_lange_change_product)

def back_choose_lange_change_product(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "O'zgartirmoqchi bo'lgan mahsulotingizning tilini tanlang",
                     reply_markup=reply_markup(lang_msg_with_btn, 2))
    state.set(Panel.change_products_st)

def choose_edit_btn(message: Message, bot: TeleBot, state: StateContext):
    state.add_data(edit_product=message.text)
    bot.send_message(message.from_user.id, "Quyidagilardan birini tanlang", reply_markup=reply_markup(edit_btn, 1))
    state.set(Panel.choose_edit_btn_st)
def back_choose_edit_btn(message: Message, bot: TeleBot, state: StateContext):
    lang = return_data(message, bot, 'lang')
    bot.send_message(message.from_user.id, "Quyidagi mahsulotlardan birini tanlang", reply_markup=admin_products(lang))
    state.set(Panel.choose_lange_change_product)
def price_choose_edit_btn(message: Message, bot: TeleBot, state: StateContext):
    edit_product = return_data(message, bot, 'edit_product')
    db = SQLite()
    rows = db.get_products_by_name(edit_product, 'uz')
    bot.send_message(message.from_user.id,
                     f"<b>{edit_product}</b> uchun yangi narx kiriting.\n\n<b>{edit_product}</b>ning eski narxi: <b>{rows[1]}</b>",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.price_choose_edit_btn_st)


def back_price_choose_edit_btn(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "Quyidagilardan birini tanlang", reply_markup=reply_markup(edit_btn, 1))
    state.set(Panel.choose_edit_btn_st)


def change_price(message: Message, bot: TeleBot, state: StateContext):
    if message.text.isdigit():
        edit_product = return_data(message, bot, 'edit_product')
        lang = return_data(message, bot, 'lang')

        db = SQLite()
        db.update_product(edit_product, lang, {"price": message.text})
        bot.send_message(message.from_user.id, f"<b>{edit_product}</b> mahsulot narxi {message.text}ga o'zgardi.")
        open_admin(message, bot, state)
    else:
        bot.send_message(message.from_user.id, price_in_int, reply_markup=reply_markup(back_btn['uz'], 1))
        state.set(Panel.price_choose_edit_btn_st)

def price_image_edit_btn(message: Message, bot: TeleBot, state: StateContext):
    edit_product = return_data(message, bot, 'edit_product')

    bot.send_message(message.from_user.id, f"<b>{edit_product}</b> uchun yangi rasm yuboring.",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.price_image_edit_btn)


def change_image_from_db(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    edit_product = return_data(message, bot, 'edit_product')
    lang = return_data(message, bot, 'lang')

    db.update_product(edit_product, lang, {"image": message.photo[-1].file_id})
    bot.send_message(message.from_user.id, f"<b>{edit_product}</b> mahsulot rasmi o'zgardi.")
    open_admin(message, bot, state)

def change_name_product(message: Message, bot: TeleBot, state: StateContext):
    edit_product = return_data(message, bot, 'edit_product')

    bot.send_message(message.from_user.id, f"<b>{edit_product}</b> uchun yangi nom yuboring.",
                     reply_markup=reply_markup(back_btn['uz'], 1))
    state.set(Panel.change_name_product_st)
def change_from_db_name(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    edit_product = return_data(message, bot, 'edit_product')
    lang = return_data(message, bot, 'lang')
    name_ch = {f"name_{lang}": message.text} if lang in ["uz", "ru"] else {}

    db.update_product(edit_product, lang, name_ch)
    bot.send_message(message.from_user.id, f"<b>{edit_product}</b> mahsulot rasmi o'zgardi.")
    open_admin(message, bot, state)


def statistica(message: Message, bot: TeleBot, state: StateContext):
    bot.send_message(message.from_user.id, "Kerakli statistikani tanlang.",
                     reply_markup=reply_markup(statistics_btn, 2))
    state.set(Panel.statistica_st)

def products_statistika(message: Message, bot: TeleBot, state: StateContext):
    """Prompt user to select a date range for statistics"""
    bot.send_message(
        message.from_user.id,
        "Sanani yuboring masalan: 01-01-2025\n\nYoki «📆 Bugungi sana» yoki «📆 Bugungi oy» tugmalaridan birini tanlang.",
        reply_markup=reply_markup(today_btn, 1)
    )
    state.set(Panel.products_statistika_st)

def back_statistica(message: Message, bot: TeleBot, state: StateContext):
    """Return to statistics menu"""
    bot.send_message(
        message.from_user.id,
        "Kerakli statistikani tanlang.",
        reply_markup=reply_markup(statistics_btn, 2)
    )
    state.set(Panel.statistica_st)
def get_end_time(message: Message, bot: TeleBot, state: StateContext):
    if message.text == "📆 Bugungi oy":
        sales_data1 = SQLite().get_sales_by_branch_and_date("Original Xot Dog Yunusobod")
        # print(sales_data1)
        sales_data2 = SQLite().get_sales_by_branch_and_date("Original Xot Dog Ibn Sino")
        print(sales_data2)
        sales_data1, total_cost1, total_count, average_sum = check_admin_pr(sales_data1)
        sales_data2, total_cost2, total_count2, average_sum2 = check_admin_pr(sales_data2)
        if sales_data1:
            bot.send_message(message.from_user.id,
                             f"📆 Oylik statistika\n\nOriginal Xot Dog Yunusobod\n\nJami ketgan mahsulotlar soni: <b>{total_count}</b>\n\n{sales_data1}Jami: {total_cost1}\nO'rtacha narx: {average_sum}")
        if sales_data2:
            bot.send_message(message.from_user.id,
                             f"📆 Oylik statistika\n\nOriginal Xot Dog Ibn Sino\n\nJami ketgan mahsulotlar soni: <b>{total_count2}</b>\n\n{sales_data2}Jami: {total_cost2}\nO'rtacha narx: {average_sum2}")


        open_admin(message, bot, state)
    elif message.text == "📆 Bugungi sana":
        sales_data1 = SQLite().get_todays_sales_by_branch("Original Xot Dog Yunusobod")
        sales_data2 = SQLite().get_todays_sales_by_branch("Original Xot Dog Ibn Sino")
        utc_now = datetime.utcnow()
        uzbekistan_timezone = pytz.timezone('Asia/Tashkent')
        local_time = pytz.utc.localize(utc_now).astimezone(uzbekistan_timezone)
        today_date = local_time.date()

        print(sales_data2)
        sales_data1, total_cost1, total_count, average_sum = check_admin_pr(sales_data1)
        sales_data2, total_cost2, total_count2, average_sum2 = check_admin_pr(sales_data2)
        if sales_data1:
            bot.send_message(message.from_user.id,
                             f"📆 {today_date}\n\nOriginal Xot Dog Yunusobod\n\nJami ketgan mahsulotlar soni: <b>{total_count}</b>\n\n{sales_data1}Jami: {total_cost1}\nO'rtacha narx: {average_sum}")
        if sales_data2:
            bot.send_message(message.from_user.id,
                             f"📆 {today_date}\n\nOriginal Xot Dog Ibn Sino\n\nJami ketgan mahsulotlar soni: <b>{total_count2}</b>\n\n{sales_data2}Jami: {total_cost2}\nO'rtacha narx: {average_sum2}")
        open_admin(message, bot, state)
    elif message.text == "📆 10 kunlik":
        # send_sales_report_to_telegram(message, bot, "Original Xot Dog Ibn Sino")
        db = SQLite()
        report = db.get_last_10_days_sales_by_branch("Original Xot Dog Ibn Sino")
        report2 = db.get_last_10_days_sales_by_branch("Original Xot Dog Yunusobod")

        if report:
            bot.send_message(message.chat.id, report)
        if report2:
            bot.send_message(message.chat.id, report2)
        open_admin(message, bot, state)
    elif message.text == "📆 Sanani kiritish":
        bot.send_message(message.from_user.id, "Filtrlab olmoqchi bo'lgan sanani kiriting masalan: 01-12-2025.", reply_markup=reply_markup(back_btn['uz'], 1))
        state.set(Panel.get_one_filter_product_date_st)
    else:
        state.add_data(start_date=datetime.strptime(message.text, '%d-%m-%Y').date())
        print(datetime.strptime(message.text, '%d-%m-%Y').date())
        bot.send_message(message.from_user.id,
                         "Tugash sananisini yuboring masalan: 01-12-2025.",
                         reply_markup=reply_markup(back_btn['uz'], 1))
        state.set(Panel.get_end_time_statistics_st)
