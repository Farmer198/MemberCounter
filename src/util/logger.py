import os
import logging
import logging.handlers
from termcolor import colored
from typing import List

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.WARNING:
            record.msg = colored(text = record.msg, color = 'yellow')
            record.levelname = colored(text = f"{record.levelname:<8}", color = 'yellow')
            record.name = colored(text = f"{record.name:<20}", color = 'yellow')

        if record.levelno == logging.ERROR:
            record.msg = colored(text = record.msg, color = 'red')
            record.levelname = colored(text = f"{record.levelname:<8}", color = 'red')
            record.name = colored(text = f"{record.name:<20}", color = 'red')

        if record.levelno == logging.DEBUG:
            record.msg = colored(text = record.msg, color = 'blue')
            record.levelname = colored(text = f"{record.levelname:<8}", color = 'blue')
            record.name = colored(text = f"{record.name:<20}", color = 'blue')

        if record.levelno == logging.INFO:
            record.msg = colored(text = record.msg, color = 'cyan')
            record.levelname = colored(text = f"{record.levelname:<8}", color = 'cyan')
            record.name = colored(text = f"{record.name:<20}", color = 'cyan')

        # not colored
        return logging.Formatter.format(self, record)

class Logger(logging.Logger):
    def __init__(self, client, name: str, level = logging.INFO) -> None:
        super().__init__(name, level)

        self.client = client
        self.extra_loggers: List[logging.Logger] = []

        # check directory
        self.check_directory()

        self.get_extra_loggers()
        self.setup_file_logger()
        self.setup_console_logger()

    def check_directory(self):
        path = "{}/logs".format(self.client.dirname)
        isExists = os.path.exists(path)
        if not isExists:
            os.mkdir(path)

    def get_extra_loggers(self):
        self.extra_loggers.append(logging.getLogger('discord'))
        self.extra_loggers.append(logging.getLogger('discord.http'))

        [logger.setLevel(self.level) for logger in self.extra_loggers]

    def setup_console_logger(self):
        # format's
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        log_fmt = '[{asctime}] [{levelname:<8}] [{name:<20}] >>> {message}'
        formatter = ColoredFormatter(log_fmt, dt_fmt, style='{') 

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        # add's the console logger to the extra_loggers
        self.addHandler(console_handler)
        [logger.addHandler(console_handler) for logger in self.extra_loggers]

    def setup_file_logger(self):
        # format's
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        log_fmt = '[{asctime}] [{levelname:<8}] [{name:<20}] >>> {message}'
        formatter = logging.Formatter(log_fmt, dt_fmt, style='{')

        file_handler = logging.handlers.RotatingFileHandler(
            filename = '{}/logs/{}.log'.format(self.client.dirname, self.client.__class__.__name__),
            encoding = 'utf-8',
            maxBytes = 32 * 1024 * 1024,# 32 MB
            backupCount = 5
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(self.level)

        # adds the file logger to the extra_loggers
        self.addHandler(file_handler)
        [logger.addHandler(file_handler) for logger in self.extra_loggers]
