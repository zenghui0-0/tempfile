"""
@copyright: (c)Copyright 2013, Intel Corporation All Rights Reserved.
The source code contained or described here in and all documents related
to the source code ("Material") are owned by Intel Corporation or its
suppliers or licensors. Title to the Material remains with Intel Corporation
or its suppliers and licensors. The Material contains trade secrets and
proprietary and confidential information of Intel or its suppliers and
licensors.

The Material is protected by worldwide copyright and trade secret laws and
treaty provisions. No part of the Material may be used, copied, reproduced,
modified, published, uploaded, posted, transmitted, distributed, or disclosed
in any way without Intel's prior express written permission.

No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be express
and approved by Intel in writing.

@organization: INTEL MCG PSI
@summary: This file implements a Test Step to initialize SysDebug modules
@since 26/11/2013
@author: pbluniex
"""

from Core.TestStep.DeviceTestStepBase import DeviceTestStepBase

class SysDebugBase(DeviceTestStepBase):
    """
    Sysdebug base class for test steps
    """
    def __init__(self, tc_conf, global_conf, ts_conf, factory):

        """
        Constructor
        """
        DeviceTestStepBase.__init__(self, tc_conf, global_conf, ts_conf, factory)
        self._sysdebug_apis = None

    def run(self, context):
        DeviceTestStepBase.run(self, context)
        self._sysdebug_apis = context.get_info("SysDebug")
        if self._sysdebug_apis is None:
            self._sysdebug_apis = self._device.get_uecmd("SysDebug")
            context.set_info("SysDebug", self._sysdebug_apis)
