import telebot
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from telebot.states.sync.middleware import StateMiddleware

#For calling commands
from tgbot.Filters.admin_commands import set_commands
# For calling token
from tgbot.files.config import token
#For calling admin dashboard
from tgbot.handlers.admin import *
#For calling user's dashboard
from tgbot.handlers.user import *
#For calling LanguageMiddleware like i18
from tgbot.Middleware.middleware import LanguageMiddleware
#For calling filter admins
from tgbot.Filters.admin_filter import AdminFilter

import logging


# After deploying uncomment this.
# # Set up logging
# logging.basicConfig(
#     filename='bot.log',       # Log file name
#     filemode='a',             # Append to the log file
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
#     level=logging.INFO        # Log level
# )
#
# logger = logging.getLogger(__name__)

# After deploying comment this.
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

# Initialize the bot
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token, state_storage=state_storage, parse_mode='HTML', num_threads=5, use_class_middlewares = True)




# To shorten the "register_message_handler" code
def register_m_handler(func, state=None, text=None, commands=None, admin=None):
    return bot.register_message_handler(func, text=text, state=state, commands=commands, admin=admin, pass_bot=True)



def register_handlers():
    ###########Admins
    register_m_handler(open_admin, commands=['admin'])
    register_m_handler(new_status, commands=['status'])
    bot.register_callback_query_handler(get_admin_name, func=lambda call: call.data.startswith('status_admin_'), pass_bot=True)
    bot.register_callback_query_handler(back_to_status, func=lambda call: call.data == "ortga_status", pass_bot=True)
    register_m_handler(add_admine, state=Panel.status_st)
    bot.register_callback_query_handler(bekor_status, func=lambda call: call.data == "bekor_status", pass_bot=True)

    #Register
    register_m_handler(start_func, commands=['start'])
    register_m_handler(language, text=lang_msg, state=Register.lang_st)
    register_m_handler(get_full_name, state=Register.full_name_st)

    #Order
    register_m_handler(order_func, text = ["🛍 Buyurtma berish", "🛍 Заказать"], state=MyStates.headers_st)
    register_m_handler(header, text = ["⬅️ Ortga", "⬅️ Назад", "⬅️ Back"], state=MyStates.order_func_st)

    register_m_handler(delivery_func, text=['🚙 Yetkazib berish', '🚙 Доставка'], state=MyStates.order_func_st)
    register_m_handler(back_pickup_func, text=["⬅️ Ortga", "⬅️ Назад"],state=MyStates.delivery_func_st)
    register_m_handler(deliveryss_branch_func, text=for_main_btn, state=MyStates.delivery_func_st)
    register_m_handler(back_delivery_func, text=["⬅️ Ortga", "⬅️ Назад"],state=MyStates.deliveryss_branch_func_st)

    bot.register_message_handler(get_location_by_handle, state=MyStates.deliveryss_branch_func_st, content_types=['location'],
                                 pass_bot=True)
    register_m_handler(back_get_location_by_handle, text=["⬅️ Ortga", "⬅️ Назад"], state=MyStates.not_home_handle_st)
    register_m_handler(send_again_error, text=["📍 Manzilni Qayta Yuborish 🔄", "📍 Повторная Отправка Адреса 🔄"],
                       state=MyStates.not_home_handle_st)

    bot.register_message_handler(confirm_location, state=MyStates.delivery_func_st, content_types=['location'],
                                 pass_bot=True)

    register_m_handler(back_pickup_func, text=["⬅️ Ortga", "⬅️ Назад"], state=MyStates.not_home_st)
    register_m_handler(delivery_func, text=["📍 Manzilni Qayta Yuborish 🔄", "📍 Повторная Отправка Адреса 🔄"],
                       state=MyStates.not_home_st)

    register_m_handler(back_confirm_location, text=["❌ Yo'q", "❌ Нет", "⬅️ Ortga", "⬅️ Назад"],
                       state=MyStates.confirm_location_st)
    register_m_handler(delivery_menu_func, text=["✅ Ha", "✅ Да"], state=MyStates.confirm_location_st)

    register_m_handler(my_addresses_func, text=["🗺 Mening manzillarim", "🗺 Мои адреса"],
                       state=MyStates.delivery_func_st)
    register_m_handler(back_delivery_address_func, text=["⬅️ Ortga", "⬅️ Назад"], state=MyStates.my_addresses_func_st)
    register_m_handler(address_user_func, state=MyStates.my_addresses_func_st)

    register_m_handler(pickup_func, text = ['🚶 Borib olish', '🚶 Самовывоз'], state=MyStates.order_func_st)
    register_m_handler(back_pickup_func, text = ["⬅️ Ortga", "⬅️ Назад", "⬅️ Back"], state=MyStates.pickup_func_st)
    register_m_handler(menu_func, text = ["📍 Chef Street Koloxoz","📍 Chef Street Колхоз"],
                       state=MyStates.pickup_func_st)
    bot.register_message_handler(pickup_location, state=MyStates.pickup_func_st, content_types=['location'],
                                 pass_bot=True)
    register_m_handler(back_menu_func, text=["⬅️ Ortga", "⬅️ Назад"], state=MyStates.menu_func_st)
    register_m_handler(basket_function, text=["🛒 Savat", "🛒 Корзина"], state=MyStates.menu_func_st)
    register_m_handler(back_basket_function,text=["⬅️ Ortga", "⬅️ Назад"], state=MyStates.basket_user_st)
    #Product
    register_m_handler(products_user, state=MyStates.menu_func_st)
    register_m_handler(delete_basket, text=["♻️ Savatni tozalash", '♻️ Очистить корзину'],
                       state=MyStates.basket_user_st)
    register_m_handler(confirm_order, text=["✅ Buyurtmani tasdiqlash", '✅ Подтвердить заказ'], state=MyStates.basket_user_st)
    register_m_handler(back_confirm_order, text=["⬅️ Ortga", "⬅️ Назад"], state= MyStates.confirm_order_st)
    bot.register_message_handler(handle_contacts_update,content_types=['contact'], state= MyStates.confirm_order_st,pass_bot=True)
    register_m_handler(handle_text_message, state= MyStates.confirm_order_st)
    register_m_handler(comments_txt, state= MyStates.comments_st)
    register_m_handler(back_payment,text=["⬅️ Ortga", "⬅️ Назад"], state=MyStates.payment_type_st)

    register_m_handler(payment_cash, text=['💵 Naqd', '💵 Наличные'], state=MyStates.payment_type_st)
    register_m_handler(click_payment, text=['💳 Click','💳 Payme'], state=MyStates.payment_type_st)
    register_m_handler(back_from_online_payment,text=["⬅️ Ortga", "⬅️ Назад"],state=MyStates.click_payment_st )
    register_m_handler(cancel_order, text=["❌ Rad etish", "❌ Отклонить"], state=MyStates.confirm_last_st)
    register_m_handler(accept_order, text=["✅ Tasdiqlash", "✅ Подтвердить"], state=MyStates.confirm_last_st)

    bot.register_message_handler(successful_payment_payme, content_types=['successful_payment'], pass_bot=True)


    register_m_handler(back_products_user,text=["⬅️ Ortga", "⬅️ Назад"], state=MyStates.products_menu_st)
    register_m_handler(product_basket, text=["🛒 Savat", "🛒 Корзина"], state=MyStates.products_menu_st)
    register_m_handler(update_product_user, state=MyStates.basket_user_st)

    register_m_handler(show_product, state= MyStates.products_menu_st)


    #Enter count
    register_m_handler(back_enter_number_by_handle, text=["⬅️ Ortga", "⬅️ Назад"], state=MyStates.enter_number_by_handle_st)
    register_m_handler(add_enter_number, state=MyStates.enter_number_by_handle_st)

    #Contact
    register_m_handler(contacts_func, text = ["📞️ Kontaktlar", "📞️ Контакты", "📞️ Contacts"], state=MyStates.headers_st)
    # social_media
    register_m_handler(social_media, text = ["📲 Ijtimoiy tarmoqlar", "📲 Социальные сети", "📲 Social networks"],
                       state=MyStates.headers_st)
    # location
    register_m_handler(location_func, text=["📍 Kafe Lokatsiyasi", "📍 Расположение Кафе", "📍 Location of the Restaurant"],
                       state=MyStates.headers_st)

    #####Settings
    register_m_handler(settings_func, text = ["⚙️ Sozlamalar", "⚙️ Настройки"], state=MyStates.headers_st)
    register_m_handler(back_contacts_function, text = ["⬅️ Ortga", "⬅️ Назад"], state=MyStates.settings_st)

    # Change Language
    register_m_handler(change_language, text = ["🌐 Tilni tanlash", "🌐 Выбрать язык", "🌐 Choose a language"], state=MyStates.settings_st)
    register_m_handler(update_language, text=lang_msg, state=MyStates.change_language_st)

    register_m_handler(complaint_func,
                       text = ["✍ Taklif va Shikoyatlar", "✍️Предложения и Жалобы", "✍ Suggestions and Complaints"],
                       state=MyStates.headers_st)
    register_m_handler(start_func, text = ["⬅️ Ortga", "⬅️ Назад", "⬅️ Back"], state=MyStates.complaint_branch_st)
    register_m_handler(send_group_complaint,state=MyStates.complaint_branch_st)
    register_m_handler(open_admin, commands=['admin'])
    register_m_handler(get_answer, state=MyStates.get_answer)

    #Callback
    bot.register_callback_query_handler(back_products_info, func=lambda call: call.data == "back_basket", pass_bot=True)
    bot.register_callback_query_handler(
        add_or_minus_product,
        func=lambda call: call.data in ('minus_product', 'add_product'),
        pass_bot=True
    )
    bot.register_callback_query_handler(admin_otkaz, func=lambda call: call.data.endswith("_otkaz"), pass_bot=True)
    bot.register_callback_query_handler(tasdiq, func=lambda call: call.data.endswith("_tasdiqlash"), pass_bot=True)
    bot.register_callback_query_handler(finish_user, func=lambda call: call.data.endswith("_tugatildi"), pass_bot=True)

    bot.register_callback_query_handler(save, func=lambda call: call.data.startswith("save_"), pass_bot=True)
    bot.register_callback_query_handler(enter_number_by_handle, func=lambda call: call.data.startswith("entern_"), pass_bot=True)
    bot.register_callback_query_handler(previous_and_next, func=lambda call: call.data in ('previous', 'next'), pass_bot=True)
    bot.register_callback_query_handler(delete_basket_from_inline, func=lambda call: call.data.startswith("del_"),
                                        pass_bot=True)
    bot.register_callback_query_handler(save_edit_basket, func=lambda call: call.data.startswith("saves_"), pass_bot=True)
    bot.register_callback_query_handler(back_from_basket, func=lambda call: call.data == "basket_back", pass_bot=True)
    bot.register_pre_checkout_query_handler(pre_checkout_query,func=lambda query: True,pass_bot=True)

    register_m_handler(users_count, text="👤 Foydalanuvchilar soni", state=Panel.open_admin_st)
    register_m_handler(information_about_user, text="👤 Foydalanuvchilar haqida ma'lumot", state=Panel.open_admin_st)
    register_m_handler(send_rassilka, text="✏️ Foydalanuvchilarga xabar yuborish", state=Panel.open_admin_st)
    register_m_handler(back_send_rassilka, text="⬅️ Ortga", state=Panel.send_rassilka_st)
    register_m_handler(rassilka, state=Panel.send_rassilka_st)
    register_m_handler(confirm_rasilka, text=["✅ Ha", "❌ Yo'q"], state=Panel.confirm_rasilka_st)


    register_m_handler(categories_and_products, text=["Mahsulotlar va Categoriyalar"], state=Panel.open_admin_st)
    register_m_handler(back_send_rassilka, text="⬅️ Ortga", state=Panel.categories_and_products_st)
    ###########Categories
    register_m_handler(categories_func, text=["Categoriyalar"], state=Panel.categories_and_products_st)
    register_m_handler(back_categories_func, text="⬅️ Ortga", state=Panel.categories_func_st)
    #############Add categories
    register_m_handler(add_categories, text="➕ Categoriya qo'shish", state=Panel.categories_func_st)
    register_m_handler(back_add_categories, text="⬅️ Ortga", state=Panel.add_categories_st)
    register_m_handler(add_categories_ru, state=Panel.add_categories_st)
    register_m_handler(back_add_categories_ru, text="⬅️ Ortga", state=Panel.add_categories_ru)
    register_m_handler(add_categories_to_database, state=Panel.add_categories_ru)
    ###################Delete categories
    register_m_handler(delete_categories,text="❌ Categoriyani o'chirish", state=Panel.categories_func_st)
    register_m_handler(back_add_categories, text="⬅️ Ortga", state=Panel.delete_categories_st)
    register_m_handler(ask_delete_categories, state=Panel.delete_categories_st)
    register_m_handler(confirm_or_not_func, text=confirm_or_not, state=Panel.ask_delete_categories_st)
    ###################Change categories
    register_m_handler(change_categories,text="🔄 Categoriyani o'zgartirish", state=Panel.categories_func_st)
    register_m_handler(back_add_categories, text="⬅️ Ortga", state=Panel.change_categories_st)
    register_m_handler(change_categories_lang, text=lang_msg, state=Panel.change_categories_st)
    register_m_handler(back_add_change_categories_lang, text="⬅️ Ortga", state=Panel.change_categories_lang_st)
    register_m_handler(ask_new_name, state=Panel.change_categories_lang_st)
    register_m_handler(back_ask_new_name, text="⬅️ Ortga", state=Panel.ask_new_name_st)
    register_m_handler(change_ask_new_name, state=Panel.ask_new_name_st)
    ###########Products
    register_m_handler(products_admin, text=["Mahsulotlar"], state=Panel.categories_and_products_st)
    register_m_handler(back_categories_func, text="⬅️ Ortga", state=Panel.products_admin_st)
    #############Delete products
    register_m_handler(delete_products, text="❌ Mahsulotni o'chirish", state=Panel.products_admin_st)
    register_m_handler(back_products_add_admin, text="⬅️ Ortga", state=Panel.delete_products_st)
    register_m_handler(ask_delete_products,  state=Panel.delete_products_st)
    register_m_handler(confirm_delete_pr_not_products, text=confirm_or_not, state=Panel.ask_delete_products_st)
    #############Add products
    register_m_handler(products_add_admin, text="➕ Mahsulot qo'shish", state=Panel.products_admin_st)
    register_m_handler(back_products_add_admin, text="⬅️ Ortga", state=Panel.products_add_admin_st)
    register_m_handler(add_product_name,  state=Panel.products_add_admin_st)
    register_m_handler(back_add_product_name, text="⬅️ Ortga", state=Panel.add_product_name_st)
    register_m_handler(add_product_name_ru,  state=Panel.add_product_name_st)
    register_m_handler(back_add_product_name_ru, text="⬅️ Ortga", state=Panel.add_product_name_ru_st)
    register_m_handler(add_price_product,  state=Panel.add_product_name_ru_st)
    register_m_handler(back_add_price_product, text="⬅️ Ortga", state=Panel.add_price_product_st)
    register_m_handler(add_image_product,  state=Panel.add_price_product_st)
    register_m_handler(back_add_image_product, text="⬅️ Ortga", state=Panel.add_image_product_st)
    bot.register_message_handler(add_products_database, state=Panel.add_image_product_st,content_types=['photo'],pass_bot=True)
    #############Change products
    register_m_handler(change_products, text="🔄 Mahsulotni o'zgartirish", state=Panel.products_admin_st)
    register_m_handler(back_products_add_admin, text="⬅️ Ortga", state=Panel.change_products_st)
    register_m_handler(choose_lange_change_product, text=lang_msg, state=Panel.change_products_st)
    register_m_handler(back_choose_lange_change_product, text="⬅️ Ortga", state=Panel.choose_lange_change_product)
    register_m_handler(choose_edit_btn,  state=Panel.choose_lange_change_product)
    register_m_handler(back_choose_edit_btn, text="⬅️ Ortga", state=Panel.choose_edit_btn_st)
    #############Change price
    register_m_handler(price_choose_edit_btn, text="💰 Mahsulot narxini o'zgartirish", state=Panel.choose_edit_btn_st)
    register_m_handler(back_price_choose_edit_btn, text="⬅️ Ortga", state=Panel.price_choose_edit_btn_st)
    register_m_handler(change_price, state=Panel.price_choose_edit_btn_st)
    #############Change image
    register_m_handler(price_image_edit_btn, text="🗾 Mahsulot rasmini o'zgartirish", state=Panel.choose_edit_btn_st)
    register_m_handler(back_price_choose_edit_btn, text="⬅️ Ortga", state=Panel.price_image_edit_btn)
    bot.register_message_handler(change_image_from_db, state=Panel.price_image_edit_btn, content_types=['photo'], pass_bot=True)
    #############Change name
    register_m_handler(change_name_product, text="✏️ Mahsulot nomini o'zgartirish",  state=Panel.choose_edit_btn_st)
    register_m_handler(back_price_choose_edit_btn, text="⬅️ Ortga", state=Panel.change_name_product_st)
    register_m_handler(change_from_db_name,  state=Panel.change_name_product_st)

    register_m_handler(statistica, text="📊 Statistika", state=Panel.open_admin_st)
    register_m_handler(back_send_rassilka, text="⬅️ Ortga", state=Panel.statistica_st)
    register_m_handler(products_statistika, text= "Mahsulotlar statistikasi", state=Panel.statistica_st)
    register_m_handler(back_statistica, text="⬅️ Ortga", state=Panel.products_statistika_st)
    #
    register_m_handler(get_end_time,  state=Panel.products_statistika_st)
    register_m_handler(back_get_end_time, text="⬅️ Ortga", state=Panel.get_end_time_statistics_st)
    register_m_handler(back_get_end_time, text="⬅️ Ortga", state=Panel.get_one_filter_product_date_st)
    register_m_handler(send_one_filtered_date, state=Panel.get_one_filter_product_date_st)
    register_m_handler(send_product_with_end_time, state=Panel.get_end_time_statistics_st)

    register_m_handler(branch_statistics, text= "Filliallar statistikasi", state=Panel.statistica_st)
    register_m_handler(back_statistica, text="⬅️ Ortga", state=Panel.branch_statistics_st)
    register_m_handler(get_this_month_branch_statistics, state=Panel.branch_statistics_st)
    register_m_handler(back_get_this_month_branch_statistics, text="⬅️ Ortga", state=Panel.get_one_filter_branch_date_st)
    register_m_handler(back_get_this_month_branch_statistics, text="⬅️ Ortga", state=Panel.get_end_time_branch_st)
    register_m_handler(filter_one_date_filter_branch, state=Panel.get_one_filter_branch_date_st)

    register_m_handler(send_branch_statistics, state=Panel.get_end_time_branch_st)

    register_m_handler(average_count, text= "O'rtacha narx", state=Panel.statistica_st)
    register_m_handler(back_statistica, text="⬅️ Ortga", state=Panel.average_count_st)
    register_m_handler(get_start_avaerage_count, state=Panel.average_count_st)
    register_m_handler(back_get_start_avaerage_count, text="⬅️ Ortga", state=Panel.get_start_avaerage_count_st)
    register_m_handler(back_get_start_avaerage_count, text="⬅️ Ortga", state=Panel.get_one_average_sum_st)
    register_m_handler(process_daily_date_input, state=Panel.get_one_average_sum_st)

    register_m_handler(send_end_date_avaerage_count, state=Panel.get_start_avaerage_count_st)


    register_m_handler(admins_func, text="👨‍💻 Adminlar bo'limi", state=Panel.open_admin_st)
    register_m_handler(back_send_rassilka, text="⬅️ Ortga", state=Panel.admins_func_st)
    register_m_handler(list_of_admins, text="👁 Adminlar ro'yxatini ko'rish", state=Panel.admins_func_st)
    register_m_handler(delete_admin_by_name, text="🗑 Adminni o'chirish", state=Panel.admins_func_st)
    register_m_handler(admins_func, text="⬅️ Ortga", state=Panel.delete_admin_by_name_st)
    register_m_handler(ask_delete_admin,state=Panel.delete_admin_by_name_st )
    register_m_handler(delete_or_not,text=["✅ Ha", "❌ Yo'q"],state=Panel.ask_delete_admin_st )


def run():
    bot.infinity_polling(skip_pending=True, logger_level=logging.INFO)


register_handlers()
# custom filters
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.IsDigitFilter())
# Pass bot instance and any required arguments here
bot.add_custom_filter(AdminFilter())

# necessary for state parameter in handlers.
bot.setup_middleware(LanguageMiddleware(bot))
bot.setup_middleware(StateMiddleware(bot))
if __name__ == "__main__":
    set_commands(bot)
    run()


