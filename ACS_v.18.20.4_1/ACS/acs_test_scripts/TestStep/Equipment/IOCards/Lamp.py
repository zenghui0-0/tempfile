"""
:copyright: (c)Copyright 2015, Intel Corporation All Rights Reserved.
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

:organization: INTEL OTC
:summary: This file implements a Test Step to turn on and off a lamp using io card
:since: 2015-11-27
:author: hsolver
"""
from Core.TestStep.EquipmentTestStepBase import EquipmentTestStepBase
from ErrorHandling.TestEquipmentException import TestEquipmentException


class On(EquipmentTestStepBase):
    """
    Turns on the lamp
    """

    def run(self, context):
        """
        Runs the test step

        :type context: TestStepContext
        :param context: test case context
        """
        EquipmentTestStepBase.run(self, context)
        io_card = self._equipment_manager.get_io_card(self._pars.eqt)
        if not io_card.lamp(True):
            raise TestEquipmentException(TestEquipmentException.OPERATION_FAILED,
                                         "Fail to turn on the light using {0}".format(self._pars.eqt))


class Off(EquipmentTestStepBase):
    """
    Turns off the light
    """

    def run(self, context):
        """
        Runs the test step

        :type context: TestStepContext
        :param context: test case context
        """
        EquipmentTestStepBase.run(self, context)
        io_card = self._equipment_manager.get_io_card(self._pars.eqt)
        if not io_card.lamp(False):
            raise TestEquipmentException(TestEquipmentException.OPERATION_FAILED,
                                         "Fail to turn off the light {0}".format(self._pars.eqt))