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

:organization: INTEL NDG SW DEV
:summary: This file implements a Test Step to retreive the name of a BT device
:since:02/03/2015
:author: msouyrix
"""
from acs_test_scripts.TestStep.Device.Wireless.BT.Base import BtBase


class BtGetName(BtBase):
    """
    Implements the test step to get BT Address
    """

    def run(self, context):
        """
        Runs the test step

        :type context: TestStepContext
        :param context: test case context
        """

        BtBase.run(self, context)

        # Get the BT name and post it in the context
        address = self._api.get_bt_device_name()
        context.set_info(self._pars.save_as, address)