import telebot
import wikipedia
import re
import random
import schedule
import time
from telebot import types

# bot token
bot = telebot.TeleBot("TOKEN")

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


# читаем сообщение юзера и даем инфу из вики
def get_wiki(message):
    answer = message.text
    bot.send_message(message.chat.id, getwiki(answer))


# -------------------------------------------------------------------------------
# schedule (который не работает)

menu_schedule = None
reminder_flag = False


def reminder_bot(message):
    remind_user = message.text
    bot.send_message(message.chat.id, remind_user)


if menu_schedule == "10:30":
    schedule.every().day.at("10:30").do(reminder_bot)

elif menu_schedule == "10:30 и 18:30":
    schedule.every().day.at("10:30").do(reminder_bot)

elif menu_schedule == "через 5 сек":
    schedule.every(5).seconds.do(reminder_bot)

while reminder_flag:
    schedule.run_pending()
    time.sleep(4)

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
# кнопки с меню

# функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_fs = types.KeyboardButton("ℹ факты/поговроки")
    item_wiki = types.KeyboardButton("🌐 wiki")
    item_reminder = types.KeyboardButton("⏱ напоминание")
    item_about_bot = types.KeyboardButton("💠 о боте")

    markup.add(item_fs, item_wiki, item_reminder, item_about_bot)

    bot.send_message(message.chat.id, f"Приветствую, {message.from_user.first_name}, "
                                      f"выбери, что ты хочешь сделать.", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def bot_message(message):
    # блок меню с выбором факта или поговорки
    if message.text == "ℹ факты/поговроки":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

        item_f = types.KeyboardButton("факт")
        item_s = types.KeyboardButton("поговорка")
        item_back = types.KeyboardButton("🔚 назад")
        markup.add(item_s, item_f, item_back)

        bot.send_message(message.chat.id, "Пожалуйста, выберите что вы хотите увидеть.", reply_markup=markup)

    # блок кода с фактом и логикой
    elif message.text == "факт":
        bot.send_message(message.chat.id, random.choice(facts))
    elif message.text == "поговорка":
        bot.send_message(message.chat.id, random.choice(thinks))

    # блок с wiki
    elif message.text == "🌐 wiki":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item_back = types.KeyboardButton("🔚 назад")
        markup.add(item_back)

        bot.send_message(message.chat.id, "Пожалуйста, напишите то, что вас интересует:", reply_markup=markup)

        bot.register_next_step_handler(message, get_wiki)

    elif message.text == "💠 о боте":
        markup = types.InlineKeyboardMarkup()

        markup.add(types.InlineKeyboardButton("Сайт бота",
                                              url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"))

        bot.send_message(message.chat.id, "Создатель бота: KH_Mad. Бот был написан для лабораторки по ООП. "
                                          "Ссылка на сайт бота (не судите строго):", parse_mode="html",
                         reply_markup=markup)

    elif message.text == "⏱ напоминание":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

        item_one_reminder = types.KeyboardButton("10:30")
        item_two_reminder = types.KeyboardButton("10:30 и 18:30")
        item_three_reminder = types.KeyboardButton("через 5 сек")
        item_off = types.KeyboardButton("выключить напоминание")
        item_back = types.KeyboardButton("🔚 назад")
        markup.add(item_one_reminder, item_two_reminder, item_three_reminder, item_off, item_back)

        bot.send_message(message.chat.id, "На данный момент бот умеет напоминать только в определенное"
                                          "время, установленное разработчиком", reply_markup=markup)

    elif message.text == "🔚 назад" or "меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

        item_fs = types.KeyboardButton("ℹ факты и поговроки")
        item_wiki = types.KeyboardButton("🌐 wiki")
        item_about_bot = types.KeyboardButton("💠 о боте")
        markup.add(item_fs, item_wiki, item_about_bot)

        bot.send_message(message.chat.id, "основное меню", reply_markup=markup)

    elif message.text == "10:30":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item_back_reminder = types.KeyboardButton("выключить напоминание")
        markup.add(item_back_reminder)

        menu_schedule = "10:30"
        reminder_flag = True

        bot.send_message(message.chat.id, "Напишите время, в которое вам нужно будет прислать напоминание",
                         reply_markup=markup)

        bot.register_next_step_handler(message, reminder_bot)

    elif message.text == "10:30 и 18:30":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item_back_reminder = types.KeyboardButton("выключить напоминание")
        markup.add(item_back_reminder)

        menu_schedule = "10:30 и 18:30"
        reminder_flag = True

        bot.send_message(message.chat.id, "Напишите время, в которое вам нужно будет прислать напоминание",
                         reply_markup=markup)

        bot.register_next_step_handler(message, reminder_bot)

    elif message.text == "через 5 сек":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item_back_reminder = types.KeyboardButton("выключить напоминание")
        markup.add(item_back_reminder)

        menu_schedule = "через 5 сек"
        reminder_flag = True

        bot.send_message(message.chat.id, "Напишите время, в которое вам нужно будет прислать напоминание",
                         reply_markup=markup)

        bot.register_next_step_handler(message, reminder_bot)

    elif message.text == "выключить напоминание" or "":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

        item_one_reminder = types.KeyboardButton("10:30")
        item_two_reminder = types.KeyboardButton("10:30 и 18:30")
        item_three_reminder = types.KeyboardButton("напоминание через 5 секунд")
        item_off = types.KeyboardButton("выключить напоминание")
        item_back = types.KeyboardButton("🔚 назад")
        markup.add(item_one_reminder, item_two_reminder, item_three_reminder, item_off, item_back)

        bot.send_message(message.chat.id, "Напоминание выключено", reply_markup=markup)


# запуск бота
bot.polling(none_stop=True, interval=0)
