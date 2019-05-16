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

property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be express
and approved by Intel in writing.

:organization: INTEL MCG PSI
:summary: This file implements the AudioComms CSV call (Check volume
quality).
:since: 10/09/2013
:author: nprecigx
"""

import time
from UtilitiesFWK.Utilities import Global
from ErrorHandling.AcsConfigException import AcsConfigException
from acs_test_scripts.UseCase.Audio.LAB_AUDIO_QUALITY_BASE import LabAudioQualityBase
from ErrorHandling.AcsBaseException import AcsBaseException

# pylint: disable=E1101


class LabAudioVolumeCSV(LabAudioQualityBase):

    """
    AudioComms Audio CSV Call class.
    """

    def __init__(self, tc_name, global_config):
        """
        Constructor
        """

        # Call LabAudioQualityBase Init function
        LabAudioQualityBase.__init__(self, tc_name, global_config)

        # Instantiate generic UECmd for voiceCall Ucs
        self._voice_call_api = self._device.get_uecmd("VoiceCall")
        self._phonesystem_api = self._device.get_uecmd("PhoneSystem")
        self._keyevent_api = self._device.get_uecmd("KeyEvent")
        self._networking_api = self._device.get_uecmd("Networking")

        self._voice_call_api2 = None

        # Instantiate the instances for phone caller, receiver and releaser
        self._phone_calling = None
        self._phone_receiving = None
        self._phone_releasing = None
        # Initialization of phone_number to call
        self._calling_phone_number = None
        self._delta_volume = 0

    def __compute_test_verdict__(self, audio_analyzer_result):
        """
        Compute the result verdict and the verdict comment

        :type audio_analyzer_result: int
        :param audio_analyzer_result: the Audio Analyzer return code return by run command
        """

        if audio_analyzer_result == 0:
            self._result_verdict = Global.SUCCESS
            self._verdict_comment = ("Audio Volume test success: with "
                                     "a %s call and %s accessories and %s db"
                                     % (self._call_type,
                                        self._acc_type,
                                        self._delta_volume))
        elif audio_analyzer_result == 1:
            self._result_verdict = Global.FAILURE
            self._verdict_comment = ("Audio Volume test fail: with "
                                     "a %s call and %s accessories and %s db"
                                     % (self._call_type,
                                        self._acc_type,
                                        self._delta_volume))
        elif audio_analyzer_result == 3:
            self._result_verdict = Global.BLOCKED
            self._verdict_comment = "Audio Volume test fail: Audio Analyzer executable exception occurred"
        else:
            self._result_verdict = Global.BLOCKED
            self._verdict_comment = ("Audio Volume test fail: Audio Analyzer problems detected "
                                     "with a %s call and %s accessories"
                                     % (self._call_type,
                                        self._acc_type))

    def set_up(self):
        """
        Set up the test configuration
        """
        # Call LabAudioQualityBase Init function
        LabAudioQualityBase.set_up(self)

        if self._phone2 is not None:
            self._voice_call_api2 = self._phone2.get_uecmd("VoiceCall")
        else:
            error_msg = \
                "This test case requires two phones to be executed !"
            self._logger.error(error_msg)
            raise AcsConfigException(AcsConfigException.INVALID_BENCH_CONFIG, error_msg)

        # Setup phone type ( calling, receiving, releasing phone)
        if self._call_origin_type == "MO":
            self._phone_calling = self._voice_call_api
            self._phone_receiving = self._voice_call_api2
            self._calling_phone_number = self._phone2.get_phone_number()
        elif self._call_origin_type == "MT":
            self._phone_calling = self._voice_call_api2
            self._phone_receiving = self._voice_call_api
            self._calling_phone_number = self._device.get_phone_number()
        else:
            error_msg = \
                "This test case requires call originated type to be executed !"
            self._logger.error(error_msg)
            raise AcsConfigException(AcsConfigException.INVALID_PARAMETER, error_msg)

        if self._call_end_type == "NR":
            self._phone_releasing = self._voice_call_api2
        elif self._call_end_type == "MR":
            self._phone_releasing = self._voice_call_api
        else:
            error_msg = \
                "This test case requires call end type to be executed !"
            self._logger.error(error_msg)
            raise AcsConfigException(AcsConfigException.INVALID_PARAMETER, error_msg)

        # Release any previous call (Robustness)
        self._voice_call_api.release()
        self._voice_call_api2.release()

        if self._acc_type == "HEADSET":
            if self._use_io_card:
                self._wired_headset.unplug_headphone()
                self._wired_headset.plug_whs()
        elif self._acc_type == "HEADPHONE":
            if self._use_io_card:
                self._wired_headset.unplug_whs()
                self._wired_headset.plug_headphone()

        # Dial using PHONE_NUMBER parameter
        self._phone_calling.dial(self._calling_phone_number)
        time.sleep(self._wait_btwn_cmd)

        # Wait for state "active" before callSetupTimeout seconds
        self._phone_receiving.wait_for_state(
            self._uecmd_types.VOICE_CALL_STATE.INCOMING,
            self._call_setup_time)

        # Answer call
        self._phone_receiving.answer()

        # Phone1 & 2 : Check voice call is active
        self._phone_calling.wait_for_state(
            self._uecmd_types.VOICE_CALL_STATE.ACTIVE,
            self._call_setup_time)
        self._phone_receiving.wait_for_state(
            self._uecmd_types.VOICE_CALL_STATE.ACTIVE,
            self._call_setup_time)

        # Configure Audio output to acc_type given with the test_case
        if self._acc_type == "EARPIECE":
            if self._use_io_card:
                self._wired_headset.unplug_whs()
                self._wired_headset.unplug_headphone()
        elif self._acc_type == "SPEAKER":
            # Switch to Speaker, nothing to do in Earpiece
            # Bluetooth already done with connect Bluetooth function above
            self._phonesystem_api.switch_audio_output(self._acc_type.lower())
            time.sleep(self._wait_btwn_cmd)

        self._system_api2.adjust_specified_stream_volume("VoiceCall",
                                                         self._call_stream_volume_ref)

        return Global.SUCCESS, "No errors"

    def run_test(self):
        """
        Execute the test
        """
        # Call LabAudioQualityBase run_test function
        LabAudioQualityBase.run_test(self)

        # WAIT FOR CALL DURATION
        self._logger.info(
            "Wait for call duration: %s s..." % str(self._call_duration))

        # Set Voice Call Volume 0%
        self._system_api.adjust_specified_stream_volume("VoiceCall", 0)
        # Launch audio_quality test
        audio_analyzer_result, l_volume_zero_percent = self._audio_analyzer.get_volume(self._call_type, self._acc_type)
        self._logger.info(
            "Volume at 0 percent: %s " % str(l_volume_zero_percent))

        # Set Voice Call Volume 100%
        self._system_api.adjust_specified_stream_volume("VoiceCall", 100)
        # Launch audio_quality test
        audio_analyzer_result2, l_volume_hundred_percent = self._audio_analyzer.get_volume(self._call_type, self._acc_type)
        self._logger.info(
            "Volume at 100 percent: %s " % str(l_volume_hundred_percent))

        self._keyevent_api.scenario(["POWER_BUTTON"])
        # Set Voice Call Volume 0%
        self._system_api.adjust_specified_stream_volume("VoiceCall", 0)
        # Launch audio_quality test
        audio_analyzer_result3, l_volume_zero_percent2 = self._audio_analyzer.get_volume(self._call_type, self._acc_type)
        self._logger.info(
            "Volume at 0 percent after press power down button: %s "
            % str(l_volume_zero_percent2))

        if audio_analyzer_result == 0 and audio_analyzer_result2 == 0 and audio_analyzer_result3 == 0:
            l_delta1 = int(l_volume_hundred_percent) - int(l_volume_zero_percent)
            l_delta2 = int(l_volume_hundred_percent) - int(l_volume_zero_percent2)
            self._delta_volume = abs(l_delta1 - l_delta2)

            if self._delta_volume < 10:
                self._result_verdict = 0
            else:
                self._result_verdict = 1
        else:
            self._result_verdict = 3
        # Compute test verdict and comment verdict
        self.__compute_test_verdict__(self._result_verdict)

        return self._result_verdict, self._verdict_comment

    def tear_down(self):
        """
        End and dispose the test
        """
        try:
            # RELEASE THE CALL
            # Phone1 & 2 : Check call is still active
            self._phone_calling.check_state(
                self._uecmd_types.VOICE_CALL_STATE.ACTIVE)
            self._phone_receiving.check_state(
                self._uecmd_types.VOICE_CALL_STATE.ACTIVE)

            # Hang up call
            self._phone_releasing.release()

            # Phone1 & 2 : Check call is idle
            self._phone_calling.wait_for_state(
                self._uecmd_types.VOICE_CALL_STATE.NOCALL,
                self._call_setup_time)
            self._phone_receiving.wait_for_state(
                self._uecmd_types.VOICE_CALL_STATE.NOCALL,
                self._call_setup_time)

        except AcsBaseException as acs_exception:
            self._logger.warning("Call release fail:" + str(acs_exception))

        # Call LabAudioQualityBase tear_down function
        LabAudioQualityBase.tear_down(self)

        if self._acc_type == "HEADSET":
            if self._use_io_card:
                self._wired_headset.unplug_whs()
        elif self._acc_type == "HEADPHONE":
            if self._use_io_card:
                self._wired_headset.unplug_headphone()

        # Release any previous call (Robustness)
        if self._voice_call_api is not None:
            self._voice_call_api.release()
        if self._voice_call_api2 is not None:
            self._voice_call_api2.release()

        return Global.SUCCESS, "No errors"
