#!/usr/bin/env python
# -*- coding: utf-8 -*-
# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08
from airtest.core.android.recorder import *
from airtest.core.android.adb import *
from devices_init.devices_init import args
from internal.tools.project_path import report_mp4


def start_recording():
    adb = ADB(serialno=args.devices)
    recorder = Recorder(adb)
    recorder.start_recording()
    return recorder


def stop_recording(recorder):
    recorder.stop_recording(
        output=report_mp4() + "/" + args.devices + args.task_id + ".mp4")
