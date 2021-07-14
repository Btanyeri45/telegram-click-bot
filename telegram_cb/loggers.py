from typing import Callable, Optional

from rich import print
from rich.console import Console


def console_logger(target: Callable):
    def log(*args, **kwargs):
        message_dir = {
            'active':
                '[%s]Performing tasks[/%s] :money_with_wings::money_with_wings::money_with_wings:',
            'idle':
                '[%s]Patiently awaiting new offers[/%s] :seven_o’clock:',
        }
        console = Console()
        spinner = 'aesthetic'
        speed = 0.6
        message_style = 'blink italic green_yellow'
        message = message_dir['active'] % (message_style, message_style)
        console.clear()
        with console.status(message, spinner=spinner, speed=speed):
            target(*args, **kwargs)
        console.clear()
        print(message_dir['idle'] % ('blink bold red1', 'blink bold red1'))

    return log


@console_logger
def console_logger_demo():
    for _ in range(10):
        import time
        time.sleep(0.5)
    print('done')


if __name__ == '__main__':
    console_logger_demo()
