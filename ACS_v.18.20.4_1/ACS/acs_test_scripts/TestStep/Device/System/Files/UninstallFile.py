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
:summary: This file implements a Test Step to remove file(s) on device folder
:since:04/03/2014
:author: kturban
"""

from Core.TestStep.DeviceTestStepBase import DeviceTestStepBase
from ErrorHandling.DeviceException import DeviceException
from UtilitiesFWK.Utilities import Global


class UninstallFile(DeviceTestStepBase):

    """
    Remove file(s) on device
    """
    def run(self, context):
        """
        Runs the test step

        :type context: TestStepContext
        :param context: test case context
        """
        DeviceTestStepBase.run(self, context)

        status, msg = self._device.remove_device_files(self._pars.device_folder, self._pars.filename)

        if status != Global.SUCCESS:
            raise DeviceException(DeviceException.OPERATION_FAILED, msg)
        else:
            self.ts_verdict_msg = msg
