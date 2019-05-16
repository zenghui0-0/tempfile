from _prerequisites import *
from PyUiApi.tests.storage_usb_tests.with_adb.emulated import *

test_result = SingleMethodRunner.run_single_test(StorageUSBTestsEmulatedWithAdb, "test_create_a_file")

if test_result.wasSuccessful():
    print "PASS"
else:
    TestUtils.print_test_result_problems(test_result)
    sys.exit("FAIL")

