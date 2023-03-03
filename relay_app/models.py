from typing import Any

from django.conf import settings
from django.db import models

from conf.translations import t
from relay_app.gpio import switch_gpio
from relay_app.validators import validate_cron

# Create your models here.


class PinDataQuerySet(models.QuerySet):
    # bulk_delete from admin panel
    def delete(self, *args, **kwargs):
        # try to turn-off pins before deleting
        for pin_data in self:
            switch_gpio(
                pin_data.board_num,
                False,
                pin_data.invert_state,
            )
        super().delete()


class PinData(models.Model):
    BOARD_CHOICES = [(i, f"BOARD-{i}") for i in settings.BOARD_NUMS]

    objects = PinDataQuerySet.as_manager()

    order_id = models.PositiveIntegerField(
        verbose_name=t("Порядковый номер"),
        help_text=t("Для отображения в списке"),
        unique=True,
    )
    board_num = models.PositiveIntegerField(
        verbose_name=t("Номер пина (BOARD)"),
        help_text=t("Нумерация GPIO BOARD"),
        unique=True,
        choices=BOARD_CHOICES,
    )
    command = models.CharField(
        max_length=30,
        unique=True,
        verbose_name=t("Назначение переключателя"),
        help_text=t('Например "Свет на кухне"'),
    )
    comment = models.TextField(
        verbose_name=t("Комментарий"),
        help_text=t("Необязательное поле"),
        blank=True,
        null=True,
    )
    state = models.BooleanField(
        default=False,
        verbose_name=t("Текущее состояние"),
        help_text=t("Включен или выключен"),
    )
    invert_state = models.BooleanField(
        default=False,
        verbose_name=t("Инвертировать состояние"),
        help_text=t(
            "Инвертировать состояние пинов на уровне GPIO "
            '(т.е. "Включенный пин" = GPIO.LOW (gnd))'
        ),
    )
    visible = models.BooleanField(
        default=True,
        verbose_name=t("Активен"),
        help_text=t("Отображать ли в интерфейсах?"),
    )

    def __str__(self):
        return self.command

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "board_num": self.board_num,
            "state": self.state,
            "name": self.command,
            "comment": self.comment,
            "invert_state": self.invert_state,
        }

    def switch(self, state: bool):
        self.state = state
        self.save()

    def save(self, *args, **kwargs):
        if not self.visible:
            self.state = False
        switch_gpio(self.board_num, self.state, self.invert_state)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        switch_gpio(self.board_num, False, self.invert_state)
        super().delete(*args, **kwargs)

    @classmethod
    def init_pin_state(cls):
        for elem in cls.objects.filter(visible=True):
            switch_gpio(elem.board_num, elem.state, elem.invert_state)

    class Meta:
        ordering = ["order_id"]
        verbose_name = t("Настройка пина")
        verbose_name_plural = t("Настройки пинов")
        db_table = "pin_data"


class ScheduleData(models.Model):
    ACTION_CHOICES = [
        (0, t("Выключать")),
        (1, t("Включать")),
        (2, t("Переключать")),
    ]
    pin_data = models.ForeignKey(
        PinData,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name=t("Переключатель"),
    )
    cron_time = models.CharField(
        max_length=100,
        default="* * * * *",
        verbose_name=t("Время срабатывания"),
        help_text=t("Нотация Cron"),
        validators=[validate_cron],
    )
    describe_cron = models.TextField(
        max_length=200,
        default=t("Каждую минуту"),
        verbose_name=t("Описание времени выполнения"),
    )
    action = models.PositiveSmallIntegerField(
        choices=ACTION_CHOICES,
        verbose_name=t("Действие"),
        help_text=t("Действие над переключателем"),
    )
    active = models.BooleanField(
        default=True,
        verbose_name=t("Активно"),
        help_text=t("Активна ли эта задача"),
    )
    comment = models.CharField(
        max_length=200, verbose_name=t("Комментарий"), blank=True, null=True
    )

    def __str__(self):
        return str(self.pin_data) + " " + str(self.action)

    def get_action_name(self) -> str:
        for action, verbose in self.ACTION_CHOICES:
            if self.action == action:
                return verbose

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.pk,
            "pin_board_num": self.pin_data.board_num,
            "pin_command": self.pin_data.command,
            "cron_time": self.cron_time,
            "cron_verbose": self.describe_cron,
            "action": self.action,
            "action_name": self.get_action_name(),
            "active": self.active,
        }

    class Meta:
        ordering = ["pin_data"]
        verbose_name = t("Настройка задачи по таймеру")
        verbose_name_plural = "  " + t("Настройки задач по таймеру")
        db_table = "schedule_data"


class BotConfig(models.Model):
    TELEGRAM_TOKEN_ID = "TELEGRAM_TOKEN"
    ALLOWED_CLIENTS_ID = "ALLOWED_CLIENTS"

    ID_CHOICES = [
        (TELEGRAM_TOKEN_ID, t("Токен телеграм-бота")),
        (ALLOWED_CLIENTS_ID, t("Разрешенные id (через запятую)")),
    ]
    id = models.TextField(
        max_length=40,
        choices=ID_CHOICES,
        verbose_name=t("Идентификатор"),
        help_text=t("Идентификатор параметра"),
        primary_key=True,
    )
    value = models.TextField(
        max_length=400,
        verbose_name=t("Значение"),
        help_text=t("Значение параметра"),
    )

    def __str__(self):
        return self.id

    @staticmethod
    def parse_allowed_ids(value: str) -> list[int]:
        allowed_clients = [int(s.strip()) for s in value.split(",")]
        return allowed_clients

    class Meta:
        ordering = ["id"]
        verbose_name = t("Настройка телеграм-бота")
        verbose_name_plural = t("Настройки телеграм-бота")
        db_table = "bot_config"


PinData.init_pin_state()
