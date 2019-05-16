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

@organization: INTEL MCG PSI
@summary: unit test
@since 04/04/2014
@author: obouzain
"""

import mock

from unit_test.UtTestStep.UTestTestStepBase import UTestTestStepBase
from Core.TestStep.TestStepContext import TestStepContext
from UtilitiesFWK.Utilities import TestConst
from acs_test_scripts.TestStep.Device.Wireless.GNSS.GNSSGetPower import GNSSGetPower


class GNSSGetPowerTest(UTestTestStepBase):
    """
    SetPower test cases
    """

    def setUp(self):
        """
        Set up
        """
        UTestTestStepBase.setUp(self)
        self._dest_var = "GPS_cur_state"

        self._context = TestStepContext()

    def test_get_power_on_ok(self):
        sut = self._create_sut()

        valueExp = TestConst.STR_ON
        self._method.return_value = 1

        sut.run(self._context)

        ValueGot = self._context.get_info(self._dest_var)

        self._assert_method_called_and_value_good(sut, self._method, valueExp, ValueGot,
                                                  'VERDICT: %s stored as %s' % (self._dest_var, str(valueExp)))

    def test_get_power_off_ok(self):
        sut = self._create_sut()

        valueExp = TestConst.STR_OFF
        self._method.return_value = 0

        sut.run(self._context)

        ValueGot = self._context.get_info(self._dest_var)

        self._assert_method_called_and_value_good(sut, self._method, valueExp, ValueGot,
                                                  'VERDICT: %s stored as %s' % (self._dest_var, str(valueExp)))

    def test_get_power_off_ko(self):
        sut = self._create_sut()

        valueExp = TestConst.STR_OFF
        self._method.return_value = 1

        sut.run(self._context)

        ValueGot = self._context.get_info(self._dest_var)

        self._assert_method_called_and_value_bad(self._method, valueExp, ValueGot)

    def test_get_power_on_ko(self):
        sut = self._create_sut()

        valueExp = TestConst.STR_ON
        self._method.return_value = 0

        sut.run(self._context)

        ValueGot = self._context.get_info(self._dest_var)

        self._assert_method_called_and_value_bad(self._method, valueExp, ValueGot)

    # pylint: disable=W0212
    def _create_sut(self):
        """
        Create the SUT with only test step pars
        """
        sut = GNSSGetPower(None, None, {"SAVE_AS": self._dest_var}, mock.Mock())
        self._method = sut._api.get_gps_power_status
        return sut
