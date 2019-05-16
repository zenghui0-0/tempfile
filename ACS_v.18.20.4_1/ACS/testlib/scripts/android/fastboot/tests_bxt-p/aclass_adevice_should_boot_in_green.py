#!/usr/bin/env python

######################################################################
#
# @filename:    aclass_adevice_should_boot_in_green.py
# @description: Type "adb shell getprop ro.boot.verifiedbootstate" return "green"
#
# @run example:
#
#            python aclass_adevice_should_boot_in_green.py --serial=A6EC8F70 --script-args
#                                               relay_type=RLY08B
#                                               relay_port=/dev/serial/by-id/usb-Devantech_Ltd._USB-RLY08_00015234-if00
#                                               power_port=4
#
# @author:      haojiex.xie@intel.com
#
#######################################################################

##### imports #####
import os
import sys
import time
from testlib.scripts.android.adb import adb_steps
from testlib.scripts.connections.local import local_steps
from testlib.base.base_utils import get_args
from testlib.scripts.relay import relay_steps

##### initialization #####
globals().update(vars(get_args(sys.argv)))

args = {}
for entry in script_args:
    key, val = entry.split("=")
    args[key] = val

relay_type = args["relay_type"]
relay_port = args["relay_port"]
power_port = args["power_port"]

##### test start #####
def get_devices_info(command):
    r = os.popen(command)
    info = r.readlines()
    for line in info:
        line = line.strip("\r\n")
        line = line.split()
        for s in line:
            if "bxtp_abl" in s:
                return True
            if "gordon_peak" in s:
                return False

wait_ui = get_devices_info("adb shell getprop ro.product.device")

try:
    relay_steps.reboot_main_os(serial = serial,
                                 relay_type = relay_type,
                                 relay_port = relay_port,
                                 power_port = power_port,
                                 wait_ui = wait_ui,
                                 timeout = 300,
                                 delay_power_on = 30,
                                 device_info = "broxtonp")()

    adb_steps.root_connect_device(serial = serial)()
    time.sleep(5)

    command = "adb shell getprop ro.boot.verifiedbootstate"
    result = False
    r = os.popen(command)
    info = r.readlines()
    for line in info:
        line = line.strip("\r\n")
        line = line.split()
        for s in line:
            if "green" in s:
                result = True
    if not result:
        raise Exception("The test result did not achieve the desired results")

except:
    raise

finally:
    relay_steps.reboot_main_os(serial = serial,
                                 relay_type = relay_type,
                                 relay_port = relay_port,
                                 power_port = power_port,
                                 wait_ui = wait_ui,
                                 timeout = 300,
                                 delay_power_on = 30,
                                 device_info = "broxtonp")()

##### test end #####