import config
import telegram
import json
from random import randint

TOKEN = config.token
bot = telegram.bot.Bot(TOKEN)


def get_last_update_id(updates):
    """Возвращает ID последнего апдейта"""
    id_list = list()  # пустой список ID апдейтов
    for update in updates:  # для каждого апдейта
        id_list.append(update["update_id"])  # заносим в список его ID
    return max(id_list)  # возвращаем последний

markup = telegram.ReplyKeyboardMarkup(
    keyboard=['Как пользоваться']
)
recognize = {
    'Как пользоваться': [bot.sendMessage, "Hello \n I can test your skill of recognizing nmr spectra \U0001F604"
                                          " \n Firstly, a spectrum of proton magnetic resonance and four variants of molecules will be sent to you. You are to choose a suitable picture and type its number.\n If your answer is wrong, I'll send the correct answer with explanation."],
 #   'Stop': [exit, None]
}

def send_test(bot, tests_dict, chat_id):
    tests = tests_dict['tests']
    test_id = randint(0, len(tests) - 1)
    test = tests[test_id]
    bot.sendPhoto(chat_id, test['img'])
    correct_ans = test['correct_ans']
    incorrect_ans = test['incorrect_ans']
    all_ans = incorrect_ans + [correct_ans]
    correct_ans_num = -1
    for i in range(len(all_ans)):
        ans_id = randint(0, len(all_ans) - 1)
        bot.sendMessage(chat_id, str(i + 1) + '. ')
        bot.sendPhoto(chat_id, all_ans[ans_id])
        if all_ans[ans_id] == correct_ans:
            correct_ans_num = i + 1
        all_ans.pop(ans_id)

    return test_id, correct_ans_num


def check_ans(bot, tests_dict, chat_id, test_id, correct_ans_num, player_ans_num):
    tests = tests_dict['tests']
    test = tests[test_id]
    if str(player_ans_num) == str(correct_ans_num):
        bot.sendMessage(chat_id, "Correct!!! \U0001F601")
    else:
        bot.sendMessage(chat_id, "Unfortunately the answer is wrong \U0001F601")
        #        bot.sendMessage(chat_id, "The correct answer is " + str(correct_ans_num))
        #        bot.sendMessage(chat_id, "Here is some theory to help you")
        bot.sendPhoto(chat_id, test['help_img'])


def main():
    last_update_id = None
    file = open("test.json", "r")
    tests_dict = json.load(file)
    file.close()
    testing = False
    while True:
        updates = bot.getUpdates(last_update_id, timeout=100)
        if len(updates) > 0:
            last_update_id = get_last_update_id(updates) + 1
            for update in updates:  # сообщения могут приходить быстро, быстрее, чем работает код
                last_message = update["message"]  # взяли из него сообщение
                if last_message :
                    print(last_message)
                    last_message_text = last_message['text']  # из сообщения - текст
                    last_chat_id = last_message['chat']['id']  # и идентификатор чата
                    if recognize.get(last_message_text):
                        function = recognize[last_message_text][0]  # функция, которую мы вызываем -
                        # нулевой элемент массива - значения по ключу
#                        if last_message_text == 'Stop':
#                            exit()
                        arg = recognize[last_message_text][1]  # аргумент - его первый элемент
                        function(last_chat_id, arg)
                    if (not testing) and last_message_text == "Test me":
                        testing = True
                        test_id, correct_ans_num = send_test(bot, tests_dict, last_chat_id)
                    elif testing:
                        check_ans(bot, tests_dict, last_chat_id, test_id, correct_ans_num, last_message_text)
                        testing = False


main()
