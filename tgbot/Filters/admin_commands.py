from telebot import TeleBot
from telebot.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from tgbot.helpers.database import SQLite

db = SQLite()

# admins = [db.select_all_admin()]

admins = [866489508, 766158313]


def set_commands(bot: TeleBot) -> None:
    # Default commands (all users)
    default_commands = [
        BotCommand(
            command="start",
            description="Botni ishga tushirish"
        ),
    ]
    bot.set_my_commands(default_commands, scope=BotCommandScopeDefault())

    # Admin commands
    for admin in admins:
        try:
            admin_commands = [
                BotCommand(
                    command="start",
                    description="Botni qayta ishga tushirish"
                ),
                BotCommand(
                    command="admin",
                    description="Admin panelga kirish"
                )
            ]
            bot.set_my_commands(
                admin_commands,
                scope=BotCommandScopeChat(chat_id=admin)
            )
        except Exception as e:
            print(f"Set command error for admin {admin}: {e}")
