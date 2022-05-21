from telegram.ext import Updater, ExtBot, Filters, \
    MessageHandler, CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from db_bot import *
bot = ExtBot(token='5177422586:AAEaoT-X0pWeMLmEPSQ0m8wJSsglmnx9Z7M')
import time

updater = Updater(bot.token, use_context=True)
dispatcher = updater.dispatcher

but_menu = ['Личный кабинет', 'Разместить объявление', 'Поиск']
bot_menu = ReplyKeyboardMarkup([but_menu], resize_keyboard=True)


def start(update, context):
    bot.send_message(chat_id=update.message.from_user.id, text='Добро пожаловать!\n'
                                                               '    Данный бот поможет тебе в поиске\n'
                                                               '        И размещении объявлений в штатах Гоа')
    id = update.message.from_user.id
    try:
        check_registration = Person.select().where(Person.user_id==id).get()
    except DoesNotExist as e:
        city = City()
        list_city = city.get_list()
        button = []
        for but in list_city:
            button.append(InlineKeyboardButton(text=but.name, callback_data=but.id))
        menu_city = InlineKeyboardMarkup(inline_keyboard=[button])
        bot.send_message(chat_id=id, text='Выберите штат в котором находитесь', reply_markup=menu_city.from_column(button))

def city_select(update, context):
    id = update.callback_query.from_user.id
    if update.callback_query.message.text == "Выберите штат в котором находитесь":
        Person.create(user_id=id, city_id=update.callback_query.data)
    bot.send_message(chat_id=id, text='Теперь можешь искать или размещать объявления', reply_markup=bot_menu)


# Handlers
start_handler = CommandHandler('start', start)
city_handler = CallbackQueryHandler(city_select)

# Dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(city_handler)

updater.start_polling()
