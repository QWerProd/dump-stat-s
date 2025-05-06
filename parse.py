import os
import json
from datetime import datetime


def parse_file(file: str) -> str:
    """Парсинг JSON файла с перепиской от ppldump_bot

    Args:
        file (str): Путь к файлу от telebot.get_file

    Returns:
        str: JSON с результатами
    """

    result = {
        "error": None,
        "result": None
    }

    statistics = {
        'total_count': 0,
        'hearts': 0,
        'skulls': 0,
        'your_messages': 0,
        'first_start': '',
        'first_message': '',
        'first_message_date': '',
        'first_heart': '',
        'first_heart_date': '',
        'first_skull': '',
        'first_skull_date': '',
        'last_message_date': '',
        'content_types': {
            'photo': 0,
            'video': 0,
            'audio': 0,
            'animation': 0,
            'text': 0
        }
    }

    past_message = {}

    with open(file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)


    try:
        if data['name'] != 'dump' and data['type'] != 'bot_chat':
            result['error'] = 'неизвестная переписка: это не переписка с ботом @ppldump_bot'
            return result
        
        for i in data['messages']:
            buttons = i.get('inline_bot_buttons')
            statistics['last_message_date'] = datetime.fromisoformat(i['date']).strftime("%d.%m.%Y %H:%M:%S")

            # Первый старт
            if statistics['first_start'] == '':
                statistics['first_start'] = datetime.fromisoformat(i['date']).strftime("%d.%m.%Y %H:%M:%S")

            if i['from'] == 'dump' and buttons is not None:

                # Общее количество прочитанных помоев (по кнопкам под сообщением)
                if len(buttons[0]) == 3 and len(buttons[1]) >= 1:
                    statistics['total_count'] += 1
                    

                    ## Кол-во лайков и дизов
                    if '💚' in buttons[0][0]['text']:
                        statistics['hearts'] += 1

                        # Первое поставленное сердце
                        if statistics['first_heart'] == '':
                            statistics['first_heart'] = i['text']
                            statistics['first_heart_date'] = datetime.fromisoformat(i['date']).strftime("%d.%m.%Y %H:%M:%S")

                    elif '☠' in buttons[0][1]['text']:
                        statistics['skulls'] += 1

                        # Первый поставленный черепок
                        if statistics['first_skull'] == '':
                            statistics['first_skull'] = i['text']
                            statistics['first_skull_date'] = datetime.fromisoformat(i['date']).strftime("%d.%m.%Y %H:%M:%S")

                    # Определение типа контента
                    if 'photo' in i:
                        statistics['content_types']['photo'] += 1
                    elif i.get('media_type') == 'video_file':
                        statistics['content_types']['video'] += 1
                    elif i.get('media_type') == 'audio_file':
                        statistics['content_types']['audio'] += 1
                    elif i.get('media_type') == 'animation':
                        statistics['content_types']['animation'] += 1
                    else:
                        statistics['content_types']['text'] += 1

            ## Отправленные
            elif i['from'] == 'dump' and i['text'] == 'кинул в свалку 🛢️':
                statistics['your_messages'] += 1

                # Первое сообщение
                if statistics['first_message'] == '':
                    statistics['first_message'] = past_message['text']
                    statistics['first_message_date'] = datetime.fromisoformat(past_message['date']).strftime("%d.%m.%Y %H:%M:%S")


            past_message = { 'text': i['text'], 'date': i['date']}

    
    except KeyError:
        pass
    except:
        result['error'] = 'структура файла некорректная'
        return result
    
    result['result'] = statistics
    return result