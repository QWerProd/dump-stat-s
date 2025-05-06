import telebot
import texts

from keys import TG_BOT_API_KEY
from parse import parse_file


bot = telebot.TeleBot(TG_BOT_API_KEY)

# Приветствие
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, texts.start_text)

# Подсказка как начать статистику
@bot.message_handler(commands=['importFile'])
def start_import(message):
    bot.send_message(message.from_user.id, texts.import_file_text)
    bot.register_next_step_handler(message, get_json_file)

@bot.message_handler(content_types=['document'])
def get_json_file(message):
    file_name = message.document.file_name.split('.')
    if file_name[1] != 'json':
        return bot.send_message(message.from_user.id, "нужно загрузить файл JSON формата") 
    
    # Сохранение файла
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(message.document.file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.from_user.id, "ожидайте завершения загрузки и обработки файла")

    results = parse_file(message.document.file_name)


bot.polling(none_stop=True, interval=0)