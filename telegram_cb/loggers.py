import time
from typing import Callable, Union

from rich import print as rich_print
from rich.console import Console

console: Console


def start_logger():
    global console
    console = Console()


def cleanup_console():
    console.clear()


def console_logger(target: Callable):
    def log(*args, **kwargs):
        message_dir = {
            "active": "[%s]Performing tasks[/%s] :money_with_wings::money_with_wings::money_with_wings:",
            "idle": "[%s]Patiently awaiting new offers[/%s] :seven_o’clock:",
        }
        spinner = "aesthetic"
        speed = 0.6
        message_style = "blink italic green_yellow"
        message = message_dir["active"] % (message_style, message_style)
        cleanup_console()
        with console.status(message, spinner=spinner, speed=speed):
            target(*args, **kwargs)
        cleanup_console()
        rich_print(message_dir["idle"] % ("blink bold red1", "blink bold red1"))

    return log


def console_show_stat(message: str, reuse_line: bool = False):
    m = f"[rosy_brown]STAT[/rosy_brown]: [pale_green1]{message}[/pale_green1]"
    if reuse_line:
        rich_print(m, end="\r")
    else:
        rich_print(m)


@console_logger
def console_logger_demo():
    for _ in range(10):
        time.sleep(0.5)
    rich_print("done")


if __name__ == "__main__":
    console_logger_demo()
