from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

from tgbot.helpers.database import SQLite
# for calling text_repky
from tgbot.texts.text_reply import *

def reply_markup(texts, row_width=2, one_time_keyboard=False):
    """
    Create a ReplyKeyboardMarkup with the given texts.

    :param texts: List of button texts.
    :param row_width: Number of buttons per row.
    :return: ReplyKeyboardMarkup object.
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time_keyboard, row_width=row_width)
    markup.add(*texts)
    return markup

def reply_headers(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*order_btn[lang])
    markup.add(*header_button[lang])
    return markup

def get_social_inline():
    markup = InlineKeyboardMarkup(row_width=1)
    btn2 = InlineKeyboardButton("Instagram",
                                url="https://www.instagram.com/chef.street.bukhara?igsh=ZzRkN3RxZzEyNXI1")
    markup.add(btn2)
    return markup
def pickup_branches_btn(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    contact_button = KeyboardButton(text=pickup_bt[lang], request_location=True)
    markup.add(contact_button)
    markup.add(*pickup_branches_btns[lang])

    return markup
def get_categories(lang):
    db = SQLite()
    categories = db.get_categories(lang)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*back_btn[lang], *basket_btn_sub[lang])
    categories_list = []
    for category in categories:
        categories_list.append(category)
    markup.add(*categories_list)
    return markup

