import logging
from colorlog import ColoredFormatter


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s: %(name)s  [%(asctime)s] -- %(message)s",
        datefmt='%d/%m/%Y %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger


class DualOutput:
    def __init__(self, file, terminal):
        self.file = file
        self.terminal = terminal

    def write(self, message):
        self.file.write(message)
        self.terminal.write(message)

    def flush(self):
        self.file.flush()
        self.terminal.flush()


class DualInput:
    def __init__(self, file, input_func=input):
        self.file = file
        self.input_func = input_func

    def __call__(self, prompt=""):
        response = self.input_func(prompt)
        self.file.write(prompt + response + "\n")
        self.file.flush()
        return response
