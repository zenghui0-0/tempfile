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

@organization: UMG PSI Validation
@summary: This file implements the unit test for Logic Analyzer.

@author: emarchan

"""
import mock
from unit_test.UtTestStep.UTestTestStepBase import UTestTestStepBase
from Core.TestStep.TestStepContext import TestStepContext
from acs_test_scripts.TestStep.Equipment.LogicAnalyzer.LogicAnalyzerSetCaptureRate import LogicAnalyzerSetCaptureRate

DEFAULT_VALUE = "1500"
class Test_LogicAnalyzerSetCaptureRate(UTestTestStepBase):

    def setUp(self):
        UTestTestStepBase.setUp(self)
        self._context = TestStepContext()
        self._sut = None
        self._ping_return = None

    def test_cap_rate_call_ok(self):
        self._create_sut({"CAPTURE_RATE":DEFAULT_VALUE})
        self._sut.run(self._context)
        self._sut._log_an.set_capture_rate.assert_called_once_with(DEFAULT_VALUE)

    def test_cap_rate_call_ko(self):
        self._create_sut({"CAPTURE_RATE":"Dummy"})
        with self.assertRaisesRegexp(AssertionError, "is invalid at this stage"):
            self._sut.run(self._context)

    def _create_sut(self, params=None):
        self._sut = LogicAnalyzerSetCaptureRate(None, mock.Mock(), params, mock.Mock())
        return self._sut
