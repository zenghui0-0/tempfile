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

:organization: INTEL MCG PSI
:summary: This file implements a Test Step to set sim operator information (MCC and MNC) on equipment
:since may 12th 2015
:author: Martin Brisbarre
"""
from Core.TestStep.EquipmentTestStepBase import EquipmentTestStepBase


class SetSimOperatorInfo(EquipmentTestStepBase):
    """
    Returns the MCC and MNC stored in SIM
    """
    def run(self, context):
        """
        Runs the test step

        :type context: TestStepContext
        :param context: test case context
        """
        EquipmentTestStepBase.run(self, context)
        net_sim = self._equipment_manager.get_cellular_network_simulator(self._pars.eqt, visa=True)

        net_sim.get_cell().set_mcc(self._pars.mcc)
        net_sim.get_cell().set_mnc(self._pars.mnc)
