import telebot
from telebot import types
import webbrowser
import random
from const import TOKEN, PATH

elements = ['h2', 'he', 'li', 'be', 'b', 'c', 'n', 'o2', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba', 'la', 'ce', 'pr', 'nd', 'pm', 'sm', 'eu', 'gd', 'tb', 'dy', 'ho', 'er', 'tm', 'yb', 'lu', 'hf', 'ta', 'w', 're', 'os', 'ir', 'pt', 'au', 'hg', 'tl', 'pb', 'bi', 'po', 'at', 'rn', 'fr', 'ra', 'ac', 'th', 'pa', 'u', 'np', 'pu', 'am', 'cm', 'bk', 'cf', 'es', 'fm', 'md', 'no', 'lr', 'rf', 'db', 'sg', 'bh', 'hs', 'mt', 'ds', 'rg', 'cn', 'nh', 'fl', 'mc', 'lv', 'ts', 'og']


bot = telebot.TeleBot(TOKEN)
bd_path = PATH
bd_RandEl = 'RandEl'
bd_ZadCep = 'ZadCep'
zad_count = 6


@bot.message_handler(commands=['start'])
def start(message):
    print(message.from_user.first_name)
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Случайный элемент')
    btn2 = types.KeyboardButton('Задача на цепочки')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Привет! Напиши обозначение любого химического элемента:', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def vivod(message):
    if message.text.lower() in elements:
        picture = open(fr'{bd_path}\{bd_RandEl}\{message.text.lower()}.jpg', 'rb') #with, try, except
        capt = open(fr'{bd_path}\{bd_RandEl}\{message.text.lower()}.txt', 'r', encoding='utf-8')

        bot.send_message(message.chat.id, 'Это может занять несколько секунд :)')
        bot.send_photo(message.chat.id, picture)
        bot.send_message(message.chat.id, capt.read(), parse_mode = 'html') #message text is empty

        capt.close()
        picture.close()

    elif message.text.lower() == 'случайный элемент':
        el = random.choice(elements)
        #print(el)
        picture = open(fr'{bd_path}\{bd_RandEl}\{el}.jpg', 'rb')
        capt = open(fr'{bd_path}\{bd_RandEl}\{el}.txt', 'r', encoding='utf-8')

        bot.send_message(message.chat.id, 'Это может занять несколько секунд :)')
        bot.send_photo(message.chat.id, picture)
        bot.send_message(message.chat.id, capt.read(), parse_mode = 'html') #message text is empty

        capt.close()
        picture.close()

    elif message.text.lower() == 'задача на цепочки':
        n_zad = random.randint(1, zad_count)

        if len(str(n_zad)) == 1:
            n_zad = '0' + str(n_zad) #мб начну индексацию zad/otv с 11

        print(n_zad, type(n_zad))

        zad_f = open(fr'{bd_path}\{bd_ZadCep}\zad{n_zad}.txt', 'r', encoding='utf-8')
        zad = zad_f.read()
        zad_f.close()


        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Показать ответ', callback_data=f'otvet{n_zad}')
        btn2 = types.InlineKeyboardButton('Далее', callback_data='dalee')
        markup.row(btn1, btn2)

        bot.send_message(message.chat.id, 'Решите цепочку: \n' + zad, reply_markup=markup)


    else:
        bot.send_message(message.chat.id, 'Ошибка ввода')

@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data[:-2] == 'otvet':

        n_zad = callback.data[-2:]
        otv_f = open(fr'{bd_path}\{bd_ZadCep}\otv{n_zad}.txt', 'r', encoding='utf-8')
        otv = otv_f.read()
        otv_f.close()

        #bot.send_message(callback.message.chat.id, 'Ответ:\n' + otv)
        bot.edit_message_text('Ответ:\n' + otv, callback.message.chat.id, callback.message.message_id)

    elif callback.data == 'dalee':
        n_zad = random.randint(1, zad_count)

        if len(str(n_zad)) == 1:
            n_zad = '0' + str(n_zad) #мб начну индексацию zad/otv с 11

        print('Е', n_zad, type(n_zad))

        zad_f = open(fr'{bd_path}\{bd_ZadCep}\zad{n_zad}.txt', 'r', encoding='utf-8')

        zad = zad_f.read()
        zad_f.close()

        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Показать ответ', callback_data=f'otvet{n_zad}')
        btn2 = types.InlineKeyboardButton('Далее', callback_data='dalee')
        markup.row(btn1, btn2)

        bot.send_message(callback.message.chat.id, 'Решите цепочку: \n' + zad, reply_markup=markup)


bot.polling(non_stop = True)
