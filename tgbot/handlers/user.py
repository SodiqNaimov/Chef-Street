from telebot import TeleBot
from telebot.types import *  # ReplyKeyboardRemove, CallbackQuery
# for state
from telebot.states.sync.context import StateContext
# for define states
from tgbot.states.state import Register, MyStates
# messages
from tgbot.texts.messages import *

# for use keyboards
from tgbot.helpers.keyboards import *  # , inline_markup
from tgbot.texts.text_reply import *

# for use database
from tgbot.helpers.database import SQLite
# for smaller function
remove_keyboard = ReplyKeyboardRemove(selective=True)
from tgbot.helpers.small_function import *
a_q = {}
def start_func(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    is_registered = db.is_registered(message.from_user.id)

    if message.text != "/start" and "/start" in message.text:
        try:
            a_q[message.chat.id] = message.text.split(' ')[1]
            bot.send_message(message.chat.id, "Savol uchun javobni yuboring:",
                             reply_markup=reply_markup(['◀️ Ortga'], 1))
            state.set(MyStates.get_answer)
        except:
            pass
    elif is_registered:
        user_language = db.get_user_lang(message.from_user.id)
        bot.send_message(message.from_user.id, headers_message[user_language],
                         reply_markup=reply_headers(user_language))
        state.set(MyStates.headers_st)
    else:
        bot.send_message(message.from_user.id,
                         msg_start.format(message.from_user.first_name, message.from_user.first_name),
                         reply_markup=reply_markup(lang_msg, 2))
        state.set(Register.lang_st)
def language(message: Message, bot: TeleBot, state: StateContext):
    if message.text in lang_msg:
        lang = set_user_lang(message.text)
        state.add_data(lang=lang)
        bot.send_message(message.from_user.id, get_name_message[lang], reply_markup=remove_keyboard)
        state.set(Register.full_name_st)

def get_full_name(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    lang = return_data(message, bot, 'lang')
    db.register_user(message.from_user.id,lang, message.text)
    bot.send_message(message.from_user.id, headers_message[lang], reply_markup=reply_headers(lang))
    state.set(MyStates.headers_st)
def contacts_func(message: Message, bot: TeleBot, state: StateContext, user_language: str):
    bot.send_message(message.chat.id, contact_branches_second[user_language], reply_markup=reply_headers(user_language))
    state.set(MyStates.contacts_st)
def header(message: Message, bot: TeleBot,user_language: str, state: StateContext):
    bot.send_message(message.from_user.id, headers_message[user_language], reply_markup=reply_headers(user_language))
    state.set(MyStates.headers_st)
def social_media(message: Message, bot: TeleBot, user_language: str,  state: StateContext):
    bot.send_message(message.chat.id, social_media_message[user_language], reply_markup=get_social_inline())
    header(message, bot, user_language, state)

def location_func(message: Message, bot: TeleBot, user_language: str,  state: StateContext):
    bot.send_location(message.chat.id, 39.781011, 64.403939)
    bot.send_message(message.chat.id, location_message[user_language])
    header(message, bot, user_language, state)

def settings_func(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    bot.send_message(message.from_user.id, settings_message[user_language],
                     reply_markup=reply_markup(settings_button[user_language], 2))
    state.set(MyStates.settings_st)
def change_language(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    bot.send_message(message.from_user.id, update_language_message[user_language], reply_markup=reply_markup(lang_msg, 2))
    state.set(MyStates.change_language_st)


def update_language(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    if message.text in lang_msg:
        db.update_user(message.from_user.id, {"lang": set_user_lang(message.text)})  # ✅ Deactivate subscription
    start_func(message, bot, state)

def back_contacts_function(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    header(message, bot, user_language, state)

def complaint_func(message: Message, bot: TeleBot, user_language: str,  state: StateContext):
    bot.send_message(message.chat.id, choose_complaint_message[user_language], reply_markup=reply_markup(back_btn[user_language], 2))
    state.set(MyStates.complaint_branch_st)

def send_group_complaint(message: Message, bot: TeleBot, user_language: str,  state: StateContext):
    if message.content_type in ['voice', 'text']:
        db = SQLite()
        mention = mention_or_silka(message)
        full_name, phone_number = db.get_user_info(message.from_user.id)
        print(full_name)
        print(phone_number)
        user_complaint = f"<b>👤 Telegram account: {mention}</b>\n"
        user_complaint += f"<b>👤 Mijoz Ism Familyasi: {full_name}</b>\n"
        if phone_number:
            user_complaint += f"📞 {phone_number}\n"
        referral_link = f"https://t.me/{bot.get_me().username}?start={message.chat.id}"

        user_complaint += f"\n<a href='{referral_link}'>✉️ Javob qaytarish</a>"

        caption = message.caption if message.caption else None
        bot.send_message(message.chat.id, successful_send_text[user_language])
        header(message, bot, user_language, state)
        if message.voice:
            if message.caption:
                caption = f"{caption}\n\n{user_complaint}"

                bot.copy_message(chat_id=-1003871440267, from_chat_id=message.from_user.id, message_id=message.message_id, caption=caption, )
            else:
                caption = f"{user_complaint}"

                bot.copy_message(chat_id=-1003871440267, from_chat_id=message.from_user.id, message_id=message.message_id, caption=caption)

        else:
            caption = f"{message.text}\n\n{user_complaint}"

            bot.send_message(-1003871440267,caption)

    else:
        bot.send_message(message.from_user.id, complaint_type_complaint_not[user_language],  reply_markup=reply_markup(back_btn[user_language], 2))
        state.set(MyStates.complaint_branch_st)
def get_answer(message: Message, bot: TeleBot,user_language: str,  state: StateContext):
    if message.text == '◀️ Ortga':
        start_func(message, bot, state)
    else:
        db = SQLite()
        lang = db.get_user_lang(a_q[message.chat.id])
        bot.send_message(a_q[message.chat.id], answer_to_question[lang].format(message.text))
        bot.send_message(message.chat.id, 'Javobingiz yuborildi')
        header(message, bot, user_language, state)

def order_func(message: Message, bot: TeleBot,user_language: str,  state: StateContext):
    bot.send_message(message.from_user.id, order_type_text[user_language],  reply_markup=reply_markup(order_type_btn[user_language], 2))
    state.set(MyStates.order_func_st)

def pickup_func(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    state.add_data(order_type=message.text)
    bot.send_message(message.from_user.id, location_text[user_language], reply_markup=pickup_branches_btn(user_language))
    state.set(MyStates.pickup_func_st)

def back_pickup_func(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    bot.send_message(message.from_user.id, order_type_text[user_language],  reply_markup=reply_markup(order_type_btn[user_language], 2))
    state.set(MyStates.order_func_st)
def menu_func(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    state.add_data(branch=message.text)
    bot.send_message(message.from_user.id, category_text[user_language], reply_markup=get_categories(user_language))
    state.set(MyStates.menu_func_st)

def pickup_location(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    Latitude = message.location.latitude
    Longitude = message.location.longitude
    closest_location_name = find_closest_location((Latitude, Longitude), user_language)[0]
    closest_location_km = find_closest_location((Latitude, Longitude), user_language)[1]
    state.add_data(branch=closest_location_name)
    bot.send_message(message.from_user.id,
                     pickup_location_text[user_language].format(closest_location_name, round(closest_location_km)))
    bot.send_message(message.from_user.id, category_text[user_language], reply_markup=get_categories(user_language))
    state.set(MyStates.menu_func_st)

def back_menu_func(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    db = SQLite()
    db.delete_basket_data(message.from_user.id)
    bot.send_message(message.from_user.id, order_type_text[user_language],
                     reply_markup=reply_markup(order_type_btn[user_language], 2))
    state.set(MyStates.order_func_st)
