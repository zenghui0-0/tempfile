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
:summary: Use Case WCDMA Voice Call Mobile Originated
          and MO SMS and Released call
:since: 08/10/2012
:author: lvacheyx
"""

import time

from LAB_FIT_TEL_WCDMA_VC_SMS_CS_BASE import LabFitTelWcdmaVcSmsCsBase

from acs_test_scripts.Utilities.SmsUtilities import SmsMessage
from UtilitiesFWK.Utilities import Global


class LabFitTelWcdmaVcSmsCsMt(LabFitTelWcdmaVcSmsCsBase):

    """
    Lab reception of SMS Cs during a WCDMA voice call class.
    """

    def __init__(self, tc_name, global_config):
        """
        Constructor
        """

        # Call wcdma fit tel voice call sms base Init function
        LabFitTelWcdmaVcSmsCsBase.__init__(self, tc_name, global_config)

        # Read PHONE_NUMBER from testcase xml parameters
        if self._tc_parameters.get_param_value("PHONE_NUMBER") not in (None, ''):
            self._is_phone_number_checked = True
            if str(self._tc_parameters.get_param_value("PHONE_NUMBER")).isdigit():
                self._phone_number = self._tc_parameters.get_param_value("PHONE_NUMBER")

            # If value of PHONE_NUMBER from testcase xml is [PHONE_NUMBER], the value used
            # will be the phoneNumber defined in the Phone_Catalog.xml
            elif self._tc_parameters.get_param_value("PHONE_NUMBER") == "[PHONE_NUMBER]":
                self._phone_number = str(self._device.get_phone_number())
            else:
                self._phone_number = None
        else:
            self._phone_number = None
        self._sms_sent = SmsMessage(self._sms_text,
                                    self._phone_number,
                                    "CSD",
                                    self._messaging_3g,
                                    self._messaging_api,
                                    self._data_coding_sheme,
                                    self._nb_bits_per_char,
                                    self._sms_transfer_timeout,
                                    self._content_type,
                                    "MT")

# ------------------------------------------------------------------------------
    def set_up(self):
        """
        Set up the test configuration
        """
        # Call wcdma fit tel voice call sms base Setup function
        LabFitTelWcdmaVcSmsCsBase.set_up(self)

        self._sms_sent.configure_sms()

        return Global.SUCCESS, "No errors"
# ------------------------------------------------------------------------------

    def run_test(self):
        """
        Execute the test
        """

        # Call wcdma fit tel voice call sms base run_test function
        LabFitTelWcdmaVcSmsCsBase.run_test(self)

        # Check call state still "CONNECTED" during 5 seconds
        self._ns_voice_call_3g.check_call_connected(5)

        # Calculate how many SMS will be sent to equipment
        time.sleep(self._wait_btwn_cmd)

        # Send SMS
        self._sms_sent.send_sms()

        # Check call state still "CONNECTED" during 5 seconds
        self._ns_voice_call_3g.check_call_connected(5)

        # get sms received and Compare sent and received SMS (Text, Destination number)
        (result_verdict, result_message) = self._sms_sent.get_sms()

        self._logger.info(result_message)

        # Check call state still "CONNECTED" during 5 seconds
        self._ns_voice_call_3g.check_call_connected(5)

        # Stop voice call
        self._logger.info("Release voice call")
        self._voicecall_api.release()

        return result_verdict, result_message
