# Raspberry WebPin
## _Control GPIO pin's output via web interface, scheduled tasks or optional telegram bot_

This is a simple web app that allows you to switch on/off GPIO pins using webpage, scheduled tasks or additional telegram bot. All this features easy to set up in comfortable admin web-panel. Supports English and Russian language.
## Features
- Set up pins (name, ordering, etc.) and control them remotely from lan
- Set up telegram bot (just token and chat-id whitelist) and control pins form anywhere
- Set up sheduled pin tasks in admin panel and enable-disable them remotely

Telegram-bot can be easy disabled in settings if you don't need them.

App uses Django's built-in devserver with forced single-thread mode, to avoid possibly conflicts with pin commands.

Usage with full mode (app, bot, schedule_cron_worker) ~ 25Mb RAM

## Installation

Requires installed locales ru_RU.UTF-8 and/or en_US.UTF-8 (you can install them in raspi-config)

Also don't forget set up timezone (in raspi-config)

After that reboot and start to install

Tested on PiZero, Pi4B (Raspbian OS) and PC (Ubuntu 22.04)

WebPin requires to run just python3.11 and some pip-libraries:

1) Create and activate new python virtual environment if needed.
2) Check py_3_11_requirements.txt, uncomment lines if you on raspberry
3) Check conf/settings.py, all actual settings are on top of file
4) In terminal (in folder with run_app.py):
```
pip install -r py_3_11_requirements.txt
python run_app.py
```
NOTE: If you set in settings USE_BOT=True then after run_app you see error messages in console like this:
```
A request to the Telegram API was unsuccessful. Error code: 401. Description: Unauthorized
```
Don't afraid, just set valid Telegram bot token in web_app admin panel, then restart.
5) It's recommended to add "python manage.py cleanup_temp" command to system cron (e.g. once a day)
