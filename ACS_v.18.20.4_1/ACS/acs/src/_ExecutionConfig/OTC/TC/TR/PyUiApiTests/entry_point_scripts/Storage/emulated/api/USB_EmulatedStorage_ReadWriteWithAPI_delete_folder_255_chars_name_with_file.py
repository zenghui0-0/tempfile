from _prerequisites import *
from PyUiApi.tests.storage_usb_tests.with_api.emulated import *

test_result = SingleMethodRunner.run_single_test(StorageUSBTestsEmulatedWithApi, "test_delete_a_folder_255_char_name_with_file")

if test_result.wasSuccessful():
    print "PASS"
else:
    TestUtils.print_test_result_problems(test_result)
    sys.exit("FAIL")
