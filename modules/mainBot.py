import json

from urllib.request import urlopen
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, RegexHandler, CallbackQueryHandler


class Order:
    idGoods = 0
    count = 0

    def __init__(self, idGoods, count):
        self.idGoods = idGoods
        self.count = count

    def __str__(self) -> str:
        return "product ->  id = {} and count = {}".format(self.idGoods, self.count)

    def increment(self):
        self.count += 1


TOKEN = "602606847:AAGNryoE6AyI9dX5uHNMRrKXAEbZVFGmFDw"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

orderArr = []


def createCategoriesButtons(categories):
    buttons = []
    for cat in categories:
        data = "cat-{}".format(cat["id"])
        buttons.append([InlineKeyboardButton(cat["name"], callback_data=data)])
    return buttons


def getCategories():
    data = json.loads(urlopen("http://95.46.45.206:8000/public/category").read())
    return data


def getSubCategories(id):
    data = json.loads(urlopen("http://95.46.45.206:8000/public/subCategory/{}".format(id)).read())
    return data


def getProducts(idSubCategory):
    data = json.loads(urlopen("http://95.46.45.206:8000/public/goods/by/subCategory/{}".format(idSubCategory)).read())
    return data


def showMenu(bot, update):
    categories = getCategories()
    buttons = createCategoriesButtons(categories)
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.send_message(chat_id=update['message']['chat']['id'], text='Виберіть:',
                     reply_markup=reply_markup)


def showMainControllers(bot, update):
    keyboard = [[KeyboardButton("Меню")],
                ["Пошук страв"]]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update['message']['chat']['id'], text='Виберіть:',
                     reply_markup=reply_markup)


def start(bot, update):
    bot.send_message(chat_id=update['message']['chat']['id'], text='ПРИВІТАННЯ')
    showMainControllers(bot, update)


def showSearch(bot, update):
    pass


def createSubCategoriesButtons(subCategories):
    buttons = []
    for subCat in subCategories:
        data = "sub-{}".format(subCat["id"])
        buttons.append([InlineKeyboardButton(subCat["name"], callback_data=data)])
    return buttons


def createProductButtons(products):
    buttons = []
    for prod in products:
        data = "prod-{}".format(prod["id"])
        buttons.append([InlineKeyboardButton(prod["name"], callback_data=data)])
    return buttons


def showSubCategories(bot, update, categoryId):
    subCategories = getSubCategories(categoryId)
    buttons = createSubCategoriesButtons(subCategories)
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.send_message(chat_id=update["callback_query"]["message"]["chat"]["id"], text='Виберіть підкатегорію:',
                     reply_markup=reply_markup)


def showProducts(bot, update, subCategoryId):
    products = getProducts(subCategoryId)
    buttons = createProductButtons(products)
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.send_message(chat_id=update["callback_query"]["message"]["chat"]["id"], text='Виберіть Товар:',
                     reply_markup=reply_markup)


def addToBucket(bot, update, idProduct):
    order = Order(idProduct, 0)
    for ord in orderArr:
        if ord.idGoods == idProduct:
            order = ord
            break
    orderArr.append(order)
    order.increment()
    result = "Замовлення -> "
    for ord in orderArr:
        result += ' '
        result += str(ord)
    bot.send_message(chat_id=update["callback_query"]["message"]["chat"]["id"], text=result)


def queryHandler(bot, update):
    query = update.callback_query
    data = query.data
    id = data.split('-')[1]
    # if data.startswith('cat-'):
    if (data.split('-')[0] == "cat"):
        showSubCategories(bot, update, id)
        return 1
    if (data.split('-')[0] == "sub"):
        showProducts(bot, update, id)
        return 1
    if (data.split("-")[0] == "prod"):
        addToBucket(bot, update, id)


# def trick(bot, update):
#     bot.send_message(chat_id=update['message']['chat']['id'],
#                      text="Введіть ім'я: ")


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(RegexHandler('Меню', showMenu))
    updater.dispatcher.add_handler(RegexHandler('Пошук', showSearch))
    updater.dispatcher.add_handler(CallbackQueryHandler(queryHandler))
    updater.dispatcher.add_handler(CommandHandler('help', help))

    # updater.dispatcher.add_handler(CommandHandler('trick', trick))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()



if __name__ == '__main__':
    main()
