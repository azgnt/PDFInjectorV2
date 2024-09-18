from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace 'YOUR_TOKEN' with your bot's token
updater = Updater(token='YOUR_TOKEN', use_context=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! I am your bot. How can I assist you today?')

def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('echo', echo))

updater.start_polling()
updater.idle()
