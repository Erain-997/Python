#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08
import logging
from airtest.utils.logger import get_logger
from internal.tools.project_path import log_path


def log(devices_id, level="INFO"):
    logger = get_logger("airtest")
    logger.setLevel(level)
    log_file = logging.FileHandler(log_path() + devices_id + ".log", encoding='utf-8')
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    log_file.setFormatter(formatter)
    logger.addHandler(log_file)
    log_file.close()
    return logger

