#!/usr/bin/env python

##### imports #####
import os
import sys
import time
from testlib.scripts.android.adb import adb_steps
from testlib.scripts.connections.local import local_steps
from testlib.base.base_utils import get_args

##### initialization #####
globals().update(vars(get_args(sys.argv)))

##### test start #####
adb_steps.root_connect_device(serial = serial)()
time.sleep(5)

command = "adb shell ps | grep gatekeeperd"
r = os.popen(command)
info = r.readlines()
for line in info:
    line = line.strip("\r\n")
    line = line.split()
    local_steps.command("adb -s {} shell kill {}".format(serial, line[1]))()
time.sleep(5)

command = "adb shell ps | grep gatekeeperd"
r = os.popen(command)
info = r.readlines()
if not info:
    raise Exception("The test result did not achieve the desired results")
##### test end #####