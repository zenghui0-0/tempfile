#Copyright (C) 2014  Lan, SamX <samx.lan@intel.com>
#Intel Corporation All Rights Reserved.

#The source code contained or described herein and
#all documents related to the source code ("Material") are owned by
#Intel Corporation or its suppliers or licensors.

#Title to the Material remains with Intel Corporation or
#its suppliers and licensors.
#The Material contains trade secrets and proprietary and
#confidential information of Intel or its suppliers and licensors.
#The Material is protected by worldwide copyright and
#trade secret laws and treaty provisions.
#No part of the Material may be used, copied, reproduced, modified,
#published, uploaded, posted, transmitted, distributed
#or disclosed in any way without Intel's prior express written permission.
#No license under any patent, copyright, trade secret or
#other intellectual property right is granted to
#or conferred upon you by disclosure or delivery of the Materials,
#either expressly, by implication, inducement, estoppel or otherwise.

#Any license under such intellectual property rights must be express
#and approved by Intel in writing.

'''
@summary: test data is not erased after GOTA update
@since: 11/12/2014
@author: Sam Lan(samx.lan@intel.com)
'''
import os
from testlib.util.uiatestbase import UIATestBase
from testlib.gota.gota_impl import gotaImpl
from testlib.system.system_impl import SystemImpl
from testlib.common.common import g_common_obj2

#from testlib.domains.settings_impl import SettingsImpl
class BiosUpdateAfterGOTA(UIATestBase):
    """
    @summary: Test bios is updated after GOTA update
    """

    def setUp(self):
        super(BiosUpdateAfterGOTA, self).setUp()
        cfg_file = os.path.join(os.environ.get('TEST_DATA_ROOT', ''), \
            'tests.tablet.gota.conf')
        self._test_name = __name__
        print "[Setup]: %s" % self._test_name
        self.cfg = self.config.read(cfg_file, 'gota')
        self.gota= gotaImpl(self.cfg)
        self.system=SystemImpl(self.cfg)
        self.ssid = self.config.read(cfg_file,'wifisetting').get("ssid")
        self.passwd = self.config.read(cfg_file,'wifisetting').get("passwd")
    def tearDown(self):
        print "[Teardown]: %s" % self._test_name
        super(BiosUpdateAfterGOTA, self).tearDown()
        self.cfg = None

    def testBiosUpdateAfterGOTA(self):
        """
        This test case is to test basic GOTA update function

        Test Case Precondition:
        set screen lock as none, and sleep time to be more than 10 minutes

        Test Case Step:
        1. check base bios
        2. process GOTA update
        3. check update bios

        Expect Result:
        1. check base bios successfully
        2. DUT can GOTA update successfully
        3. check the update bios successfully

        The real implementation will be in SystemImpl class.
        """
        print "[RunTest]: %s" % self.__str__()

        sn=g_common_obj2.getSerialNumber()
        cm="adb -s %s shell getprop ro.product.device" %sn
        device=os.popen(cm).read().strip()
        print device
        if device=="st70408_4_coho":
            target_bios=self.cfg.get("target_bios_trekstor")
            
        elif device=="one7_0_4_coho":
            target_bios=self.cfg.get("target_bios_one704")
            
        elif device=="one695_1_coho":
            target_bios=self.cfg.get("target_bios_one695")
            
        elif device=="one8_0_1_coho":
            target_bios=self.cfg.get("target_bios_one801")
            
        elif device=="ecs210a_0_coho":
            target_bios=self.cfg.get("target_bios_ecs210a")
        self.gota.check_bios_version(target_bios)
