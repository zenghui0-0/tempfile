from _prerequisites import *
from PyUiApi.tests.system_os_tests import *

test_result = SingleMethodRunner.run_single_test(SystemOsTests, "test_multi_user_shell")

if test_result.wasSuccessful():
    print "TEST_PASSED"
else:
    TestUtils.print_test_result_problems(test_result)
    print "FAIL"
