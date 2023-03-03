import time
from datetime import datetime

import pycron

from library.clients import switch_data
from library.loggers import get_logger
from library.repository import get_app_data
from tbot.helpers import API_PIN_PK_NAME

logger = get_logger("scheduler")

APP_DATA = get_app_data()


def process_schedule_jobs(current_time: datetime):
    APP_DATA.update()
    active_schedules = [s for s in APP_DATA.schedules_data.values() if s]
    for schedule_data in active_schedules:
        if not pycron.is_now(schedule_data.cron_time, current_time):
            continue
        target_pin = APP_DATA.pins_data[schedule_data.pin_data_id]
        to_state = schedule_data.action
        if to_state == 2:  # change state to opposite current
            to_state = int(not target_pin.state)
        elif to_state == int(target_pin.state):
            continue
        switch_data(API_PIN_PK_NAME, target_pin.id, to_state, logger)


def cron_worker():
    logger.info("Start schedule worker")
    while True:
        time.sleep(0.8)
        now = datetime.now()
        if now.second:  # we work only when second == 0
            continue
        try:
            process_schedule_jobs(now)
        except Exception as e:
            logger.error(f"Scheduler main loop: {type(e)} {e}")
        time.sleep(1.0)


if __name__ == "__main__":
    cron_worker()
