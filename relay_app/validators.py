import cron_descriptor
import pycron
from django.core.exceptions import ValidationError

from conf.translations import t


def validate_cron(cron_str):
    err_msg = t(
        "Невалидная нотация. Строка должна содержать только знаки "
        "-/,*0123456789, и четыре одинарных пробела. Удобно настроить"
        " и скопировать строку можно здесь - https://crontab.guru/"
    )
    try:
        pycron.is_now(cron_str)
        cron_descriptor.get_description(cron_str)
    except Exception:
        raise ValidationError(err_msg)
    spaces_counter = 0
    for char in cron_str:
        if char == " ":
            spaces_counter += 1
        if char not in " -/,*0123456789":
            raise ValidationError(err_msg)
    if spaces_counter != 4:
        raise ValidationError(err_msg)
    return cron_str
