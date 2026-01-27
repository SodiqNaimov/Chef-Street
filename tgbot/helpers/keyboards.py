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

def get_products_btn(lang, category_id):
    db = SQLite()
    # category = db.get_category_choosed(lang, category_name)
    products = db.get_product_names_by_category(category_id, lang)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*back_btn[lang], *basket_btn_sub[lang])

    products_list = []
    for i in products:
        products_list.append(i)
    markup.add(*products_list)
    return markup

def get_basket_user_data(lang, user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    markup.add(*basket_user_button[lang])
    db = SQLite()
    p_name = db.get_user_basket(user_id, lang)
    # print(p_name)

    sub_category_list = []
    for i in p_name:
        # print(i)
        if i[0] not in sub_category_list:
            sub_category_list.append('✏' + ' ' + i[0])
    markup.add(*sub_category_list, row_width=2)
    return markup
def change_basket_count(lang, name, tanlaganda):
    markup = InlineKeyboardMarkup()

    button_text = f"{tanlaganda}"
    button = InlineKeyboardButton(text=button_text, callback_data=str(name) + '_firs')

    button1 = InlineKeyboardButton(text='➖', callback_data='minus_product')
    button2 = InlineKeyboardButton(text='➕', callback_data='add_product')
    button3 = InlineKeyboardButton(text=back_inline_btn[lang], callback_data='back_basket')
    button5 = InlineKeyboardButton(text=inline_button_save[lang], callback_data=f'save_{tanlaganda}' + f'_{str(name)}')
    button6 = InlineKeyboardButton(text=enter_number[lang], callback_data=f'entern_{str(name)}')

    markup.add(button3)
    markup.add(button1, button, button2)
    markup.add(button6)
    markup.add(button5)
    return markup
def reply_phone_number(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*back_btn[lang])
    contact_button = KeyboardButton(text=get_contact_btn[lang], request_contact=True)
    markup.add(contact_button)
    return markup
def pickup_orders_btn(message, order_number):
    markup = InlineKeyboardMarkup(row_width=1)
    # _tasdiqlash
    markup.add(InlineKeyboardButton(text="✅ Buyurtmani qabul qilish", callback_data=f"tasdiqlash_{message.chat.id}_{order_number}"))
    return markup
def edit_basket_count(lang, name, tanlaganda):
    markup = InlineKeyboardMarkup()

    button_text = f"{tanlaganda}"
    button = InlineKeyboardButton(text=button_text, callback_data=name + '_f')
    button4 = InlineKeyboardButton(text=inline_button[lang], callback_data=f"del_{name}")

    button1 = InlineKeyboardButton(text='➖', callback_data='previous')
    button2 = InlineKeyboardButton(text='➕', callback_data='next')
    button3 = InlineKeyboardButton(text=back_inline_btn[lang], callback_data='basket_back')
    button5 = InlineKeyboardButton(text=inline_button_save[lang], callback_data=f'saves_{tanlaganda}' + f'_{name}')
    markup.add(button3)
    markup.add(button4)

    markup.add(button1, button, button2)
    markup.add(button5)
    return markup