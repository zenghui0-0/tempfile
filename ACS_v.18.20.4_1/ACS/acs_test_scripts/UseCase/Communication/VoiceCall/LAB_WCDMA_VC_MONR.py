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
:summary: This file implements the WCDMA Voice Call Mobile Originated / Network release UC
:since: 19/08/2010
:author: ssa
"""

from UtilitiesFWK.Utilities import Global
from LAB_WCDMA_VC_BASE import LabWcdmaVcBase


class LabWcdmaVcMoNr(LabWcdmaVcBase):

    """
    Lab Wcdma Voice Call MO/NR.
    """

    def __init__(self, tc_name, global_config):
        """
        Constructor
        """
        # Call WCDMA VoiceCall base init function
        LabWcdmaVcBase.__init__(self, tc_name, global_config)

        # Read PHONE_NUMBER from test case xml file
        self._phone_number = \
            str(self._tc_parameters.get_param_value("PHONE_NUMBER"))
        if self._phone_number.upper() == "[PHONE_NUMBER]":
            self._phone_number = str(self._device.get_phone_number())
#------------------------------------------------------------------------------

    def run_test(self):
        """
        Execute the test
        """
        # pylint: disable=E1101
        # Disable this pylint error due to Enum class VOICE_CALL_STATE

        # Call WCDMA VoiceCall base run_test function
        LabWcdmaVcBase.run_test(self)

        # Release any previous call (Robustness)
        self._voice_call_api.release()

        # Dial using PHONE_NUMBER parameter
        self._voice_call_api.dial(self._phone_number)

        # Check call state "CONNECTED" before callSetupTimeout seconds
        self._ns_voice_call_3g.check_call_connected(self._call_setup_time,
                                                    blocking=False)

        # Wait for state "active" before callSetupTimeout seconds
        self._voice_call_api.wait_for_state(
            self._uecmd_types.VOICE_CALL_STATE.ACTIVE,
            self._call_setup_time)

        # Check call is connected for x seconds
        # (x is CALL_DURATION value in seconds)
        self._ns_voice_call_3g.is_voice_call_connected(self._call_duration)

        # Network Release call
        self._ns_voice_call_3g.voice_call_network_release()

        # Check voice call state is "IDLE"
        self._ns_voice_call_3g.check_call_state("IDLE",
                                                self._call_setup_time,
                                                blocking=False)

        # Check voice call state is "no_call"
        self._voice_call_api.wait_for_state(
            self._uecmd_types.VOICE_CALL_STATE.NOCALL,
            self._call_setup_time)

        # pylint: enable=E1101
        return Global.SUCCESS, "No errors"
