def test():
    import solution
    importlib.reload(sys.modules['solution'])
    file = open("tests.txt", "r")
    tests = file.readlines()
    tests_n = len(tests)
    correct = 0
    errors = 0
    for i in tests:
        test = list(map(float, i.split()))
        a, b, c = test[0], test[1], test[2]
        if len(test) > 3:
            answers = test[3:]
        else:
            answers = []
        try:
            if list(map(float, solution.solve(a, b, c))) == answers:
                correct += 1
            else:
                print("Incorrect:", a, b, c)
        except:
            errors += 1
    file.close()
    return (tests_n, correct, errors)

def get_last_update_id(updates):
    update_ids = []
    for update in updates:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


import telegram
import config
import time
from time import localtime
import sys, importlib

TOKEN = config.token
bot = telegram.bot.Bot(TOKEN)


markup = telegram.ReplyKeyboardMarkup(
    keyboard=[['Как пользоваться'],["Stop"]]
)
recognize = {
    'Как пользоваться': [bot.sendMessage, "Я умею проверять программы \U0001F604 \nСкиньте мне файл с программой, в которой есть функция solve(), принимющая три числа - коэффициенты квадратного уравнения, а возвращает массив действительных корней уравнения по возрастанию. \nЯ быстро протестирую программу у пришлю результаты."],
    'Stop': [exit, None]
}

def main():
    first_msg = False
    last_update_id = None
    while True:
        updates = bot.getUpdates(last_update_id, timeout=100)
        if len(updates) > 0:
            last_update_id = get_last_update_id(updates) + 1
            if first_msg:
                for update in updates: # сообщения могут приходить быстрее, чем работает код
                    #print(update)
                    last_message = update["message"] # взяли из него сообщение
                    #print(dir(last_message))
                    last_message_text = last_message['text'] # из сообщения - текст
                    last_chat_id =  last_message['chat']['id']
                    if  recognize.get(last_message_text):
                        function = recognize[last_message_text][0] # функция, которую мы вызываем - 
                                                               # нулевой элемент массива - значения по ключу
                        if last_message_text == 'Stop':
                            exit()
                        arg = recognize[last_message_text][1] # аргумент - его первый элемент
                        function(last_chat_id, arg)
                    elif last_message.document:
                        fid = last_message.document.file_id
                        inpfile = bot.getFile(fid)
                        inpfile.download('solution.py')
                        bot.sendMessage(last_chat_id, "Файл скачан") #\U0001F44D
                        bot.sendMessage(last_chat_id, "Проверяю решение \U0001F914")
                        results = test()
                        tests_n, correct, errors = results
                        incorrect = tests_n - correct - errors
                        if tests_n != 0:
                            procent = correct / tests_n * 100
                        else:
                            procent = 0
                        if procent == 100:
                            bot.sendMessage(last_chat_id, "Всё правильно!!! \U0001F44D \U0001F604")
                            bot.sendMessage(last_chat_id, "\U0001F197")
                        else:
                            if procent > 85:
                                bot.sendMessage(last_chat_id, "Почти всё правильно.")
                            elif procent > 40:
                                bot.sendMessage(last_chat_id, "Программу нужно дороботать.")
                            elif procent > 0:
                                bot.sendMessage(last_chat_id, "Есть правильные ответы, но их мало ")
                            else:
                                bot.sendMessage(last_chat_id, "Программа не выдала ни одного правильного ответа :(")
                            bot.sendMessage(last_chat_id, "Неправильных ответов: " + str(incorrect))
                            bot.sendMessage(last_chat_id, "Ошибок во время выполнения программы: " + str(errors))

                        bot.sendMessage(last_chat_id, "Правильных ответов: " + str(correct))
                        bot.sendMessage(last_chat_id, "Процент: " + str(int(procent)) + "%")


                    else:
                        bot.sendMessage(last_chat_id, # написавшему
                                        "Приветствую!", # отправляем сообщение
                                        reply_markup = markup) # включаем кнопки
        if not first_msg:
            first_msg = True
if __name__ == '__main__':
    main()