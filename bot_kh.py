import telebot
import wikipedia
import re
import random
from telebot import types

# bot token
bot = telebot.TeleBot("5367333927:AAGelE8i-Y9TsOGoqwjdFGBlo1xZIIpKEGI")

# ----------------------------------------------------------------------------
# wiki
wikipedia.set_lang("ru")


# чистка текста статьи в Wikipedia и ограничивание его 1000 символов
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        # проходимся по строкам, где нет знаков "равно"
        for x in wikimas:
            if not ('==' in x):
                if len((x.strip())) > 3:
                    wikitext2 = wikitext2 + x + '.'
            else:
                break

        # очистка разметок
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)

        # возвращается текстовая строка
        return wikitext2

    # обрабатывание исключения, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


# ------------------------------------------------------------------------------
# facts and (logic) thinks

# список НУ ОЧЕНЬ ИНТЕРЕСНЫХ фактов
f = open('data/facts.txt', 'r', encoding='UTF-8')
facts = f.read().split('\n')
f.close()

# список поговорок (на все случаи жизни)
f = open('data/thinks.txt', 'r', encoding='UTF-8')
thinks = f.read().split('\n')
f.close()


# ------------------------------------------------------------------------------

# функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    # 3 кнопки (факт, поговорка и вики)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("факт")
    item2 = types.KeyboardButton("поговорка")
    item3 = types.KeyboardButton("wiki")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(m.chat.id, 'Приветствую, выбери любую команду.', reply_markup=markup)


# получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # факт
    if message.text.strip() == 'факт':
        answer = random.choice(facts)
    # поговорка
    elif message.text.strip() == 'поговорка':
        answer = random.choice(thinks)
    # wiki
    elif message.text.strip() == 'wiki' :
        bot.send_message(m.chat.id, 'Пришли любой термин, который тебя интересует.')
        # answer = getwiki(message.text)
    # отсылаем сообщение юзеру в чат
    bot.send_message(message.chat.id, answer)



# запуск бота
bot.polling(none_stop=True, interval=0)
