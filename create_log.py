import logging
import datetime
import os
import sys

def init(current_date_time_utc):
    path = os.path.abspath(os.path.dirname(__file__))
    if not os.path.isdir(f"{path}/logs"):
        os.mkdir(f"{path}/logs")
    now = current_date_time_utc
    logFileName = f'{path}/logs/{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}.log'
    logging.basicConfig(
        #handlers=[logging.FileHandler(logFileName, 'a', 'utf-8')],
        level = logging.INFO,
        format = '%(asctime)s %(levelname)-7.7s %(message)s',
        datefmt = '%d.%m.%y %H:%M:%S'
    )

    fileHnd = logging.FileHandler(logFileName, 'a', 'utf-8')
    formatter = logging.Formatter("%(asctime)s --ST %(levelname)s-- %(message)s --FN--")
    formatter.datefmt = '%d.%m.%y %H:%M:%S'
    formatter.level = logging.INFO
    fileHnd.setFormatter(formatter)

    log = logging.getLogger()  # root logger
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("chardet.charsetprober").setLevel(logging.WARNING)
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)
    log.addHandler(fileHnd)
    logging.info("logging setup ok")
    return logFileName

def writeInfo(log):
    logging.info(log)
