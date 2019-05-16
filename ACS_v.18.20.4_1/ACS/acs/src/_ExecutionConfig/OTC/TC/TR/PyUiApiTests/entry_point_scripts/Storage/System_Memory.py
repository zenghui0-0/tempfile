from _prerequisites import *
from PyUiApi.tests.storage_usb_tests.generic import *
import sys

test_result = SingleMethodRunner.run_single_test(StorageUSBTests, "test_memory")

if test_result.wasSuccessful():
    print "PASS"
else:
    TestUtils.print_test_result_problems(test_result)
    sys.exit("FAIL")
