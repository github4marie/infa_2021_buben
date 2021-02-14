import telegram
import config
TOKEN = config.token
bot = telegram.Bot(TOKEN)

print(*bot.getUpdates(), sep = '\n_______\n')

update1 = bot.getUpdates()[1] # взяли первый апдейт
message1 = update1['message'] # из него взяли сообщение
print(message1['text']) # из которого взяли текст
chat_id = message1['chat']['id'] # отправим ответ тому, кто первый написал боту
bot.sendMessage(chat_id, "Привет!") # первый аргумент - адресат, второй - текст

def get_last_update_id(updates):
    """Возвращает ID последнего апдейта"""
    id_list = list() # пустой список ID апдейтов
    for update in updates: # для каждого апдейта 
        id_list.append(update["update_id"]) # заносим в список его ID
    return(max(id_list)) # возвращаем последний


last_update_id = None
while True:
    updates = bot.getUpdates(last_update_id, timeout=100)
    if len(updates) > 0:
        last_update_id = get_last_update_id(updates) + 1
        for update in updates: # сообщения могут приходить быстро, быстрее, чем работает код
            last_message = update["message"] # взяли из него сообщение
            last_message_text = last_message['text'] # из сообщения - текст
            last_chat_id =  last_message['chat']['id'] # и идентификатор чата
            bot.sendMessage(last_chat_id, last_message_text[::-1]) # отправили обратно последнее
                                                                   # сообщение задом наперёд   

