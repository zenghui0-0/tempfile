#!/usr/bin/env python

#######################################################################
#
# @description: DUT can act as PANU
# @note:        Connect to Wifi on DEV and close Wifi on DUT must be
#               made outside the test
# @author:      adrian.palko@intel.com
# @author:      lucia.huru@intel.com
#
#######################################################################

import sys

from testlib.base.base_utils import get_args
from testlib.scripts.wireless.bluetooth import bluetooth_steps, bt_utils

bluetooth_steps.LogInfo("##### INITIALIZE ######")()

# ############# Get parameters ############

globals().update(vars(get_args(sys.argv)))
if not script_args:
    raise Exception("--script-args is mandatory")
args = {}
for entry in script_args:
    key, val = entry.split("=")
    args[key] = val

# mandatory param
if "serial2" not in args.keys():
    raise Exception("serial2 parameter is mandatory")
serial_dev = args["serial2"]

# Initialize versions and names

DUT_VERSION = bluetooth_steps.GetAndroidVersion(serial=serial, blocking=True)()
DEV_VERSION = bluetooth_steps.GetAndroidVersion(serial=serial_dev, blocking=True)()
DUT_NAME = bluetooth_steps.GetBtMac(serial=serial, blocking=True)()
PAIRING_DEV_NAME = bluetooth_steps.GetBtMac(serial=serial_dev, blocking=True)()

try:

    # ########### Preconditions ###############
    # #########################################

    bluetooth_steps.LogInfo("######## SETUP ########")()

    # DUT: turn on BT
    bluetooth_steps.StopPackage(serial=serial, blocking=True)()
    bluetooth_steps.PressHome(serial=serial, blocking=True)()
    bluetooth_steps.OpenBluetoothSettings(serial=serial, use_intent=True, version=DUT_VERSION, blocking=True)()
    bluetooth_steps.ClickBluetoothSwitch(serial=serial, state="ON", version=DUT_VERSION, blocking=True)()

    # DEV: turn on BT, rename device and remove all paired devices
    bluetooth_steps.StopPackage(serial=serial_dev, blocking=True)()
    bluetooth_steps.PressHome(serial=serial_dev, blocking=True)()
    bluetooth_steps.OpenBluetoothSettings(serial=serial_dev, use_intent=True, version=DEV_VERSION, blocking=True)()
    bluetooth_steps.ClickBluetoothSwitch(serial=serial_dev, state="ON", version=DEV_VERSION, blocking=True)()

    # DUT: wait scan , rename device and remove all paired devices
    bluetooth_steps.WaitBtScanning(serial=serial, version=DUT_VERSION, blocking=True)()
    bluetooth_steps.BtChangeDeviceName(serial=serial,
                                       name=DUT_NAME, version=DUT_VERSION, blocking=True)()
    bluetooth_steps.BtRemoveAllPairedDevices(serial=serial, version=DUT_VERSION, blocking=True)()
    bluetooth_steps.CheckBtVisibility(serial=serial, version=DUT_VERSION, blocking=True)()

    # DEV: wait scan (should be already finished)
    bluetooth_steps.WaitBtScanning(serial=serial_dev, timeout_appear=0, version=DEV_VERSION, blocking=True)()
    bluetooth_steps.BtChangeDeviceName(serial=serial_dev,
                                       name=PAIRING_DEV_NAME, version=DEV_VERSION, blocking=True)()
    bluetooth_steps.BtRemoveAllPairedDevices(serial=serial_dev, version=DEV_VERSION, blocking=True)()
    bluetooth_steps.CheckBtVisibility(serial=serial_dev, version=DEV_VERSION, blocking=True)()

    # pair devices
    bt_utils.bt_pair_devices(serial=serial,
                             dev=serial_dev,
                             dut_name=DUT_NAME,
                             dev_name=PAIRING_DEV_NAME,
                             scan_max_attempts=5, version_dut=DUT_VERSION, version_dev=DEV_VERSION, blocking=True)
    # check dev internet connection
    bluetooth_steps.CheckInternetConnection(serial=serial_dev, blocking=True)()

    # ############### Test ####################
    # #########################################

    bluetooth_steps.LogInfo("##### ACTUAL TEST #####")()

    # activate bt tethering on DEV
    bluetooth_steps.BtSetTethering(serial=serial_dev, state="ON", tethering_settings_opened=False,
                                   version=DEV_VERSION)()
    # activate internet service on DUT
    bluetooth_steps.BtSetService(serial=serial, paired_device_name=PAIRING_DEV_NAME, state=True,
                                 service="Internet access", version=DUT_VERSION)()
    bluetooth_steps.WaitForState(serial=serial, device_name=PAIRING_DEV_NAME, connected=True, version=DUT_VERSION)()
    bluetooth_steps.CheckInternetAccessServiceState(serial=serial, state="ON", max_checks=15, version=DUT_VERSION)()


finally:

    # ########### Postconditions ##############
    # #########################################

    bluetooth_steps.LogInfo("####### CLEANUP #######")()

    # DUT: turn bt on if not already
    bluetooth_steps.StopPackage(serial=serial, critical=False)()
    bluetooth_steps.PressHome(serial=serial, critical=False)()
    bluetooth_steps.OpenBluetoothSettings(serial=serial, use_intent=True, version=DUT_VERSION, critical=False)()
    bluetooth_steps.ClickBluetoothSwitch(serial=serial, state="ON", version=DUT_VERSION, critical=False)()

    # DEV: turn off bt tethering, turn bt on if not already
    bluetooth_steps.StopPackage(serial=serial_dev, critical=False)()
    bluetooth_steps.PressHome(serial=serial_dev, critical=False)()
    bluetooth_steps.BtSetTethering(serial=serial_dev, state="OFF", tethering_settings_opened=False, version=DEV_VERSION,
                                   critical=False)()
    bluetooth_steps.OpenBluetoothSettings(serial=serial_dev, use_intent=True, version=DEV_VERSION, critical=False)()
    bluetooth_steps.ClickBluetoothSwitch(serial=serial_dev, state="ON", version=DEV_VERSION, critical=False)()

    # DUT: remove all paired devices and turn off BT
    bluetooth_steps.WaitBtScanning(serial=serial, version=DUT_VERSION, critical=False)()
    bluetooth_steps.BtRemoveAllPairedDevices(serial=serial, version=DUT_VERSION, critical=False)()
    bluetooth_steps.ClickBluetoothSwitch(serial=serial, state="OFF", version=DUT_VERSION, critical=False)()
    bluetooth_steps.StopPackage(serial=serial, critical=False)()
    bluetooth_steps.PressHome(serial=serial, critical=False)()

    # DEV: remove all paired devices and turn off BT
    bluetooth_steps.WaitBtScanning(serial=serial_dev, version=DEV_VERSION, critical=False)()
    bluetooth_steps.BtRemoveAllPairedDevices(serial=serial_dev, version=DEV_VERSION, critical=False)()
    bluetooth_steps.ClickBluetoothSwitch(serial=serial_dev, state="OFF", version=DEV_VERSION, critical=False)()
    bluetooth_steps.StopPackage(serial=serial_dev, critical=False)()
    bluetooth_steps.PressHome(serial=serial_dev, critical=False)()
