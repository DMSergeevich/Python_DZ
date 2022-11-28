import sqlite3  # иморт sqlite3

from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from random import randint



bot_token = '5905885390:AAEZvKJWXWCEqrzOrw6wbOwgFd_hV_ZBTso'
bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        f"Привет! Это телефонный справочник!\n"
        f"Выберите необходимое действие:\n"
        f"показать все /show \n"
        f"показать конкретного человека /show_person\n"
        f"удалить запись /del_note\n"
        f"добавить запись /add_note\n"
    )


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END




def show(update, context):
    conn = sqlite3.connect(
        'Homework9/fonebook.db')  
    cursor = conn.cursor()
    cursor.execute("select * from fonebook")  
    results = cursor.fetchall()
    context.bot.send_message(update.effective_chat.id,
                             f"{results}")  



def show_person(update, context):
    context.bot.send_message(update.effective_chat.id,
                             f"Введите фамилию: \n Для выхода напишите /stop")
    return 1


def show_person_out(update, context):
    conn = sqlite3.connect('Homework9/fonebook.db')
    cursor = conn.cursor()
    text = update.message.text  
    cursor.execute(
        f"select * from fonebook where firs_name like '%{text}%'")
    results = cursor.fetchall()
    update.message.reply_text(f"{results}")


show_person_handler = ConversationHandler(
    
    entry_points=[CommandHandler('show_person', show_person)],

    
    states={
       
        1: [MessageHandler(Filters.text & ~Filters.command, show_person_out)],
    },

   
    fallbacks=[CommandHandler('stop', stop)]
)

def del_note(update, context):
    context.bot.send_message(
        update.effective_chat.id, f"Введите индекс для удаления: \n Для выхода напишите /stop")
    return 1




def del_note_out(update, context):
    conn = sqlite3.connect('Homework9/fonebook.db')
    cursor = conn.cursor()
    text = update.message.text   
    cursor.execute(
        f"delete from fonebook where id={text}")
    conn.commit()
    update.message.reply_text(f"информация удалена")



del_note_handler = ConversationHandler(
    
    entry_points=[CommandHandler('del_note', del_note)],

    
    states={
       
        1: [MessageHandler(Filters.text & ~Filters.command, del_note_out)],
    },

    
    fallbacks=[CommandHandler('stop', stop)]
)






def add_note(update, context):
    context.bot.send_message(
        update.effective_chat.id, f"Введите данные для добавления: \n Для выхода напишите /stop")
    return 1




def add_note_out(update, context):
    conn = sqlite3.connect('Homework9/fonebook.db')
    cursor = conn.cursor()
    text = update.message.text  
    text = text.split()  
    cursor.execute(
        f"insert into fonebook (firs_name, second_name, father_name, fone, description)"
        f"values ('{text[0]}', '{text[1]}', '{text[2]}', '{text[3]}', '{text[4]})')")
    conn.commit()
    update.message.reply_text(f"информация добавлена")



add_note_handler = ConversationHandler(
   
    entry_points=[CommandHandler('add_note', add_note)],

    
    states={
        
        1: [MessageHandler(Filters.text & ~Filters.command, add_note_out)],
    },

    fallbacks=[CommandHandler('stop', stop)]
)




start_handler = CommandHandler('start', start)  # стартовое меню
show_handler = CommandHandler('show', show)    # показ всей книги


dispatcher.add_handler(start_handler)  # стартовое меню
dispatcher.add_handler(show_handler)    # показ всей базы
dispatcher.add_handler(show_person_handler)    # показ конкретного человека
dispatcher.add_handler(del_note_handler)    # удаление записи
dispatcher.add_handler(add_note_handler)    # добавление записи


updater.start_polling()
updater.idle()
