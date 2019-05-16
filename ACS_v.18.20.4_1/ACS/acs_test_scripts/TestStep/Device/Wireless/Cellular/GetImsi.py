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
:summary: This file implements a Test Step to get Imsi from device
:since 17/09/2014
:author: pblunie
"""
from ErrorHandling.DeviceException import DeviceException
from acs_test_scripts.TestStep.Device.Wireless.Cellular.CellularBase import CellularBase


class GetImsi(CellularBase):
    """
    Implements the get imsi test step for Cellular
    """
    def run(self, context):
        """
        Runs the test step

        @type context: TestStepContext
        @param context: test case context
        """
        CellularBase.run(self, context)

        self._logger.info("Getting the IMSI...")

        # Flight mode must be disable to use this function
        if self._networking_api.get_flight_mode() == 1:
            msg = "Can't get IMSI, Flight mode is currently ON"
            self._logger.error(msg)
            raise DeviceException(DeviceException.OPERATION_FAILED, msg)

        imsi = self._modem_api.get_imsi(self._pars.timeout)

        context.set_info(self._pars.save_as, imsi)
        self.ts_verdict_msg = str("VERDICT: %s stored as %s" % (imsi, self._pars.save_as))
        self._logger.debug(self.ts_verdict_msg)
