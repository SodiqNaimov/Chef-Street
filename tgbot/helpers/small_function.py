from typing import Optional

import aiohttp
import requests

from tgbot.helpers.database import SQLite
from tgbot.texts.text_reply import *
from telebot import TeleBot
from geopy.distance import geodesic
# import pytz
# from datetime import datetime

# For getting lang
set_user_lang = lambda text: 'ru' if text == lang_msg[1] else 'uz' if text == lang_msg[0] else None
locations = [
    ("📍 Chef Street Koloxoz", "📍 Chef Street Колхоз",39.781011, 64.403939)

]
# Alternative way to get one requirement data
def return_data(message, bot, word):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        word = data.get(word)

        return word

def mention_or_silka(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = f'<a href="tg://user?id={user_id}">{user_name}</a>'
    username = message.from_user.username
    # Determine silka
    if username is None:
        silka = mention  # Fallback to mention if username is not available
    else:
        print('yes')
        silka = f"@{username}"  # Format as @username

    return silka

# def get_current_time_in_uzbekistan():
#     # Get the timezone for Uzbekistan
#     uzbekistan_timezone = pytz.timezone('Asia/Tashkent')
#
#     # Get the current time in UTC
#     current_time_utc = datetime.utcnow()
#
#     # Localize the UTC time to Uzbekistan timezone
#     current_time_uzbekistan = pytz.utc.localize(current_time_utc).astimezone(uzbekistan_timezone)
#
#     # Format the time as per the required format
#     formatted_time = current_time_uzbekistan.strftime("%d.%m.%Y %H:%M:%S")
#
#     return formatted_time
ORS_API_KEY = "5b3ce3597851110001cf624800977a89a67242ccac9de7d85e14339c"
def get_ors_distance(origin, destination):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "coordinates": [[origin[1], origin[0]], [destination[1], destination[0]]]
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        data = response.json()
        meters = data['routes'][0]['segments'][0]['distance']
        return meters / 1000  # convert to km
    except Exception as e:
        print("⚠️ ORS failed, falling back to geopy:", e)
        return None  # signal fallback
def find_closest_location(user_location, lang):
    user_lat, user_lon = user_location
    min_distance = float('inf')
    closest_location = None

    db = SQLite()
    locations = db.get_all_locations(active_only=True)

    for location in locations:
        name_uzb, name_rus, loc_lat, loc_lon = location

        # Try ORS first
        distance = get_ors_distance((user_lat, user_lon), (loc_lat, loc_lon))

        # Fallback to geopy if ORS failed
        if distance is None or distance == float('inf'):
            distance = geodesic((user_lat, user_lon), (loc_lat, loc_lon)).kilometers
            print(f"📍 Used geopy for {name_uzb}: {distance:.2f} km")

        else:
            print(f"🚗 ORS distance to {name_uzb}: {distance:.2f} km")

        # Keep the closest
        if distance < min_distance:
            min_distance = distance
            closest_location = location

    if closest_location:
        name_uzb, name_rus, loc_lat, loc_lon = closest_location
        formatted_distance = "{:.1f}".format(min_distance)
        location_name = name_uzb if lang == 'uz' else name_rus
        return location_name, formatted_distance

    return None, None