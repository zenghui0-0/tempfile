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
:summary: This file implements a Test Step to init a voice call
:since: 23/06/2014
:author: jfranchx
"""

from Core.TestStep.DeviceTestStepBase import DeviceTestStepBase


class InitiateVoiceCall(DeviceTestStepBase):
    """
    Implements the test step to init a voice call
    """

    def __init__(self, tc_conf, global_conf, ts_conf, factory):
        """
        Constructor
        """

        DeviceTestStepBase.__init__(self, tc_conf, global_conf, ts_conf, factory)

        self._voice_call_api = self._device.get_uecmd("VoiceCall")
        self._networking_api = self._device.get_uecmd("Networking")

    def run(self, context):
        """
        Runs the test step

        :type context: TestStepContext
        :param context: test case context
        """

        DeviceTestStepBase.run(self, context)

        if self._pars.vc_type != "CIRCUIT":
            msg = "Can't perform VC_TYPE - unsupported type : %s" % str(self._pars.vc_type)
            self._logger.error(msg)
            self._raise_device_exception(msg)

        if self._networking_api.get_flight_mode() == 1 and self._pars.expected_result != "FAILED":
            msg = "Can't perform VC_DIAL : flight mode is enabled"
            self._logger.error(msg)
            self._raise_device_exception(msg)
        check = False
        if self._pars.expected_result == "FAILED":
            check = True

        try:
            self._voice_call_api.dial(self._pars.number_to_call, check)
        except:
            if self._pars.expected_result == "FAILED":
                self._logger.info("Call was unsuccessful as it was planned")
            else:
                raise
        else:
            if self._pars.expected_result == "FAILED":
                self._raise_device_exception("Voice call is successful but it should have failed")
