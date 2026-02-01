from telebot import TeleBot
from telebot.types import *  # ReplyKeyboardRemove, CallbackQuery

# for state
from telebot.states.sync.context import StateContext

from tgbot.helpers.small_function import statistics_join, return_data
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