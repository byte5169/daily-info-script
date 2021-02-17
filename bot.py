import os
import time
import logging
import telebot

from dotenv import load_dotenv
from modules.exchange_rates import get_exchange_rates
from modules.recipe import get_recipe
from modules.weather import get_weather

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
load_dotenv()
bot_token = os.getenv("bot_token")
bot = telebot.TeleBot(bot_token, parse_mode=None)

knownUsers = []

commands = {
    "help": "Gives you information about the available commands",
    "exchange": "Gives you current exchange rates",
    "recipe": "Provides you the random breakfast recipe",
    "weather": "Provides you the forecast for weather in Minsk",
}


@bot.message_handler(commands=["start"])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:
        knownUsers.append(cid)
        bot.send_message(
            cid,
            "Hello, stranger, now we know each other! \nType /help for all available commands.",
        )
    else:
        bot.send_message(cid, "You can type /help to get started.")


@bot.message_handler(commands=["help"])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)


@bot.message_handler(commands=["exchange"])
def command_exchange(m):
    cid = m.chat.id
    bot.send_message(cid, "Let me check the banks...")
    bot.send_chat_action(cid, "typing")
    time.sleep(3)
    bot.send_message(cid, get_exchange_rates())


@bot.message_handler(commands=["recipe"])
def command_recipe(m):
    cid = m.chat.id
    bot.send_message(cid, "Let me check my cooking book...")
    bot.send_chat_action(cid, "typing")
    bot.send_message(cid, f"For breakfast you can try this:\n{get_recipe()}")


@bot.message_handler(commands=["weather"])
def command_weather(m):
    cid = m.chat.id
    bot.send_message(cid, "Let me check with the best weather forecasters...")
    bot.send_chat_action(cid, "typing")
    bot.send_message(cid, get_weather(53.9006, 27.5590))


@bot.message_handler(func=lambda message: True, content_types=["text"])
def command_default(m):
    bot.send_message(
        m.chat.id,
        "I don't understand \"" + m.text + '"\nMaybe try the help page at /help',
    )


bot.polling()
