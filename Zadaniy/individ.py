#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import jsonschema


def get_human(people):
    """
    Запросить данные о человеке.
    """
    # Запросить данные о человеке.
    name = input("Фамилия и инициалы? ")
    zodiac = input("Знак Зодиака? ")
    year = list(map(int, input("Дата рождения? ").split()))
    # Создать словарь.
    human = {
        'name': name,
        'zodiac': zodiac,
        'year': year,
    }
    # Добавить словарь в список.
    people.append(human)
    # Отсортировать список в случае необходимости.
    if len(people) > 1:
        people.sort(key=lambda x: x.get('year')[::-1])


def display_people(people):
    """
    Отобразить список людей.
    """
    # Заголовок таблицы.
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 15
    )
    print(line)
    print(
        '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
            "№",
            "Ф.И.О.",
            "Знак Зодиака",
            "Дата рождения"
        )
    )
    print(line)
    # Вывести данные о всех людях.
    for idx, human in enumerate(people, 1):
        print(
            '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                idx,
                human['name'],
                human['zodiac'],
                ' '.join((str(i) for i in human['year']))
            )
        )
    print(line)


def whois(people):
    """
    Выбрать человека по фамилии.
    """
    who = input('Кого ищем?: ')
    count = 0
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 15
    )
    print(line)
    print(
        '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
            "№",
            "Ф.И.О.",
            "Знак Зодиака",
            "Дата рождения"
        )
    )
    print(line)
    for i, num in enumerate(people, 1):
        if who == num['name']:
            count += 1
            print(
                '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                    count,
                    num['name'],
                    num['zodiac'],
                    ' '.join((str(i) for i in num['year']))))
    print(line)
    if count == 0:
        print('Никто не найден')


def save_people(file_name, people):
    """
    Сохранить всех работников в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(people, fout, ensure_ascii=False, indent=4)


def load_people(file_name, schema):
    """
    Загрузить всех людей из файла JSON
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        data = json.load(fin)
    validator = jsonschema.Draft7Validator(schema)
    try:
        if not validator.validate(data):
            print("Ошибок не обнаружено")
    except jsonschema.exceptions.ValidationError:
        print("Ошибка валидации", file=sys.stderr)
        exit(1)

    return data


def main():
    """
    Главная функция программы.
    """
    schema = {
        "type": "array",
        "items": [
            {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "zodiac": {
                        "type": "string"
                    },
                    "year": {
                        "type": "array"
                    }
                },
                "required": [
                    "name",
                    "zodiac",
                    "year"
                ]
            }
        ]
    }
    people = []
    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            get_human(people)

        elif command == 'list':
            display_people(people)

        elif command == 'whois':
            whois(people)

        elif command.startswith("save"):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            save_people(file_name, people)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Загрузить данные файла с заданным именем.
            people = load_people(file_name, schema)

        else:
            print('Неизвестная команда', command, file=sys.stderr)


if __name__ == '__main__':
    main()
