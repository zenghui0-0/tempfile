import os
from testlib.util.uiatestbase import UIATestBase
#from testlib.util.repo import Artifactory
from testlib.dut_init.dut_init_impl import Function

class InitCamera(UIATestBase):

    def setUp(self):
        super(InitCamera, self).setUp()
        self._test_name = __name__
        print
        print "[Setup]: %s" % self._test_name
        cfg_file = 'tests.tablet.dut_init.conf'
        self.retry_num = self.config.read(cfg_file,'init_list').get("init_camera_app")
        if self.retry_num is None:
            self.retry_num = 3
        self.retry_num = int(self.retry_num)
        self.func = Function()

    def tearDown(self):
        super(InitCamera, self).tearDown()
        print "[Teardown]: %s" % self._test_name

    def testInitCamera(self):
        """
        Init Camera App
        """
        print "[RunTest]: %s" % self.__str__()

        succeed = False
        for i in range(self.retry_num):
            try:
                #self.testLaunchCameraSuccess()
                self.func.init_camera()
                succeed = True
                break
            except Exception as e:
                print e
        assert succeed

    def testLaunchCameraSuccess(self):
        from testlib.camera.CameraCommon import CameraCommon

        self.camera=CameraCommon().switchPlatform()
        self.camera.startCameraApp()
        self.camera.stopCameraApp()
