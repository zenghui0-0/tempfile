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
:summary: This file implements a Test Step to get mac address
:since 10/09/2014
:author: jfranchx
"""
from Core.TestStep.DeviceTestStepBase import DeviceTestStepBase
from ErrorHandling.AcsConfigException import AcsConfigException


class GetMacAddress(DeviceTestStepBase):
    """
    Implements the get MAC address step for Wireless Common
    """

    def __init__(self, tc_conf, global_conf, ts_conf, factory):
        """
        Constructor
        """
        DeviceTestStepBase.__init__(self, tc_conf, global_conf, ts_conf, factory)
        self._api = self._device.get_uecmd("Networking")

    def run(self, context):
        """
        Runs the test step

        @type context: TestStepContext
        @param context: test case context
        """
        DeviceTestStepBase.run(self, context)

        self._logger.info("Getting the %s Mac address..." % self._pars.interface)
        # Only WiFi MAC address is supported
        if self._pars.interface != "wlan0":
            msg = "Only wlan0 interface is supported - can't get %s MAC address" % self._pars.interface
            self._logger.error(msg)
            raise AcsConfigException(AcsConfigException.INVALID_PARAMETER, msg)

        # Where the information will be stored into the context?
        variable_to_set = self._pars.mac_addr

        value = self._api.get_interface_mac_addr(self._pars.interface)

        # We have the value, let's save it into the context
        context.set_info(variable_to_set, value)
        self.ts_verdict_msg = "VERDICT: %s stored as {0}".format(value) % variable_to_set
        self._logger.debug(self.ts_verdict_msg)
