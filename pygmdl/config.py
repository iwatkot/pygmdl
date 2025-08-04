"""Configuration file for the pygmdl package."""

import logging
import os
import sys
from typing import Literal

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 "
    "(KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
)
HEADERS = {"User-Agent": USER_AGENT}

SAT_URL = "https://mt0.google.com/vt/lyrs=s&hl=en&x=%d&y=%d&z=%d&s=Ga"
ROAD_URL = "http://mt1.google.com/vt/lyrs=h@162000000&hl=en&x=%d&s=&y=%d&z=%d"
TILES_DIRECTORY = os.path.join(os.getcwd(), "temp", "tiles")


class Logger(logging.Logger):
    """Handles logging to the file and stroudt with timestamps."""

    def __init__(
        self,
        level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "DEBUG",
    ):
        super().__init__("pygmdl")
        self.setLevel(level)
        self.stdout_handler = logging.StreamHandler(sys.stdout)

        formatter = "%(name)s | %(levelname)s | %(asctime)s | %(message)s"
        self.fmt = formatter
        self.stdout_handler.setFormatter(logging.Formatter(formatter))

        self.addHandler(self.stdout_handler)
