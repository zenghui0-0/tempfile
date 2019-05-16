from _prerequisites import *
from PyUiApi.tests.camera_tests import *

test_result = SingleMethodRunner.run_single_test(CameraTests, "test_set_video_size_back_camera")

if test_result.wasSuccessful():
    print "PASS"
else:
    TestUtils.print_test_result_problems(test_result)
    print "FAIL"
