# Copyright (C) 2015  Jin, YingjunX <yingjunx.jin@intel.com>
# Intel Corporation All Rights Reserved.

# The source code contained or described herein and
# all documents related to the source code ("Material") are owned by
# Intel Corporation or its suppliers or licensors.

# Title to the Material remains with Intel Corporation or
# its suppliers and licensors.
# The Material contains trade secrets and proprietary and
# confidential information of Intel or its suppliers and licensors.
# The Material is protected by worldwide copyright and
# trade secret laws and treaty provisions.
# No part of the Material may be used, copied, reproduced, modified,
# published, uploaded, posted, transmitted, distributed
# or disclosed in any way without Intel's prior express written permission.
# No license under any patent, copyright, trade secret or
# other intellectual property right is granted to
# or conferred upon you by disclosure or delivery of the Materials,
# either expressly, by implication, inducement, estoppel or otherwise.

# Any license under such intellectual property rights must be express
# and approved by Intel in writing.

'''
@summary: Class for ChromeCast operation
@since: 09/15/2015
@author: Yingjun Jin
'''


import time
import os
from testlib.util.common import g_common_obj
from testlib.util.config import TestConfig
from testlib.util.repo import Artifactory
from testlib.graphics.tools import ConfigHandle


class HwuiImpl:

    '''
    classdocs
    '''

    def init_environment(self):
        """ Init the test environment
        """
        self.config = TestConfig()
        self.cfg_file = 'tests.hwui.binary.conf'
        cfg_arti = self.config.read(self.cfg_file, 'artifactory')
        config_handle = ConfigHandle()
        cfg_arti["location"] = config_handle.read_configuration('artifactory', 'location', '/etc/oat', 'sys.conf')
        cfg = self.config.read(self.cfg_file, 'binary')
        arti = Artifactory(cfg_arti.get('location'))
        binary_name = cfg.get("name")
        file_path = arti.get(binary_name)
        self.file_name = file_path.split("/")[-1]
        print "%s" % file_path
        g_common_obj.adb_cmd_common('push ' + file_path + ' /data/app/')
        g_common_obj.adb_cmd('chmod 777 /data/app/' + self.file_name)

    def run_case(self):
        """ run the binary file and check the result
        """
        assert g_common_obj.adb_cmd_capture_msg(
            '/data/app/' + self.file_name + "| grep Success"
        ), "The test failed"
        g_common_obj.assert_exp_happens()

    def run_hwui_unitest_case(self,case_name):
        """ run the binary file and check the result
        """
        output= g_common_obj.adb_cmd_capture_msg('/data/app/hwui_unit_tests' + ' --gtest_filter='+ case_name)
        assert output.find("PASSED")!=-1, "The test failed,output is %s" % output
        g_common_obj.assert_exp_happens()