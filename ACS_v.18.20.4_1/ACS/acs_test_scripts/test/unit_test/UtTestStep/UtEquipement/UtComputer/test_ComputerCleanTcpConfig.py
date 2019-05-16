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
@summary: This file implements the unit test for ComputerCleanTcpConfig
:since: 04/12/2014
:author: jfranchx

"""
import mock
from unit_test.UtTestStep.UTestTestStepBase import UTestTestStepBase
from Core.TestStep.TestStepContext import TestStepContext
from acs_test_scripts.TestStep.Equipment.Computer.ComputerCleanTcpConfig import ComputerCleanTcpConfig


class ComputerCleanTcpConfigTest(UTestTestStepBase):

    def setUp(self):
        UTestTestStepBase.setUp(self)
        self._context = TestStepContext()
        self._sut = None

    def test_connect_call_ok(self):
        self._create_sut()
        self._sut.run(self._context)
        self._sut._computer.clean_tcp_records_computer.assert_called_once_with()

    def _create_sut(self):

        self._sut = ComputerCleanTcpConfig(None, mock.Mock(), {"EQT": "COMPUTER2"}, mock.Mock())
        return self._sut
