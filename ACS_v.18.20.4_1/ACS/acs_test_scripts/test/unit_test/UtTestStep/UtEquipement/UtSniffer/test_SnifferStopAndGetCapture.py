# @PydevCodeAnalysisIgnore
# pylint: disable=E0602,W0212,C0103,C0111
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
:summary: Unit test module
:since: 04/08/14
:author: jfranchx
"""

import mock
from unit_test.UtTestStep.UTestTestStepBase import UTestTestStepBase
from acs_test_scripts.TestStep.Equipment.Sniffer.SnifferStopAndGetCapture import SnifferStopAndGetCapture


class SnifferStopAndGetCaptureTest(UTestTestStepBase):
    def setUp(self):
        UTestTestStepBase.setUp(self)
        self._sut = None

    def test_stop_ok(self):
        sut = self._create_sut()
        sut.run(None)
        sut._sniffer.stop_capture.assert_called_with(False)
        sut._sniffer.release.assert_called_with()

    def _create_sut(self, args=None):
        self._sut = SnifferStopAndGetCapture(None, mock.Mock(), args, mock.Mock())
        return self._sut
