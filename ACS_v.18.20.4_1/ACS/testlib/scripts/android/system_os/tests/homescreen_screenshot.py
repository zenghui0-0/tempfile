#!/usr/bin/env python

######################################################################
#
# @filename:    factory_reset.py
# @description: Test factory reset.
#
# @run example:
#
#            python homescreen_screenshot.py --serial=A6EC8F70 --script-args
#                                               relay_type=RLY08B
#                                               relay_port=/dev/ttyACM0
#                                               power_port=4
#                                               v_up_port=1
#                                               v_down_port=2
#
# @author:      aurel.constantin@intel.com
#
#######################################################################

##### imports #####
import sys
from testlib.base.base_utils import get_args
from testlib.scripts.relay import relay_steps
from testlib.scripts.android.ui import ui_steps
from testlib.scripts.android.adb import adb_steps

##### initialization #####
globals().update(vars(get_args(sys.argv)))

args = {}
for entry in script_args:
    key, val = entry.split("=")
    args[key] = val

relay_type = args["relay_type"]
relay_port = args["relay_port"]
power_port = args["power_port"]
v_up_port = args["v_up_port"]
v_down_port = args["v_down_port"]
screenshots_folder = "/sdcard/Pictures/Screenshots"

##### test start #####
try:
    relay_steps.reboot_main_os(serial=serial,
                               relay_type=relay_type,
                               relay_port=relay_port,
                               power_port=power_port)()

    ui_steps.wake_up_device(serial=serial)()
    ui_steps.unlock_device(serial=serial)()

    # Take screenshot
    relay_steps.take_screenshot(serial=serial,
                                screenshots_folder=screenshots_folder,
                                relay_type=relay_type,
                                relay_port=relay_port,
                                power_port=power_port,
                                v_up_port=v_up_port,
                                v_down_port=v_down_port)()

finally:
    adb_steps.delete_folder_content(serial=serial,
                                    folder=screenshots_folder)()
#### test end #####
