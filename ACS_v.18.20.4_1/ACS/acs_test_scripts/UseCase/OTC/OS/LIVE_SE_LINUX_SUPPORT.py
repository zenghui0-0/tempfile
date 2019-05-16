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

:organization: INTEL OTC
:summary: SE Linux support
:since: 03/06/2014
:author: aconstan
"""


from acs_test_scripts.UseCase.UseCaseBase import UseCaseBase
from UtilitiesFWK.Utilities import Global

class SELinuxSupport(UseCaseBase):

    def __init__(self, tc_name, global_config):
        # Call UseCaseBase Init function
        UseCaseBase.__init__(self, tc_name, global_config)


    def set_up(self):
        """
        Set up the test configuration

        """
        UseCaseBase.set_up(self)
        return Global.SUCCESS, "No errors"

    def run_test(self):
        """
        Run the test
        """
        passed = True
        error = ""

        # Set the Permissive mode
        res, out = self._device.run_cmd("adb shell setenforce 0", 2)
        res, out = self._device.run_cmd("adb shell getenforce", 2)
        if out != "Permissive":
            passed = False
            error = "Set Permissive not OK."

        # Set the Enforcing mode
        res, out = self._device.run_cmd("adb shell setenforce 1", 2)
        res, out = self._device.run_cmd("adb shell getenforce", 2)
        if out != "Enforcing":
            passed = False
            if error != "":
                error += " Set Enforcing not OK."
        if passed:
            return Global.SUCCESS, "No errors"
        else:
            return Global.FAILURE, error

    def tear_down(self):
        """
        Tear down
        """
        return Global.SUCCESS, "No errors"
