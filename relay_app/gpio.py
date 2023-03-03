import atexit
import logging
import sys

from django.conf import settings

__ACTIVE_PINS: dict[int, bool] = {}  # Global object to hold real pin states
gpio_logger = logging.getLogger("GPIO_handler")
if settings.DEBUG:
    gpio_logger.setLevel(logging.DEBUG)
    gpio_logger.addHandler(logging.StreamHandler(sys.stdout))


class GpioDummy:
    BOARD = "BOARD"
    OUT = "OUT"

    @classmethod
    def setmode(cls, *args, **kwargs):
        gpio_logger.info(f"GPIO setmode {args} {kwargs}")

    @classmethod
    def output(cls, *args, **kwargs):
        gpio_logger.info(f"SET GPIO OUT {args} {kwargs}")

    @classmethod
    def setup(cls, *args, **kwargs):
        gpio_logger.info(f"GPIO setup {args} {kwargs}")

    @classmethod
    def cleanup(cls):
        gpio_logger.info("GPIO cleanup")

    @classmethod
    def input(cls, *args):
        gpio_logger.info(f"GPIO check state {args}")


def switch_gpio(board_num: int, state: bool, invert_state: bool):
    if board_num not in settings.BOARD_NUMS:
        raise NotImplementedError(f"{board_num} not in settings.BOARD_NUMS")
    try:
        real_state = not state if invert_state else state
        if board_num not in __ACTIVE_PINS:
            GPIO.setup(board_num, GPIO.OUT, initial=real_state)
            __ACTIVE_PINS[board_num] = real_state
        else:
            if __ACTIVE_PINS[board_num] != real_state:
                GPIO.output(board_num, real_state)
                __ACTIVE_PINS[board_num] = real_state
    except Exception as e:
        report = f"Err while switching GPIO num {board_num} {type(e)} {e}"
        gpio_logger.critical(report)
        raise NotImplementedError(report)


@atexit.register
def clean_up():
    GPIO.cleanup()
    gpio_logger.info("GPIO Cleaned up at exit")


if settings.FAKE_GPIO:
    GPIO = GpioDummy
else:
    try:
        import RPi.GPIO as GPIO
    except Exception as e:
        report = (
            f"{e} - Are you on raspberry? If yes, try install GPIO via "
            f"pip. If not, set FAKE_GPIO = True in settings.py"
        )
        raise EnvironmentError(report)
GPIO.setmode(GPIO.BOARD)
