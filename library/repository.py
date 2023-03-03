from dataclasses import dataclass, fields

from library.adapter import db_adapter


@dataclass
class PinData:
    id: int
    board_num: int
    name: str
    state: bool
    comment: str
    order_id: int
    invert_state: bool


@dataclass
class ScheduleData:
    id: int
    pin_data_id: int
    cron_time: str
    describe_cron: str
    action: int
    active: bool
    comment: str

    def __bool__(self) -> bool:
        return self.active


@dataclass
class BotData:
    allowed_clients: list[int]
    telegram_token: str


@dataclass
class AppData:
    pins_data: dict[int, PinData]
    schedules_data: dict[int, ScheduleData]
    bot_data: BotData

    def update(self):
        actual_data = get_app_data()
        for field in fields(self):
            actual_value = getattr(actual_data, field.name)
            setattr(self, field.name, actual_value)


def get_pins_data() -> dict[int, PinData]:
    sql_pins = """
    SELECT
        id AS id,
        board_num AS board_num,
        command AS command,
        order_id AS order_id,
        comment AS comment,
        state AS state,
        invert_state AS invert_state
    FROM pin_data WHERE visible = TRUE;"""
    return {
        row["id"]: PinData(
            id=row["id"],
            board_num=row["board_num"],
            name=row["command"],
            order_id=row["order_id"],
            comment=row["comment"],
            state=bool(row["state"]),
            invert_state=bool(row["invert_state"]),
        )
        for row in db_adapter.fetch_rows(sql_pins)
    }


def get_schedules_data() -> dict[int, ScheduleData]:
    sql_schedule = """
    SELECT
        id AS id,
        pin_data_id AS pin_data_id,
        cron_time AS cron_time,
        describe_cron AS describe_cron,
        action AS action,
        active AS active,
        comment AS comment
    FROM schedule_data;"""
    return {
        row["id"]: ScheduleData(
            id=row["id"],
            pin_data_id=row["pin_data_id"],
            cron_time=row["cron_time"],
            describe_cron=row["describe_cron"],
            action=row["action"],
            active=bool(row["active"]),
            comment=row["comment"],
        )
        for row in db_adapter.fetch_rows(sql_schedule)
    }


def get_bot_data() -> BotData:
    sql_tgbot = "SELECT id AS id, value as value FROM bot_config;"
    data = {
        row["id"]: row["value"] for row in db_adapter.fetch_rows(sql_tgbot)
    }
    return BotData(
        allowed_clients=[
            int(s.strip()) for s in data["ALLOWED_CLIENTS"].split(",")
        ],
        telegram_token=data["TELEGRAM_TOKEN"],
    )


def get_app_data() -> AppData:
    with db_adapter:
        app_data = AppData(
            pins_data=get_pins_data(),
            schedules_data=get_schedules_data(),
            bot_data=get_bot_data(),
        )
    return app_data
