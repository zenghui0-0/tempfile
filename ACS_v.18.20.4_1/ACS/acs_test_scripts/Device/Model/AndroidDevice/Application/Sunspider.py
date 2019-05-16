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
:summary: This script implements sunspider benchmark
:since: 16/04/2013
:author: pbluniex
"""
import re
import itertools
from acs_test_scripts.Device.Model.AndroidDevice.Application.IBrowsing import IBrowsing
from ErrorHandling.DeviceException import DeviceException


class Sunspider(IBrowsing):

    """
    Sunspider benchmark implementation
    """

    def __init__(self, device):
        """
        Initializes this instance.

        :type device: Device
        :param device: The DUT
        """
        IBrowsing.__init__(self, device)

        self._sunspider_pattern = "Sunspider result: (?P<result>\{.*\})"
        self._results = {"score": []}

    def wait(self, timeout):
        """
        Wait until the end of benchmark

        :type timeout: integer
        :param timeout: Timeout beyond no message is triggered
        """
        logger = self._get_device_logger()
        result = logger.is_message_received("regex:" + self._sunspider_pattern, timeout)
        if not result:
            self._logger.debug("Timeout while browsing : %s" % str(result))
            raise DeviceException(DeviceException.TIMEOUT_REACHED,
                                  "Timeout while browsing")

        match_res = re.search(self._sunspider_pattern, result[0])
        if match_res:
            raw_result = eval(match_res.group("result"))
            raw_result.pop("v", None)
            score = float(sum(list(itertools.chain(*raw_result.values()))))
            self._results["score"].append(score / (len(raw_result.popitem()[1]) * 1000))
        else:
            raise DeviceException(DeviceException.TIMEOUT_REACHED,
                                  "Can not find score for Sunspider")
