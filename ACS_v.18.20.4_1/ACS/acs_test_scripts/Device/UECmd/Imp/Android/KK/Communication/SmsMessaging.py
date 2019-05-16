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
:summary: This file implements the Messaging UEcmd for KitKat Android device
:since: 06/12/2013
:author: rbertolx
"""
import time

from acs_test_scripts.Device.UECmd.Imp.Android.Common.Communication.\
SmsMessaging import SmsMessaging as SmsMessagingCommon
from acs_test_scripts.Device.UECmd.UECmdTypes import MSG_DB_PATH


class SmsMessaging(SmsMessagingCommon):
    """
    :summary: SmsMessaging UEcommands operations for 4.4 Android platforms
    using an C{Intent} based communication to the I{DUT}.
    """

    def __init__(self, device):
        """
        Constructor.
        """
        SmsMessagingCommon.__init__(self, device)

    def delete_all_sms(self):
        """
        Deletes all I{SMS}

        :return: None
        """
        self._logger.info("Delete all sms")
        self._exec("adb shell sqlite3 %s \"DELETE FROM sms\""
                   % MSG_DB_PATH)

        # Clear also the sms on sim card
        self.__delete_all_sms_on_sim()
