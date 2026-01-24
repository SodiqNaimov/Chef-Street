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
    #Register
    register_m_handler(start_func, commands=['start'])
    register_m_handler(language, text=lang_msg, state=Register.lang_st)
    register_m_handler(get_full_name, state=Register.full_name_st)
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

# For commands
set_commands(bot)

# Start polling
run()
