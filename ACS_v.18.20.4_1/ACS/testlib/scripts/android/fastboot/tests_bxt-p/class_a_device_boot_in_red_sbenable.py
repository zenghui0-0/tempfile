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
	os.system("mkdir -p ./temp/files/flash ./temp/image/n ./temp/image/eb/user ./temp/image/eb/userdebug ./temp/image/eb/img")
	fastboot_utils.download_flash_scripts()

	conf_url = "https://shstor001.sh.intel.com/artifactory/acs_test_artifacts/OTC_Android_Auto_Test_Suite/resources/EBImage/System_FastBoot/fastboot.conf"
	fastboot_utils.download_file(url=conf_url, local_filename="./temp/fastboot.conf")
	config = ConfigParser.ConfigParser()
	config.read("./temp/fastboot.conf")
	fastboot_path = config.get("fastboot", "path")

	platform_name = fastboot_utils.get_platform_name(serial=serial)
	if platform_name == "bxtp_abl":
		image_platform = "image_m_bxt"
		eb_user_patch = "eb_579061_user_flashfiles_zip"
		eb_userdebug_patch = "eb_579061_userdebug_flashfiles_zip"
		eb_img_user_signed_corrupted_boot = "eb_579061_img_user_signed_corrupted_boot"
	if platform_name == "gordon_peak":
		zip_name = fastboot_utils.get_zip_name(zip_path=flash_files)
		if zip_name == "r0_bxtp_abl":
			image_platform = "image_m_bxt"
			eb_user_patch = "eb_579061_user_flashfiles_zip"
			eb_userdebug_patch = "eb_579061_userdebug_flashfiles_zip"
			eb_img_user_signed_corrupted_boot = "eb_579061_img_user_signed_corrupted_boot"

	eb_user_patch_flashfiles_zip_path = config.get(image_platform, eb_user_patch)
	eb_user_patch_flashfiles_zip_name = eb_user_patch_flashfiles_zip_path.split("/")[-1]
	fastboot_utils.download_file(url=fastboot_path+eb_user_patch_flashfiles_zip_path, local_filename="./temp/image/eb/user/"+eb_user_patch_flashfiles_zip_name)

	eb_userdebug_patch_flashfiles_zip_path = config.get(image_platform, eb_userdebug_patch)
	eb_userdebug_patch_flashfiles_zip_name = eb_userdebug_patch_flashfiles_zip_path.split("/")[-1]
	fastboot_utils.download_file(url=fastboot_path+eb_userdebug_patch_flashfiles_zip_path, local_filename="./temp/image/eb/userdebug/"+eb_userdebug_patch_flashfiles_zip_name)

	eb_img_user_signed_corrupted_boot_path = config.get(image_platform, eb_img_user_signed_corrupted_boot)
	eb_img_user_signed_corrupted_boot_name = eb_img_user_signed_corrupted_boot_path.split("/")[-1]
	fastboot_utils.download_file(url=fastboot_path+eb_img_user_signed_corrupted_boot_path, local_filename="./temp/image/eb/img/"+eb_img_user_signed_corrupted_boot_name)

	if platform_name == "bxtp_abl":
		fastboot_utils.flash_bxt_m_fused(eb_user_patch_flashfiles_zip_name=eb_user_patch_flashfiles_zip_name, eb_userdebug_patch_flashfiles_zip_name=eb_userdebug_patch_flashfiles_zip_name, support_flash=True, serial=serial)
	if platform_name == "gordon_peak":
		zip_name = fastboot_utils.get_zip_name(zip_path=flash_files)
		if zip_name == "r0_bxtp_abl":
			fastboot_utils.flash_bxt_m_fused(eb_user_patch_flashfiles_zip_name=eb_user_patch_flashfiles_zip_name, eb_userdebug_patch_flashfiles_zip_name=eb_userdebug_patch_flashfiles_zip_name, support_flash=True, serial=serial)

	adb_steps.reboot(command="fastboot", reboot_timeout=300, serial=serial)()
	fastboot_steps.fastboot_erase_partition(partition_name="boot", reboot=False, serial=serial)()
	fastboot_steps.flash_image(partition_name="boot", file_name="./temp/image/eb/img/"+eb_img_user_signed_corrupted_boot_name, lock_dut=True, serial=serial)()

	fastboot_utils.flash_bxt(flash_ioc="False", flash_ifwi="True", flash_android="False", zip_file="./temp/image/eb/user/"+eb_user_patch_flashfiles_zip_name, serial=serial, sleep_time=30, wait_for_adb=False)
	fastboot_utils.to_fastboot_by_script(serial=serial)
	time.sleep(30)
	local_steps.wait_for_fastboot(timeout=300, serial=serial)()

	check_point1 = False
	check_point2 = False
	fastboot_utils.start_minicom(serial=serial)
	os.system("fastboot reboot > /dev/null 2>&1")
	time.sleep(30)
	fastboot_utils.kill_minicom()

	local_steps.wait_for_fastboot(timeout=300, serial=serial)()

	file_path = "./temp/files/minicom_result.txt"
	return_result = open(file_path).readlines()
	for line in return_result:
		if "boot image doesn't verify" in line: check_point1 = True
		if "Failed to start boot image" in line: check_point2 = True

	if not check_point1 or not check_point2:
		raise Exception("The test result did not achieve the desired results")

	fastboot_utils.flash_bxt(zip_file=flash_files, serial=serial)
	os.system("sudo rm -rf ./temp")

except:
	fastboot_utils.kill_minicom()
	fastboot_utils.flash_bxt(zip_file=flash_files, serial=serial)
	os.system("sudo rm -rf ./temp")
	raise
##### test end #####