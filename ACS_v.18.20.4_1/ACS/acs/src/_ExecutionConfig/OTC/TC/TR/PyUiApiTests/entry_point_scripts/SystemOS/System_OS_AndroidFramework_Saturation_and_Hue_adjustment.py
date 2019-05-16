from _prerequisites import *
from PyUiApi.tests.system_os_tests import *

test_result = SingleMethodRunner.run_single_test(SystemOsTests, "test_verify_saturation_and_hue")

if test_result.wasSuccessful():
    print "PASS"
else:
    TestUtils.print_test_result_problems(test_result)
    print "FAIL"
