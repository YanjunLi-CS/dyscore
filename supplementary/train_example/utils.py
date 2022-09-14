#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
utils.py: 
"""

import time
from contextlib import contextmanager
from config import logger


@contextmanager
def timer(message):
    """Context manager for timing snippets of code."""
    tick = time.time()
    yield
    tock = time.time()

    diff = tock - tick
    if diff >= 3600:
        duration = "{:.2f}h".format(diff / 3600)
    elif diff >= 60:
        duration = "{:.2f}m".format(round(diff / 60))
    else:
        duration = "{:.2f}s".format(diff)
    logger.info("{}: {}".format(message, duration))
