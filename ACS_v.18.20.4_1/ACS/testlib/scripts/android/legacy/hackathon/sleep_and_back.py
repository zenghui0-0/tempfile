#!/usr/bin/env python
#######################################################################
#
# @filename:    vim_and_back.py
# @description: Hackaton script
# @author:      ion-horia.petrisor@intel.com
#
# python sleep_and_back.py --serial 10.237.104.142:5555
#                          --script-args app-to-test=Shazam
#                                        wait-time=2000
#                                        sleep-time=10000
#                                        host-path=/home/oane/screens
#
#######################################################################

from testlib.scripts.android.adb import adb_steps
from testlib.scripts.android.ui import ui_steps
from testlib.scripts.file import file_steps
from testlib.base.base_utils import get_args
import sys
import time

globals().update(vars(get_args(sys.argv)))

adb_steps.connect_device(
    serial = serial,
    port = adb_server_port
)()

args = {}
for entry in script_args:
    key, val = entry.split("=")
    args[key] = val

app_to_test = args["app-to-test"]
wait_time = int(args["wait-time"])/1000
sleep_time = int(args["sleep-time"])/1000
host_path = args["host-path"]

ui_steps.press_home()()

################## Openning app to test
ui_steps.open_app_from_allapps(view_to_find = {"text": app_to_test})()
time.sleep(wait_time)

################## Taking initial screenshot
adb_steps.take_screenshot_given_path(screenshot_file = "sleep_initial.png",
                                     host_path = host_path)()

################## Go to homescreen
ui_steps.put_device_into_sleep_mode()()
time.sleep(sleep_time)
ui_steps.wake_up_device()()
time.sleep(wait_time)

################## Taking final screenshot
adb_steps.take_screenshot_given_path(screenshot_file = "sleep_final.png",
                                     host_path = host_path)()

################## Compare the two screenshots
file_steps.compare_images(first_file = host_path + "/sleep_initial.png",
                          second_file = host_path + "/sleep_final.png",
                          tolerance = 10)()

ui_steps.press_home()()
