"""
@copyright: (c)Copyright 2014, Intel Corporation All Rights Reserved.
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
:summary: This file implements a Test Step to get WiFi scan always available
:since 06/01/2015
:author: jfranchx
"""
from ErrorHandling.DeviceException import DeviceException
from acs_test_scripts.TestStep.Device.Wireless.Wifi.WifiBase import WifiBase


class WifiGetScanAlwaysAvailable(WifiBase):
    """
    Implements the get scan always available option test step for WiFi
    """

    def run(self, context):
        """
        Runs the test step

        @type context: TestStepContext
        @param context: test case context
        """
        WifiBase.run(self, context)

        self._logger.info("Getting the WiFi Scan always available status...")

        # Where the information will be stored into the context?
        variable_to_set = self._pars.save_scan_always_available

        state = self._api.get_wifi_scan_always_available()

        if state not in ["ON", "OFF"]:
            msg = "ERROR - Unknown WiFi scan always available state : %s" % state
            self._logger.debug(msg)
            raise DeviceException(DeviceException.OPERATION_FAILED, msg)

        # We have the value, let's save it into the context
        context.set_info(variable_to_set, state)
        self.ts_verdict_msg = "VERDICT: %s stored as {0}".format(state) % variable_to_set
        self._logger.debug(self.ts_verdict_msg)