"""
@copyright: (c)Copyright 2013, Intel Corporation All Rights Reserved.
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
:summary: This file implements Test Step for WiFi AP set bandwidth
:since 16/07/2014
:author: jfranchx
"""
from acs_test_scripts.TestStep.Equipment.ConfigurableAP.APBase import APBase


class APWifiSetBandwidth(APBase):
    """
    Implements WiFi AP Set Bandwidth
    """

    def run(self, context):
        """
        Run the test step
        """
        APBase.run(self, context)

        # Set the WiFi Bandwidth
        self._configurable_ap.set_wifi_bandwidth(str(self._pars.bandwidth), self._pars.standard)