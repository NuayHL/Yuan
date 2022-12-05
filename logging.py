import os
import datetime
import logging
import sys

def Logging(loggerfilename: str):
    logger = logging.getLogger(loggerfilename)
    logger.setLevel("INFO")
    logger.propagate = False

    logfile = os.path.join(loggerfilename+'.log')

    def _utc8_aera(timestamp):
        now = datetime.datetime.utcfromtimestamp(timestamp) + datetime.timedelta(hours=8)
        return now.timetuple()

    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]:%(message)s')
    formatter.converter = _utc8_aera

    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
