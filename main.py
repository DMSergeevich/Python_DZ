import logging
import random
import model
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters


reply_keyboard = [['/play', '/info', '/close']]

stop_keyboard = [['/stop']]


markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
stop_markup = ReplyKeyboardMarkup(stop_keyboard, one_time_keyboard=False)



TOKEN = '5905885390:AAEZvKJWXWCEqrzOrw6wbOwgFd_hV_ZBTso'

candy = 0




def start(update, context):
    update.message.reply_text(
        "Привет! Давай играть!",
        reply_markup=markup
    )



def play(update, context):
    update.message.reply_text(
        'Введите колличество конфет в игре', reply_markup=stop_markup)
    return 1



def play_get_candy(update, context):
    global candy
    candy = int(update.message.text)  
    update.message.reply_text(
        'Сколько кофент вы возьмете?', reply_markup=stop_markup)
    return 2


def player_1(update, context):
    global candy
    try:
        temp_pleer = int(update.message.text)  
        if temp_pleer > 28:
            update.message.reply_text(
                'Вы ввели неверное число. Введите число меньше или равное 28')
            return 2
        candy -= temp_pleer
        update.message.reply_text(
            f'Конфет осталось: {candy}', reply_markup=stop_markup)
        if candy > 28:
            temp_bot = model.second_bot(candy)
            candy -= temp_bot
            update.message.reply_text(
                f'Бот взял {temp_bot} конфет. Конфет осталось: {candy}', reply_markup=stop_markup)
            if candy > 28:
                update.message.reply_text(
                    'Сколько кофент вы возьмете?', reply_markup=stop_markup)
            else:
                update.message.reply_text(
                    f'Вы победили', reply_markup=markup)
                context.bot.send_photo(update.effective_chat.id, photo=open(
                    'Python_DZ\foto1.jpg/foto1.jpg', 'rb'))
                return ConversationHandler.END
            return 2
        else:
            update.message.reply_text('Победил бот', reply_markup=markup)
            context.bot.send_photo(update.effective_chat.id, photo=open(
                'Python_DZ\foto1.jpg/foto2.jpg', 'rb'))
            return ConversationHandler.END
    except ValueError:
        update.message.reply_text('Введите число')
        return 2



def stop(update, context):
    update.message.reply_text("Всего доброго!", reply_markup=markup)
    return ConversationHandler.END



def info(update, context):
    update.message.reply_text(
        f"Правила игры \n"
        f"1. Задайте начальное количество конфет \n"
        f"2. Сделайте свой ход, взяв от 1 до 28 конфет \n"
        f"3. Выигрывает тот игрок, кто взял в последнем ходе все конфеты"
    )



def close(update, context):
    update.message.reply_text(
        "Благодарю за игру!",
        reply_markup=ReplyKeyboardRemove())


play_handler = ConversationHandler(
    entry_points=[CommandHandler('play', play)],

    
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, play_get_candy)],
        2: [MessageHandler(Filters.text & ~Filters.command, player_1)],
    },

    
    fallbacks=[CommandHandler('stop', stop)]
)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(play_handler)
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("close", close))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()