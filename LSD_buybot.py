import telebot
from telebot import types
import time
blacklist=[]
bets=["Ставки пока нету, напишите позже"]
bot = telebot.TeleBot("776214624:AAGZjzZmVTf_alPhLGKlh8g4pfUei9PNmaY")
def main():
    try:
        @bot.message_handler(commands = ["addbets"])
        def add_bet(message):
            bets.clear()
            bets.append(message.text[9:])
        @bot.message_handler(commands = ["start"])
        def switch(message):
            if bets[0] == "Ставки пока нету, напишите позже":
                bot.send_message(message.chat.id, ("Ставки пока нету, напишите позже"))
            bot.send_message(message.chat.id, ("/buy_bet - купить ставку"))
            bot.send_message(chat_id="491711894", text="Кто-то написал мне))")
        @bot.message_handler(commands = ["buy_bet"])
        def switch(message):
                markup = types.InlineKeyboardMarkup()
                do = types.InlineKeyboardButton(text = "До", callback_data = "do")
                posle = types.InlineKeyboardButton(text = "После", callback_data = "posle")
                teh = types.InlineKeyboardButton(text="Техподдержка", callback_data="te" + str(message.chat.id),)
                markup.add(do, posle)
                markup.add(teh)
                bot.send_message(message.chat.id, text = "Стоимость 50 грн. Когда хотите оплатить ставку?", reply_markup = markup)
        @bot.callback_query_handler(func = lambda call: True)
        def callback_inline(call):
            if call.data == 'do':
                bot.send_message(chat_id = call.message.chat.id, text = "Стоимость 50 грн\n4149 4393 9647 5380\nУкажите этот комментарий к платежу: {id}\n/Done - если оплатили".format(id = call.message.chat.id))
            elif call.data == 'posle':
                bot.send_message(chat_id = "491711894", text = "Выполнена послеоплата")
                if call.message.chat.id in blacklist:
                    bot.send_message(call.message.chat.id, "Оплатите последнюю ставку\nСтоимость 50 грн.\n4149 4393 9647 5380\nУкажите этот комментарий к платежу: {id}\n/Oplatil - после оплаты".format(id = call.message.chat.id))
                else:
                    blacklist.append(call.message.chat.id)
                    bot.send_message(chat_id = call.message.chat.id,text = bets[0])
                    bot.send_message(chat_id = call.message.chat.id,text = "Вы попадаете в черный список бота без возможности восстановления пока не оплатите ставку.\nУкажите этот комментарий к платежу: {0}\n4149 4393 9647 5380\n/Oplatil - когда оплатите".format(call.message.chat.id))
            elif call.data[:2] == 'ok':
                client_id=call.data[2:]
                if call.message.chat.id in blacklist:
                    blacklist.remove(call.message.chat.id)
                bot.send_message(chat_id = client_id, text = bets[0])
                bot.send_message(chat_id = "491711894", text = "Ставка отправлена")
                bot.send_message(chat_id = client_id, text = "Спасибо за покупку. Ждите следующие ставки")
            elif call.data[:2] == 'er':
                client_id = call.data[2:]
                bot.send_message(chat_id = client_id, text = "Ставка не оплачена")
            elif call.data[:2] == 'te':
                client_id = call.data[2:]
                bot.send_message(chat_id = client_id, text = "Напишите Ваш вопрос, начав его с (/teh ) и в конце укажите именно эти цифры:{id}\nПример:\n/teh Здравствуйте, мне пришла ставка за прошлый день. 374284382".format(id = call.message.chat.id))
        @bot.message_handler(commands=["Done", "Oplatil"])
        def switch(message):
            markup = types.InlineKeyboardMarkup()
            do = types.InlineKeyboardButton(text = "Да", callback_data='ok'+str(message.chat.id))
            posle = types.InlineKeyboardButton(text = "Нет", callback_data="er"+str(message.chat.id))
            markup.add(do, posle)
            bot.send_message(chat_id = "491711894", text = "Оплата прошла?\n{0}".format(message.chat.id), reply_markup = markup)
        @bot.message_handler(commands=["teh"])
        def switch(message):
            bot.send_message(message.chat.id, text="Если вопрос не тупой, с вами свяжеться один из администраторов")
            bot.send_message(chat_id="491711894", text="{0}".format(message.text[5:]))
    except ConnectionError as ErrorConnect:
        print(ErrorConnect)
        time.sleep(20)
        main()
if __name__ == "__main__":
    main()
    bot.polling()