#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
__init__.py.py:
"""

import pathlib
import os
import os.path as osp
import pandas as pd
import logging
import sys
from dyscore_model.config import model_config
from logging.handlers import TimedRotatingFileHandler


# PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent   # dyscore_model/dyscore_model
PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
# print(PACKAGE_ROOT)

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —"
    "%(funcName)s:%(lineno)d — %(message)s")
LOG_DIR = PACKAGE_ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'dyscore.log'


FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —"
    "%(funcName)s:%(lineno)d — %(message)s")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.WARNING)
    return file_handler


def get_logger(*, logger_name):
    """Get logger with prepared handlers."""

    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)  # logging.INFO

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False

    return logger

logger = get_logger(logger_name=__name__)

VERSION_PATH = PACKAGE_ROOT / 'VERSION'

with open(VERSION_PATH, 'r') as version_file:
    __version__ = version_file.read().strip()

logger.info(f'===> DyScore Model version: {__version__} <===')



