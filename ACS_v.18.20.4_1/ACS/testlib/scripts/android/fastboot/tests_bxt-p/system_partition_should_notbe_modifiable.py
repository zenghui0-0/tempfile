#!/usr/bin/env python

##### imports #####
import os
import sys
import time
import ConfigParser
from testlib.base.base_utils import get_args
from testlib.scripts.android.adb import adb_steps
from testlib.scripts.connections.local import local_steps
from testlib.scripts.android.fastboot import fastboot_steps
from testlib.scripts.android.fastboot import fastboot_utils

##### initialization #####
globals().update(vars(get_args(sys.argv)))
args = {}
for entry in script_args:
	key, val = entry.split("=")
	args[key] = val
flash_files = args["flash_files"]

##### test start #####
try:
	os.system("mkdir -p ./temp/files/flash ./temp/image/n/img")
	fastboot_utils.download_flash_scripts()

	conf_url = "https://shstor001.sh.intel.com/artifactory/acs_test_artifacts/OTC_Android_Auto_Test_Suite/resources/EBImage/System_FastBoot/fastboot.conf"
	fastboot_utils.download_file(url=conf_url, local_filename="./temp/fastboot.conf")
	config = ConfigParser.ConfigParser()
	config.read("./temp/fastboot.conf")
	fastboot_path = config.get("fastboot", "path")

	platform_name = fastboot_utils.get_platform_name(serial=serial)
	if platform_name == "bxtp_abl": image_platform = "image_m_bxt"
	if platform_name == "gordon_peak":
		ram_value = fastboot_utils.get_bxt_ram(serial=serial)
		if ram_value == "2g": image_platform = "image_o_bxt_2g"
		if ram_value == "4g": image_platform = "image_o_bxt_4g"
		if ram_value == "8g": image_platform = "image_o_bxt_4g"
	unsigned_boot_path = config.get(image_platform, "unsigned_boot")
	unsigned_boot_name = unsigned_boot_path.split("/")[-1]
	fastboot_utils.download_file(url=fastboot_path+unsigned_boot_path, local_filename="./temp/image/n/img/"+unsigned_boot_name)

	os.system("sed -i \"s/loglevel=3/loglevel=7/\" {0}".format("./temp/image/n/img/"+unsigned_boot_name))
	adb_steps.reboot(command="fastboot", reboot_timeout=300, serial=serial)()
	fastboot_steps.flash_image(partition_name="boot", file_name="./temp/image/n/img/"+unsigned_boot_name, serial=serial)()
	fastboot_steps.format_partition(partition_name="data", lock_dut=True, serial=serial)()
	fastboot_steps.continue_to_adb(serial=serial)()
	time.sleep(60)
	local_steps.wait_for_adb(timeout = 300, serial=serial)()

	check_point1 = False

	fastboot_utils.start_minicom(serial=serial)

	adb_steps.root_connect_device(serial=serial)()
	time.sleep(5)
	os.system("adb -s {0} remount rw /system".format(serial))
	time.sleep(30)

	fastboot_utils.kill_minicom()

	file_path = "./temp/files/minicom_result.txt"
	return_result = open(file_path).readlines()
	for line in return_result:
		if "Buffer I/O error on dev dm" in line and "lost sync page" in line: check_point1 = True

	if not check_point1:
		raise Exception("The test result did not achieve the desired results")

	fastboot_utils.flash_bxt(zip_file=flash_files, serial=serial)
	os.system("sudo rm -rf ./temp")

except:
	fastboot_utils.kill_minicom()
	fastboot_utils.flash_bxt(zip_file=flash_files, serial=serial)
	os.system("sudo rm -rf ./temp")
	raise
##### test end #####