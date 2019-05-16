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
:summary: This file implements Vibrator UECmds
:since: 28/01/2014
:author: mmorchex
"""
from ErrorHandling.DeviceException import DeviceException


class IVibrator():
    """
    Abstract class that defines the interface to be implemented
    by system vibrator handling sub classes.

    All method that shall be redefined in sub-classes raise a
    I{DeviceException} error.
    """

    def __init__(self, device):
        """
        Initializes this instance.
        Nothing to be done in abstract class.
        """
        pass

    def start_vibrator_for_duration(self, duration):
        # This is a default implementation.
        """
        Start vibrator for a given duration
        :type duration: int
        :param duration: duration of the vibration in milliseconds
        :rtype: None
        :return: None
        :raise: DeviceException
        """
        raise DeviceException(DeviceException.FEATURE_NOT_IMPLEMENTED)

    def start_vibrator(self):
        # This is a default implementation.
        """
        Start vibrator without a timeout
        :rtype: None
        :return: None
        :raise: DeviceException
        """
        raise DeviceException(DeviceException.FEATURE_NOT_IMPLEMENTED)

    def stop_vibrator(self):
        # This is a default implementation.
        """
        Stop the vibrator
        :rtype: None
        :return: None
        :raise: DeviceException
        """
        raise DeviceException(DeviceException.FEATURE_NOT_IMPLEMENTED)