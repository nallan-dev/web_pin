from dataclasses import dataclass
from typing import Self

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from conf.translations import t
from library.repository import AppData, PinData, ScheduleData

API_PIN_PK_NAME = "pin_id"
API_SCHEDULE_PK_NAME = "schedule_id"


@dataclass
class RowKeyboardData:
    row: str
    callback_msg: str  # combined key: api_pk_name @ pk @ inverted state


@dataclass
class KeyboardData:
    KEY_SEP = "~||~"

    pins_keyboard_data: dict[int, RowKeyboardData]
    schedules_keyboard_data: dict[int, RowKeyboardData]

    def form_keyboard(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)
        pin_rows = [
            InlineKeyboardButton(
                text=pin_keyboard_data.row,
                callback_data=pin_keyboard_data.callback_msg,
            )
            for pin_keyboard_data in self.pins_keyboard_data.values()
        ]

        if pin_rows:
            keyboard.add(*pin_rows)

        for schedule_keyboard_data in self.schedules_keyboard_data.values():
            keyboard.add(
                InlineKeyboardButton(
                    text=schedule_keyboard_data.row,
                    callback_data=schedule_keyboard_data.callback_msg,
                )
            )

        keyboard.add(
            InlineKeyboardButton(text=t("Обновить"), callback_data="refresh")
        )
        return keyboard

    def form_pushed_button_text(self, pk_name: str, pk: str) -> str:
        result = " "
        if pk_name == API_PIN_PK_NAME and int(pk) in self.pins_keyboard_data:
            result = self.pins_keyboard_data[int(pk)].row
        elif (
            pk_name == API_SCHEDULE_PK_NAME
            and int(pk) in self.schedules_keyboard_data
        ):
            result = self.schedules_keyboard_data[int(pk)].row
        return result

    @classmethod
    def decode_from_callback_msg(
        cls, callback_msg: str
    ) -> list[str, str, str]:
        return callback_msg.split(cls.KEY_SEP)

    @classmethod
    def get_from_app_data(cls, app_data: AppData) -> Self:
        return cls(
            pins_keyboard_data=cls._form_pins_keyboard_data(
                app_data.pins_data
            ),
            schedules_keyboard_data=cls._form_schedules_keyboard_data(
                app_data.schedules_data,
                app_data.pins_data,
            ),
        )

    @classmethod
    def _form_pins_keyboard_data(
        cls,
        pins_data: dict[int, PinData],
    ) -> dict[int, RowKeyboardData]:
        pins_keyboard_data = {}
        for pin_id, pin_data in pins_data.items():
            pins_keyboard_data[pin_id] = RowKeyboardData(
                row=f"{cls._get_icon(pin_data.state)} {pin_data.name}",
                callback_msg=cls.KEY_SEP.join(
                    [
                        API_PIN_PK_NAME,
                        str(pin_data.id),
                        str(int(not pin_data.state)),
                    ]
                ),
            )
        return pins_keyboard_data

    @classmethod
    def _form_schedules_keyboard_data(
        cls,
        schedules_data: dict[int, ScheduleData],
        pins_data: dict[int, PinData],
    ) -> dict[int, RowKeyboardData]:
        schedules_keyboard_data = {}
        for schedule_id, schedule_data in schedules_data.items():
            action_verbose = t(
                {
                    0: "Включать",
                    1: "Выключать",
                    2: "Переключать",
                }[schedule_data.action]
            )
            schedules_keyboard_data[schedule_id] = RowKeyboardData(
                row="{icon} {action} {pin_name} {cron_description}".format(
                    icon=cls._get_icon(schedule_data.active),
                    action=action_verbose,
                    pin_name=pins_data[schedule_data.pin_data_id].name.lower(),
                    cron_description=schedule_data.describe_cron.lower(),
                ),
                callback_msg=cls.KEY_SEP.join(
                    [
                        API_SCHEDULE_PK_NAME,
                        str(schedule_data.id),
                        str(int(not schedule_data.active)),
                    ]
                ),
            )
        return schedules_keyboard_data

    @staticmethod
    def _get_icon(state: bool) -> str:
        return "🌕" if state else "🌑"

    @staticmethod
    def _replace_icon(text: str) -> str:
        if "🌕" in text:
            text = text.replace("🌕", "🌑")
        elif "🌑" in text:
            text = text.replace("🌑", "🌕")
        return text
