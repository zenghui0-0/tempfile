"""
:copyright: (c)Copyright 2014, Intel Corporation All Rights Reserved.
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

:organization: INTEL MCG PSI
:summary: This file implements a Test Step to wait until the device becomes
          reachable.
:since:20/11/2014
:author: pblunie
"""
from Core.TestStep.DeviceTestStepBase import DeviceTestStepBase
from ErrorHandling.DeviceException import DeviceException


class WaitForDevice(DeviceTestStepBase):
    """
    Connect to the device
    """

    def run(self, context):
        """
        Runs the test step

        :type context: TestStepContext
        :param context: test case context
        """
        DeviceTestStepBase.run(self, context)

        api = self._device.get_uecmd("System")
        if not api.wait_for_device(self._pars.timeout_in_sec):
            raise DeviceException(DeviceException.OPERATION_FAILED,
                                  "wait_for_device timeout for %s" %
                                  self._pars.device)
