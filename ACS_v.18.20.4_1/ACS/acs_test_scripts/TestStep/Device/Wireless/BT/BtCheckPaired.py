"""
:copyright: (c)Copyright 2013, Intel Corporation All Rights Reserved.
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
:summary: This file implements a Test Step that checks if a device (address) is paired
:since:18/12/2013
:author: fbongiax
"""

from TestStep.Device.Wireless.BT.Base import BtBase


class BtCheckPaired(BtBase):
    """
    Implements the test step to check if a device is paired
    """

    def run(self, context):
        """
        Runs the test step

        :type context: TestStepContext
        :param context: test case context
        """

        BtBase.run(self, context)

        paired = False
        address = self._pars.bdaddr

        list_paired_devices = self._api.list_paired_device()
        for element in list_paired_devices:
            if str(element.address).upper() == str(address).upper():
                paired = True
                break

        if not paired:
            self._raise_device_exception("Device %s is not paired" % address)
