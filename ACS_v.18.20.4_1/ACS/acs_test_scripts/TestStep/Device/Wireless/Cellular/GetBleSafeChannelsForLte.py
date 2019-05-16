"""
:copyright: (c)Copyright 2014, Intel Corporation All Rights Reserved.
The source code contained or described here in and all documents related to the source code ("Material") are owned by
Intel Corporation or its suppliers or licensors. Title to the Material remains with Intel Corporation or its suppliers
and licensors. The Material contains trade secrets and proprietary and confidential information of Intel or its
suppliers and licensors.

The Material is protected by worldwide copyright and trade secret laws and treaty provisions. No part of the Material
may be used, copied, reproduced, modified, published, uploaded, posted, transmitted, distributed, or disclosed
in any way without Intel's prior express written permission.

No license under any patent, copyright, trade secret or other intellectual property right is granted to or conferred
upon you by disclosure or delivery of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be express and approved by Intel in writing.

:organization: INTEL MCG
:summary: This file implements the step to get the BLE safe channels when using LTE.
:since: 2014-11-06
:author: emarchan

"""

from acs_test_scripts.TestStep.Device.Wireless.Cellular.GetSafeChannelsForLteBase import GetSafeChannelsForLteBase


class GetBleSafeChannelsForLte(GetSafeChannelsForLteBase):
    """
    Gets the bluetooth low energy safe channels when using LTE.
    """

    def __init__(self, tc_conf, global_conf, ts_conf, factory):
        GetSafeChannelsForLteBase.__init__(self, tc_conf, global_conf, ts_conf, factory)
        self._save_as = None

    def run(self, context):
        """
        Runs the test step

        @type context: TestStepContext
        @param context: test case context
        """
        GetSafeChannelsForLteBase.run(self, context)

        self.get_safe_range_and_store(context, "BLE", self._pars.ble_safe_channels)
