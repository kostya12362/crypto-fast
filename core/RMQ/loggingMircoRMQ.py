import logging
import datetime
import os


class LoggerRMQ(object):

    def __new__(cls, name, format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO):
        os.makedirs(os.path.dirname(f"logs/log{datetime.datetime.now():%d-%m-%Y}.log"), exist_ok=True)
        logging.getLogger(name).setLevel(logging.INFO)
        logging.basicConfig(
            filename=f"logs/{name}-logs-{datetime.datetime.now():%d-%m-%Y}.txt",
            format="|%(levelname)-9s|%(asctime)s| %(message)s",
            datefmt="%I:%M",
            level=level,
        )
        logging.addLevelName(5, "UPDATE")

        return logging
