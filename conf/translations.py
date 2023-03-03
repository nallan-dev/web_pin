from .settings import LANGUAGE_CODE

RU_EN_DICT = {
    # page_context
    "Здесь пока нет переключателей - настройте их": "There are no switches "
    "here yet - set them up",
    "Обновлено": "Updated",
    "Плановые задачи": "Planned tasks",
    # admin
    "Переключатели": "Switchers",
    "Переключатели - администрирование": "Switchers - administration",
    "Приложения": "Apps",
    "Невалидный Крон": "Invalid Cron",
    "Невалидная нотация. Строка должна содержать только знаки -/,*0123456789"
    ", и четыре одинарных пробела. Удобно настроить и скопировать строку"
    " можно здесь - https://crontab.guru/": "Invalid notation. The string must"
    " contain only characters -/,*0123456789, and four single spaces. "
    "Conveniently set up and copy the string"
    " you can here - https://crontab.guru/",
    # tbot
    "Обновить": "Refresh state",
    # models
    "Порядковый номер": "Index number",
    "Для отображения в списке": "For ordering in list",
    "Номер пина (BOARD)": "Pin num (BOARD)",
    "Нумерация GPIO BOARD": "GPIO BOARD numbering",
    "Назначение переключателя": "Switch name",
    'Например "Свет на кухне"': 'For example, "Light in the kitchen"',
    "Комментарий": "Comment",
    "Необязательное поле": "Optional field",
    "Текущее состояние": "Current state",
    "Включен или выключен": "On or off",
    "Активен": "Active",
    "Отображать ли в интерфейсах?": "Display in interfaces?",
    "Инвертировать состояние": "Invert state",
    'Инвертировать состояние пинов на уровне GPIO (т.е. "Включенный пин" = '
    "GPIO.LOW (gnd))": 'Invert state at GPIO-level (e.g. "Enabled pin" = '
    "GPIO.LOW (gnd))",
    "Настройка пина": "Pin config",
    "Настройки пинов": "Pin configs",
    "Токен телеграм-бота": "Telegram bot token",
    "Разрешенные id (через запятую)": "Allowed id (separated by commas)",
    "Идентификатор": "Name",
    "Идентификатор параметра": "Param name",
    "Значение": "Value",
    "Значение параметра": "Param value",
    "Настройка телеграм-бота": "Telegram bot config",
    "Настройки телеграм-бота": "Telegram bot configs",
    "Включать": "Switch on",
    "Выключать": "Switch off",
    "Переключать": "Switch",
    "Переключатель": "Pin",
    "Время срабатывания": "Trigger time",
    "Нотация Cron": "Cron notation",
    "Каждую минуту": "Every minute",
    "Описание времени выполнения": "Time trigger description",
    "Действие": "Action",
    "Действие над переключателем": "Pin action",
    "Активно": "Active",
    "Активна ли эта задача": "Is trigger active?",
    "Настройка задачи по таймеру": "Schedule config",
    "Настройки задач по таймеру": "Schedule configs",
}


def t(text):
    if LANGUAGE_CODE == "en-us" and text in RU_EN_DICT:
        text = RU_EN_DICT[text]
    return text
