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
:summary: WCDMA Mobile Originated SMS over CS on network simulator
:since: 10/02/2011
:author: jre
"""

import time

from UtilitiesFWK.Utilities import Global
from acs_test_scripts.Utilities.SmsUtilities import compute_sms_segments, SmsMessage
from LAB_WCDMA_SMS_PS_BASE import LabWcdmaSmsPsBase


class LabWcdmaSmsPsMo(LabWcdmaSmsPsBase):

    """
    WCDMA Mobile Originated SMS over PS on network simulator class.
    """

    def __init__(self, tc_name, global_config):
        """
        Constructor
        """
        # Call LAB_WCDMA_SMS_PS_BASE init function
        LabWcdmaSmsPsBase.__init__(self, tc_name, global_config)

        # Read SMS Service Center address
        self._sms_service_center_address = global_config.benchConfig.\
            get_parameters("CELLULAR_NETWORK").get_param_value("SMSC", "default")

        # Read DESTINATION_NUMBER from xml UseCase parameter file
        self._destination_number = \
            str(self._tc_parameters.get_param_value("DESTINATION_NUMBER"))
        if self._destination_number.upper() == "[PHONE_NUMBER]":
            self._destination_number = str(self._device.get_phone_number())

    def set_up(self):
        """
        Set up the test configuration
        .. warning:: Set the Data coding scheme using DATA_CODING_SCHEME value (CDK)
        """

        # Call the LAB_WCDMA_SMS_CS_BASE Setup function
        LabWcdmaSmsPsBase.set_up(self)

        # Set the default SMS service center
        time.sleep(self._wait_btwn_cmd)
        self._messaging_api.set_service_center_address(self._sms_service_center_address)

        return Global.SUCCESS, "No errors"

#------------------------------------------------------------------------------
    def run_test(self):
        """
        Execute the test
        """

        # Call the LAB_WCDMA_SMS_CS_BASE run_test function
        LabWcdmaSmsPsBase.run_test(self)

        # Calculate how many SMS will be sent to equipment
        time.sleep(self._wait_btwn_cmd)
        nb_segments = compute_sms_segments(
            self._sms_text, self._nb_bits_per_char)

        if nb_segments > 1:
            # Enable message queuing
            self._ns_messaging_3g.set_sms_message_queuing_state("ON")

        # Send SMS to equipment using SMS parameters :
        # - SMS_TEXT
        # - DESTINATION_NUMBER
        time.sleep(self._wait_btwn_cmd)
        self._messaging_api.send_sms(self._destination_number,
                                     self._sms_text)
        sms_sent = SmsMessage(self._sms_text, self._destination_number, "PSD")

        # Check SMS delivery status OK before timeout using
        # SMS_TRANSFER_TIMEOUT value and number of SMS to be received
        (result_verdict, result_message) = \
            self._ns_messaging_3g.check_sms_delivery_state(sms_sent, nb_segments,
                                                           self._sms_transfer_timeout)

        return result_verdict, result_message
