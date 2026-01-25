ChefStreet
Telegram bot for the ChefStreet project (synchronous telebot implementation).

Quick start

- Install dependencies: `pip install -r requirements.txt`
- Configure the bot: edit `tgbot/files/config.py`
- Run: `python main.py`

Service (Linux)

- systemd unit available at `systemd/tgbot.service` (optional)

Project layout

- `main.py` — application entry point
- `tgbot/` — bot package containing handlers, filters, middleware, helpers, models, states, and texts
- `requirements.txt` — Python dependencies

Requirements

- Python 3.10+
- `pyTelegramBotAPI` >= 4.30.0

Contributing

Feel free to open issues or submit pull requests to improve the project.
