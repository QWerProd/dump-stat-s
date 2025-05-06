import os
import json


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
        'total_count': 0
    }

    with open(file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)


    try:
        if data['name'] != 'dump' and data['type'] != 'bot_chat':
            result['error'] = 'неизвестная переписка: это не переписка с ботом @ppldump_bot'
            return result
        
        for i in data['messages']:
            buttons = i.get('inline_bot_buttons')
            if i['from'] == 'dump' and buttons is not None:
                if len(buttons[0]) == 3 and len(buttons[1]) == 2:
                    statistics['total_count'] += 1
    
    except KeyError:
        pass
    except:
        result['error'] = 'структура файла некорректная'
        return result
    
    result['result'] = statistics
    return result




print(parse_file('C:\\Users\\ds\\Downloads\\Telegram Desktop\\ChatExport_2025-05-05\\result.json'))