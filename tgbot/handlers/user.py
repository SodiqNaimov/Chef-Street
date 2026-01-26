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
count = {}

uzbekistan_phone_prefix = '+998'
uzbekistan_phone_prefix_no = '998'

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
    closest_location_name, closest_location_km =find_closest_location((Latitude, Longitude), user_language)
    print(closest_location_name)
    print(closest_location_km)

    state.add_data(branch=closest_location_name)
    bot.send_message(message.from_user.id,
                     pickup_location_text[user_language].format(closest_location_name, closest_location_km))
    bot.send_message(message.from_user.id, category_text[user_language], reply_markup=get_categories(user_language))
    state.set(MyStates.menu_func_st)

def back_menu_func(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    db = SQLite()
    db.delete_basket_data(message.from_user.id)
    bot.send_message(message.from_user.id, order_type_text[user_language],
                     reply_markup=reply_markup(order_type_btn[user_language], 2))
    state.set(MyStates.order_func_st)
def products_user(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    db = SQLite()
    row = db.get_category_id_by_name(message.text, user_language)

    state.add_data(category = row)
    if row:
        bot.send_message(message.from_user.id, choose_one_from_products[user_language], reply_markup=get_products_btn(user_language, row))
        state.set(MyStates.products_menu_st)
    else:
        bot.send_message(message.from_user.id, please_choose_one[user_language], reply_markup=get_categories(user_language))
        state.set(MyStates.menu_func_st)

def basket_function(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    db = SQLite()
    rows = db.get_user_basket(message.from_user.id, user_language)
    # if is_bot_active():
    if len(rows) == 0:
        bot.send_message(message.from_user.id, basket_dont_exists[user_language], reply_markup=get_categories(user_language))
        state.set(MyStates.menu_func_st)
    else:
        distance = return_data(message, bot, 'closest_km')
        print(distance)
        order_type = return_data(message, bot, 'order_type')
        if order_type in ['🚶 Borib olish', '🚶 Самовывоз']:
            text, formatted_number2 = check_pickup(rows, user_language)
            basket_text = basket_count_pickup_message[user_language].format(text, formatted_number2)
        else:
            text, formatted_number2, delivery_cost = check(rows, user_language, distance)

            basket_text = basket_count_message[user_language].format(text,delivery_cost, formatted_number2)

        bot.send_message(message.chat.id, basket_text, reply_markup=get_basket_user_data(user_language, message.from_user.id))
        state.set(MyStates.basket_user_st)

def back_basket_function(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    bot.send_message(message.from_user.id, category_text[user_language], reply_markup=get_categories(user_language))
    state.set(MyStates.menu_func_st)

def delete_basket(message: Message, bot: TeleBot, state: StateContext, user_language: str):
    db = SQLite()
    db.delete_basket_data(message.chat.id)
    bot.send_message(message.from_user.id, basket_deleted_text[user_language], reply_markup=get_categories(user_language))
    state.set(MyStates.menu_func_st)

def show_product(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    db = SQLite()
    rows = db.get_products_by_name(message.text, user_language)
    state.add_data(product = message.text)
    print(state.get())
    category = return_data(message, bot, 'category')

    if rows:
        m = bot.send_message(message.from_user.id, header_txt[user_language], reply_markup=remove_keyboard)
        bot.delete_message(message.chat.id, m.message_id)
        count[message.from_user.id] = 1  # Initialize as integer 1 instead of dictionary
        bot.send_photo(message.from_user.id, rows[2], caption=product_info_txt[user_language].format(message.text, rows[1], 1, rows[1], rows[1]), reply_markup=change_basket_count(user_language, rows[3], 1))
        state.set(MyStates.none_st)
        # db.get_products_by_name()
    else:
        bot.send_message(message.from_user.id, please_choose_one[user_language], reply_markup=get_products_btn(user_language, category))
        state.set(MyStates.products_menu_st)
def back_products_user(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    bot.send_message(message.from_user.id, category_text[user_language], reply_markup=get_categories(user_language))
    state.set(MyStates.menu_func_st)

def product_basket(message: Message, bot: TeleBot, state: StateContext, user_language: str):
    db = SQLite()
    rows = db.get_user_basket(message.from_user.id, user_language)
    # if is_bot_active():
    if len(rows) == 0:
        bot.send_message(message.from_user.id, basket_dont_exists[user_language], reply_markup=get_products_btn(user_language, return_data(message, bot, 'category')))
        state.set(MyStates.products_menu_st)
    else:
        distance = return_data(message, bot, 'closest_km')
        order_type = return_data(message, bot, 'order_type')

        if order_type in ['🚶 Borib olish', '🚶 Самовывоз']:
            text, formatted_number2 = check_pickup(rows, user_language)
            basket_text = basket_count_pickup_message[user_language].format(text, formatted_number2)
        else:
            text, formatted_number2, delivery_cost = check(rows, user_language, distance)

            basket_text = basket_count_message[user_language].format(text, delivery_cost, formatted_number2)

        bot.send_message(message.chat.id, basket_text, reply_markup=get_basket_user_data(user_language, message.from_user.id))
        state.set(MyStates.basket_user_st)

def back_products_info(call: CallbackQuery, bot: TeleBot,  state: StateContext):
    db = SQLite()
    count[call.from_user.id] = 1  # Initialize as integer 1 instead of dictionary

    user_language = db.get_user_lang(call.from_user.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        category = data['category']
    bot.send_message(call.from_user.id, choose_one_from_products[user_language], reply_markup=get_products_btn(user_language, category))
    state.set(MyStates.products_menu_st)
def add_or_minus_product(call: CallbackQuery, bot: TeleBot):
    boolean = False if call.data=='minus_product' else True
    handle_product_count_change(call, bot, is_increase=boolean)

def handle_product_count_change(call: CallbackQuery, bot: TeleBot, is_increase: bool):
    number = 1 if not is_increase else 101
    condition = count[call.from_user.id] > number if not is_increase else count[call.from_user.id] < number
    if condition:
        count[call.message.chat.id] += 1 if is_increase else -1
        tanlaganda = count[call.message.chat.id]
        print(tanlaganda)
        db = SQLite()
        user_language = db.get_user_lang(call.from_user.id)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            product = data['product']
        row = db.get_products_by_name(product, user_language)
        name, price, photo_id = row[0], row[1], row[2]
        quantity = int(tanlaganda)
        price_clean = str(row[1]).replace(" ", "").replace(",", "")
        raw_price = float(price_clean)
        total_price = quantity * raw_price
        formatted_total = "{:,.0f}".format(total_price).replace(",", " ")
        description_to_photo = product_info_txt[user_language].format(name, price, tanlaganda, price, formatted_total)
        markup = change_basket_count(user_language, row[3], tanlaganda)
        bot.edit_message_media(
            chat_id=call.message.chat.id,
            media=InputMediaPhoto(photo_id, caption=description_to_photo, parse_mode="HTML"),
            message_id=call.message.message_id,
            reply_markup=markup
        )
def save(call: CallbackQuery, bot: TeleBot):
    _, son, nom = call.data.split("_", 2)
    print(nom)# Split with max 2 splits
    db = SQLite()
    lang = db.get_user_lang(call.from_user.id)

    # Get product data
    product_info = db.get_product_by_id(nom, lang)

    name = product_info["name"]
    print(name)
    price_str = product_info["price"]
    image = product_info["image"]
    pr_id = product_info["id"]
    name_ru = product_info["name_ru"]
    print(name_ru)

    print(price_str)

    price = int(price_str.replace(" ", ""))
    total_price = int(son) * price

    # Basket operations
    basket = db.get_user_basket(call.from_user.id, lang)
    if not basket or all(item[0] != name for item in basket):
        if lang == 'uz':
            db.insert_basket(call.from_user.id, name, son, price, total_price, name_ru)
        else:
            db.insert_basket(call.from_user.id, name_ru, son, price, total_price, name)
    else:
        for item in basket:
            if item[0] == name:
                updated_count = int(item[1]) + int(son)
                updated_total = int(item[3]) + total_price
                db.update_basket_item(call.from_user.id, name, updated_count, updated_total, lang)

    # Cleanup and response
    bot.delete_message(call.message.chat.id, call.message.message_id)  # Fixed: using message_id instead of chat.id

    bot.send_message(
        call.message.chat.id,  # Using the same chat where the callback came from
        info_about_set_basket[lang].format(name, son),
        reply_markup=get_categories(lang)
    )
    bot.set_state(call.from_user.id, MyStates.menu_func_st, call.message.chat.id)
def enter_number_by_handle(call: CallbackQuery, bot: TeleBot, state: StateContext):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    product_id = call.data.split("_")[1]
    state.add_data(product_id=product_id)
    db = SQLite()
    lang = db.get_user_lang(call.from_user.id)
    bot.send_message(call.from_user.id, enter_number_txt[lang], reply_markup=reply_markup(back_btn[lang], 1))
    state.set(MyStates.enter_number_by_handle_st)

def back_enter_number_by_handle(message: Message, bot: TeleBot, state: StateContext, user_language: str):
    row = return_data(message, bot, 'category')
    count[message.from_user.id] = 1  # Initialize as integer 1 instead of dictionary

    bot.send_message(message.from_user.id, choose_one_from_products[user_language],
                     reply_markup=get_products_btn(user_language, row))
    state.set(MyStates.products_menu_st)
def add_enter_number(message: Message, bot: TeleBot, state: StateContext, user_language: str):
    if message.text.isdigit():
        db = SQLite()
        nom = return_data(message, bot, 'product')

        product_info = db.get_products_by_name(nom, user_language)
        son = message.text
        name_uz = product_info[0]
        price_str = product_info[1]
        image = product_info[2]
        pr_id = product_info[3]
        name_ru = product_info[4]
        print("NOM :", nom)
        basket = db.get_user_basket(message.from_user.id, user_language)
        price = int(price_str.replace(" ", ""))
        total_price = int(son) * price
        for item in basket:
            print("ITEM:", item[0])

            if item[0] == nom:
                print("ITEM:", item[0])

        print(not basket or all(item[0] != nom for item in basket))
        if not basket or all(item[0] != nom for item in basket):
            print('this')
            if user_language == 'uz':
                db.insert_basket(message.from_user.id, name_uz, son, price, total_price, name_ru)
            else:
                db.insert_basket(message.from_user.id, name_ru, son, price, total_price, name_uz)

        else:
            print('this must work')
            for item in basket:
                if item[0] == nom:
                    print("ITEM:", item[0])

                    updated_count = int(item[1]) + int(son)
                    updated_total = int(item[3]) + total_price
                    db.update_basket_item(message.from_user.id, nom, updated_count, updated_total, user_language)
        bot.send_message(
            message.chat.id,  # Using the same chat where the callback came from
            info_about_set_basket[user_language].format(nom, son),
            reply_markup=get_categories(user_language)
        )
        state.set(MyStates.menu_func_st)
    else:
        bot.send_message(message.from_user.id, please_in_int_enter[user_language], reply_markup=reply_markup(back_btn[user_language], 1))
        state.set(MyStates.enter_number_by_handle_st)

@only_between_11_and_00_simple
def confirm_order(message: Message, bot: TeleBot, state: StateContext):
    db = SQLite()
    lang = db.get_user_lang(message.from_user.id)
    bot.send_message(message.from_user.id, send_contact[lang], reply_markup=reply_phone_number(lang))
    state.set(MyStates.confirm_order_st)

def back_confirm_order(message: Message, bot: TeleBot, state: StateContext, user_language: str):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        distance = data['closest_km']
    db = SQLite()
    rows = db.get_user_basket(message.chat.id, user_language)
    order_type = return_data(message, bot, 'order_type')
    if order_type in ['🚶 Borib olish', '🚶 Самовывоз']:
        text, formatted_number2 = check_pickup(rows, user_language)
        basket_text = basket_count_pickup_message[user_language].format(text, formatted_number2)
    else:
        text, formatted_number2, formatted_number3 = check(rows, user_language, distance)

        basket_text = basket_count_message[user_language].format(text, formatted_number3, formatted_number2)
    bot.send_message(message.chat.id,
                     basket_text,
                     reply_markup=get_basket_user_data(user_language, message.chat.id))
    state.set(MyStates.basket_user_st)

def handle_contacts_update(message: Message, bot: TeleBot, user_language: str, state: StateContext):
    if message.contact.phone_number.startswith(uzbekistan_phone_prefix_no) or message.contact.phone_number.startswith(
            uzbekistan_phone_prefix):
        if message.contact.phone_number.startswith(uzbekistan_phone_prefix_no):
            phone_numbers = f"+{message.contact.phone_number}"
        else:
            phone_numbers = message.contact.phone_number
        state.add_data(phone_number=phone_numbers)

        bot.send_message(message.from_user.id, comment_txt[user_language], reply_markup=reply_markup(comment_btn[user_language], 1))
        state.set(MyStates.comments_st)

def handle_text_message(message: Message, bot: TeleBot, state: StateContext, user_language: str):
    phone_number = message.text.strip()
    try:
        int(message.text)
    except Exception as e:
        bot.send_message(message.from_user.id, contact_int[user_language], reply_markup=reply_phone_number(user_language))
        state.set(MyStates.confirm_order_st)
    else:
        if len(phone_number) != 13:
            bot.send_message(message.from_user.id, send_contact[user_language], reply_markup=reply_phone_number(user_language))
            state.set(MyStates.confirm_order_st)
        else:
            if phone_number.startswith(uzbekistan_phone_prefix) or phone_number.startswith(uzbekistan_phone_prefix_no):
                if phone_number.startswith(uzbekistan_phone_prefix_no):
                    phone_numbers = f"+{phone_number}"
                else:
                    phone_numbers = phone_number
                state.add_data(phone_number=phone_numbers)
                bot.send_message(message.from_user.id, comment_txt[user_language],
                                 reply_markup=reply_markup(comment_btn[user_language], 1))
                state.set(MyStates.comments_st)
            else:
                bot.send_message(message.from_user.id, please_only_uzb_number[user_language], reply_markup=reply_phone_number(user_language))
                state.set(MyStates.confirm_order_st)

def comments_txt(message: Message, bot: TeleBot, state: StateContext, user_language: str):
    if message.text in ["➡️ Keyingi", "➡️ Далее"]:
        state.add_data(comments = '-')
        bot.send_message(message.from_user.id, payment_type_txt[user_language], reply_markup=reply_markup(payment_types[user_language], 2))
        state.set(MyStates.payment_type_st)
    elif message.text in ["⬅️ Ortga", "⬅️ Назад"]:
        bot.send_message(message.from_user.id, send_contact[user_language], reply_markup=reply_phone_number(user_language))
        state.set(MyStates.confirm_order_st)
    else:
        state.add_data(comments= message.text)
        bot.send_message(message.from_user.id, payment_type_txt[user_language], reply_markup=reply_markup(payment_types[user_language], 2))
        state.set(MyStates.payment_type_st)

def payment_cash(message: Message, bot: TeleBot, state: StateContext, user_language: str):
    state.add_data(payment = message.text)
    bot.send_message(message.from_user.id, last_confirm[user_language], reply_markup=reply_markup(last_confirm_btn[user_language], 2))
    state.set(MyStates.confirm_last_st)

def back_payment(message: Message, bot: TeleBot, state: StateContext, user_language: str):
    bot.send_message(message.from_user.id, comment_txt[user_language],
                     reply_markup=reply_markup(comment_btn[user_language], 1))
    state.set(MyStates.comments_st)