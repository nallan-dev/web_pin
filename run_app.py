from threading import Thread

import cherrypy
from django.core.wsgi import get_wsgi_application

from conf import settings
from manage import main as manage_py
from scheduler.scheduler import cron_worker
from tbot.bot import run_bot


def production_ready():
    app = get_wsgi_application()  # django_app

    cherrypy.config.update(
        {
            "server.socket_host": "0.0.0.0",
            "server.socket_port": settings.WEB_APP_PORT,
            "server.thread_pool": 1,
            "engine.autoreload.on": False,
            "checker.on": False,
            "tools.log_headers.on": False,
            "request.show_tracebacks": False,
            "request.show_mismatched_params": False,
            "log.screen": False,
        }
    )

    cherrypy.tree.graft(app, "/")
    cherrypy.engine.start()
    print("Started!")
    cherrypy.engine.block()


if __name__ == "__main__":
    manage_py("migrate")
    manage_py("cleanup_temp")
    print("Starting service...")

    if settings.USE_BOT:
        bot_thread = Thread(target=run_bot, daemon=True)
        bot_thread.start()

    schedule_tread = Thread(target=cron_worker, daemon=True)
    schedule_tread.start()

    if settings.DEBUG:
        manage_py(
            "runserver",
            f"0.0.0.0:{settings.WEB_APP_PORT}",
            "--nothreading",
            "--noreload",
        )
    else:
        production_ready()
