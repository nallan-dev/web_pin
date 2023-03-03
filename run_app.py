from threading import Thread

from conf import settings
from manage import main as manage_py
from scheduler.scheduler import cron_worker
from tbot.bot import run_bot


if __name__ == "__main__":
    manage_py("migrate")
    manage_py("cleanup_temp")

    if settings.USE_BOT:
        bot_thread = Thread(target=run_bot, daemon=True)
        bot_thread.start()

    schedule_tread = Thread(target=cron_worker, daemon=True)
    schedule_tread.start()

    manage_py(
        "runserver",
        f"0.0.0.0:{settings.WEB_APP_PORT}",
        "--nothreading",
        "--noreload",
    )
