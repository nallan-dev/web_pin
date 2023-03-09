from .settings import LANGUAGE_CODE


TRANSLATIONS = {
    "There are no switches here yet - set them up": {
        "ru-ru": "Здесь пока нет переключателей - настройте их"
    },
    "Updated": {
        "ru-ru": "Обновлено",
    },
    "Planned tasks": {
        "ru-ru": "Плановые задачи",
    },
    "Switchers": {
        "ru-ru": "Переключатели",
    },
    "Switchers - administration": {
        "ru-ru": "Переключатели - администрирование"
    },
    "Apps": {
        "ru-ru": "Приложения",
    },
    "Invalid Cron": {
        "ru-ru": "Невалидный Крон",
    },
    "Invalid notation. The string must contain only characters "
    "-/,*0123456789, and four single spaces. Conveniently set up and copy "
    "the string you can here - https://crontab.guru/": {
        "ru-ru": "Невалидная нотация. Строка должна содержать только знаки"
        " -/,*0123456789, и четыре одинарных пробела. Удобно "
        "настроить и скопировать строку можно здесь - "
        "https://crontab.guru/",
    },
    "Refresh state": {
        "ru-ru": "Обновить",
    },
    "Index number": {
        "ru-ru": "Порядковый номер",
    },
    "For ordering in list": {
        "ru-ru": "Для отображения в списке",
    },
    "Pin num (BOARD)": {
        "ru-ru": "Номер пина (BOARD)",
    },
    "GPIO BOARD numbering": {
        "ru-ru": "Нумерация GPIO BOARD",
    },
    "Switch name": {
        "ru-ru": "Назначение переключателя",
    },
    'For example, "Light in the kitchen"': {
        "ru-ru": 'Например "Свет на кухне"',
    },
    "Comment": {
        "ru-ru": "Комментарий",
    },
    "Optional field": {
        "ru-ru": "Необязательное поле",
    },
    "Current state": {
        "ru-ru": "Текущее состояние",
    },
    "On or off": {
        "ru-ru": "Включен или выключен",
    },
    "Active": {
        "ru-ru": "Активен",
    },
    "Display in interfaces?": {
        "ru-ru": "Отображать ли в интерфейсах?",
    },
    "Invert state": {
        "ru-ru": "Инвертировать состояние",
    },
    'Invert state at GPIO-level (e.g. "Enabled pin" = GPIO.LOW (gnd))': {
        "ru-ru": "Инвертировать состояние пинов на уровне GPIO "
        '(т.е. "Включенный пин" = GPIO.LOW (gnd))',
    },
    "Pin config": {
        "ru-ru": "Настройка пина",
    },
    "Pin configs": {
        "ru-ru": "Настройки пинов",
    },
    "Telegram bot token": {
        "ru-ru": "Токен телеграм-бота",
    },
    "Allowed id (separated by commas)": {
        "ru-ru": "Разрешенные id (через запятую)",
    },
    "Name": {
        "ru-ru": "Идентификатор",
    },
    "Param name": {
        "ru-ru": "Идентификатор параметра",
    },
    "Value": {
        "ru-ru": "Значение",
    },
    "Param value": {
        "ru-ru": "Значение параметра",
    },
    "Telegram bot config": {
        "ru-ru": "Настройка телеграм-бота",
    },
    "Telegram bot configs": {
        "ru-ru": "Настройки телеграм-бота",
    },
    "Switch on": {
        "ru-ru": "Включать",
    },
    "Switch off": {
        "ru-ru": "Выключать",
    },
    "Switch": {
        "ru-ru": "Переключать",
    },
    "Pin": {
        "ru-ru": "Переключатель",
    },
    "Trigger time": {
        "ru-ru": "Время срабатывания",
    },
    "Cron notation": {
        "ru-ru": "Нотация Cron",
    },
    "Every minute": {
        "ru-ru": "Каждую минуту",
    },
    "Time trigger description": {
        "ru-ru": "Описание времени выполнения",
    },
    "Action": {
        "ru-ru": "Действие",
    },
    "Pin action": {
        "ru-ru": "Действие над переключателем",
    },
    "Is trigger active?": {
        "ru-ru": "Активна ли эта задача",
    },
    "Schedule config": {
        "ru-ru": "Настройка задачи по таймеру",
    },
    "Schedule configs": {
        "ru-ru": "Настройки задач по таймеру",
    },
}


def t(text):
    if LANGUAGE_CODE.lower() != "en-us":
        text = TRANSLATIONS.get(text, {}).get(LANGUAGE_CODE, text)
    return text
