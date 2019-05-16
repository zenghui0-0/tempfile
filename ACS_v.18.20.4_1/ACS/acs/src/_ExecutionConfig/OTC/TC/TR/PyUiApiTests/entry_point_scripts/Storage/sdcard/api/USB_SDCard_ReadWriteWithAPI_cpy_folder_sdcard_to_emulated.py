from _prerequisites import *
from PyUiApi.tests.storage_usb_tests.with_api.portable import *

test_result = SingleMethodRunner.run_single_test(StorageUSBTestsPortableWithApi, "test_copy_folder_with_file_sdcard_to_emulated")

if test_result.wasSuccessful():
    print "PASS"
else:
    TestUtils.print_test_result_problems(test_result)
    sys.exit("FAIL")
