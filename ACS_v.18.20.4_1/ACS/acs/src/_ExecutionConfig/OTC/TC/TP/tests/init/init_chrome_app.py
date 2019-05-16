import os
from testlib.util.uiatestbase import UIATestBase
#from testlib.util.repo import Artifactory
from testlib.dut_init.dut_init_impl import Function
from testlib.util.common import g_common_obj

class InitChrome(UIATestBase):

    def setUp(self):
        super(InitChrome, self).setUp()
        self._test_name = __name__
        print
        print "[Setup]: %s" % self._test_name
        cfg_file = 'tests.tablet.dut_init.conf'
        self.retry_num = self.config.read(cfg_file,'init_list').get("init_chrome_app")
        if self.retry_num is None:
            self.retry_num = 3
        self.retry_num = int(self.retry_num)
        self.func = Function()

    def tearDown(self):
        super(InitChrome, self).tearDown()
        print "[Teardown]: %s" % self._test_name

    def testInitChrome(self):
        """
        Init Chrome App
        """
        print "[RunTest]: %s" % self.__str__()

        succeed = False
        for i in range(self.retry_num):
            try:
                android_version_release = g_common_obj.adb_cmd_capture_msg("getprop |grep 'version.release'").split(':')[-1].strip()
                if (android_version_release == '[8.0.0]') or (android_version_release == '[8.1.0]'):
                    self.func.init_chrome()
                succeed = True
                break
            except Exception as e:
                print e
        assert succeed

