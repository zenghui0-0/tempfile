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
:summary: voice call 3G implementation for Agilent 8960
:since: 01/04/2011
:author: ymorel
"""

import time
import re
from ErrorHandling.TestEquipmentException import TestEquipmentException
from acs_test_scripts.Equipment.NetworkSimulators.Cellular.Interface.IVoiceCall3G import IVoiceCall3G
from acs_test_scripts.Equipment.NetworkSimulators.Cellular.Agilent8960.Wrapper.Tech3G import WVoiceCall3G as W
from ErrorHandling.AcsBaseException import AcsBaseException


class VoiceCall3G(IVoiceCall3G):

    """
    Voice Call 3G implementation for Agilent 8960
    """

    def __init__(self, root):
        """
        Constructor
        :type root: weakref
        :param root: a weak reference on the root class (Agilent8960)
        """
        self.__root = root

    def __error_check(self, err, msg):
        """
        Error checking and warning reporting
        :raise TestEquipmentException: if err < 0
        """
        if err < 0:
            self.get_logger().error(msg)
            raise TestEquipmentException(TestEquipmentException.SPECIFIC_EQT_ERROR, msg)
        elif err > 0:
            self.get_logger().warning(msg)

    def get_root(self):
        """
        Gets the root of the equipment
        :rtype: Agilent8960
        :return: the root of the equipment
        """
        return self.__root

    def get_logger(self):
        """
        Gets the logger
        """
        return self.get_root().get_logger()

    def mt_originate_call(self):
        """
        Originates a mobile terminated call
        """

        self.get_logger().info("MT Originate Call")
        if not self.is_voice_call_idle():
            # End all previous call on Agilent 8960
            self.__root.send_command("CALL:END:AMR")
        time.sleep(1)
        # Establish MT AMR voice call
        self.__root.send_command("CALL:ORIGINATE:AMR")

    def set_audio_codec(self, codec):
        """
        Sets the audio codec to use
        :type codec: str
        :param codec: the audio codec to set. Possible values:
            Full rate AMR NB codecs :
            - "FR_AMR_NB_1220" | "FR_AMR_NB_1020" | "FR_AMR_NB_795"  | "FR_AMR_NB_740"
            - "FR_AMR_NB_670"  | "FR_AMR_NB_590"  | "FR_AMR_NB_515"  | "FR_AMR_NB_475"
            Full rate AMR WB codecs :
            - "AMR_WB_2385" | "AMR_WB_2305" | "AMR_WB_1985" | "AMR_WB_1825"
            - "AMR_WB_1585" | "AMR_WB_1425" | "AMR_WB_1265" | "AMR_WB_885"
            - "AMR_WB_660"
        """
        agilent_codec = None
        # Transform ACS codecs name into the codec name understood by Agilent 8960
        if codec == "FR_AMR_NB_1220":
            agilent_codec = "AMR1220"
        elif codec == "FR_AMR_NB_1020":
            agilent_codec = "AMR1020"
        elif codec == "FR_AMR_NB_795":
            agilent_codec = "AMR795"
        elif codec == "FR_AMR_NB_740":
            agilent_codec = "AMR740"
        elif codec == "FR_AMR_NB_670":
            agilent_codec = "AMR670"
        elif codec == "FR_AMR_NB_590":
            agilent_codec = "AMR590"
        elif codec == "FR_AMR_NB_515":
            agilent_codec = "AMR515"
        elif codec == "FR_AMR_NB_475":
            agilent_codec = "AMR475"
        elif codec == "AMR_WB_2385":
            agilent_codec = "AMR2385"
        elif codec == "AMR_WB_1585":
            agilent_codec = "AMR1585"
        elif codec == "AMR_WB_1265":
            agilent_codec = "AMR1265"
        elif codec == "AMR_WB_885":
            agilent_codec = "AMR885"
        elif codec == "AMR_WB_660":
            agilent_codec = "AMR660"
        else:
            raise TestEquipmentException(
                TestEquipmentException.INVALID_PARAMETER,
                "%s is an Unknown CODEC or is not supported by the equipment" % codec)

        (err, msg) = W.SetAudioCodec(self.get_root(), agilent_codec)
        self.__error_check(err, msg)

    def set_speech_configuration(self, config):
        """
        Sets the speech configuration
        :type config: str
        :param config: the speech configuration to set. Possible values:
            - "ECHO"
            - "SPEECH_OUTPUT"
        """

        if config not in ["SPEECH_OUTPUT", "ECHO"]:
            raise TestEquipmentException(
                TestEquipmentException.INVALID_PARAMETER,
                "Speech configuration must be SPEECH_OUTPUT or ECHO")

        if config == "SPEECH_OUTPUT":
            config = "RTV"
        else:
            config = "ECHO"

        (err, msg) = W.SetSpeechConfiguration(self.get_root(), config)
        self.__error_check(err, msg)

    def set_echo_loopback_delay(self, delay):
        """
        Sets the echo loopback delay
        :type delay: double
        :param config: the speech echo loopback delay to set. A double
        from 0.1 to 4 with a resolution of 0.2 (in seconds).
        """
        (err, msg) = W.SetEchoLoopbackDelay(self.get_root(), delay)
        self.__error_check(err, msg)

    def is_voice_call_idle(self):
        """
        Tests if voice call is idle (disconnected).
        :rtype: boolean
        :return:
            - true if the voice Call status is idle
            - false otherwise
        :raise: raises TestEquipmentException (error code, error message) in case of failure.
        """
        (err, status, msg) = W.GetCallControlStatus(self.get_root())
        self.__error_check(err, msg)
        return status == "IDLE"

    def is_voice_call_connected(self, connection_time=0, blocking=True):
        """
        Tests if the voice call is established between equipment and DUT for
        connection_time seconds. If connection_time is <= 0, only one test
        is performed.
        :type connection_time: integer
        :param connection_time: expected minimum connection time
        :type blocking: boolean
        :param blocking: raise or not an exception
        :rtype: boolean
        :return:
            - true if the voice call is established for connection_time seconds or if
        voice call is connected
            - false otherwise
        :raise: TestEquipmentException (error code, error message) in case of failure.
        """
        self.get_logger().info(
            "Check if voice call connected for %d seconds", connection_time)

        timer = 0
        (err, status, msg) = W.GetCallControlStatus(self.get_root())
        self.__error_check(err, msg)

        while (timer < connection_time) and (status == "CONN"):
            (err, status, msg) = W.GetCallControlStatus(self.get_root())
            self.__error_check(err, msg)
            time.sleep(1)
            timer += 1

        if status != "CONN":  # Fail

            if blocking:
                msg = "Voice call interrupted after %d seconds!" % timer
                self.get_logger().error(msg)
                raise TestEquipmentException(TestEquipmentException.TIMEOUT_REACHED, msg)
            else:
                msg = "Voice call interrupted after %d seconds!" % timer
                self.get_logger().info(msg)
                return False

        self.get_logger().info("Voice call still connected after %d seconds!",
                               connection_time)
        return True

    def check_call_idle(self, timeout=0, blocking=True):
        """
        Checks that call is finished (idle) between equipment test and DUT before
        timeout seconds. If timeout is <= 0, only one test is performed.
        :type timeout: integer
        :param timeout: allowed time in seconds to establish the call
        :raise: raises TestEquipmentException (error code, error message) in case of failure.
        """
        self.check_call_state("IDLE", timeout, blocking=True)

    def check_call_state(self, state, timeout=0, blocking=True):
        """
        Checks that equipment call state is set to the expected sate
        before the given timeout. If timeout is <= 0, only one test is performed.
        :type state: str
        :param state: the expected state. Possible values:
        - "CALL" : Alerting
        - "CONNECTED" : Connected
        - "HAND" : Handoff
        - "IDLE" : Idle
        - "PAG"  : Paging
        - "REG"  : Registering
        - "REL"  : Releasing
        - "SREQ" : Setup Request
        :type timeout: integer
        :param timeout: allowed time in seconds to reach the expected state
        :raise: raises ServiceException (error code, error message) in case of failure.
        """
        self.get_logger().info(
            "Check call state is %s before timeout %d seconds", state, timeout)

        timer = timeout
        (err, current_state, msg) = W.GetCallControlStatus(self.get_root())
        self.__error_check(err, msg)

        while (timer > 0) and (current_state != state):
            time.sleep(1)
            (err, current_state, msg) = W.GetCallControlStatus(self.get_root())
            self.__error_check(err, msg)
            timer -= 1

        if current_state == state:  # Expected state has been reached
            self.get_logger().info("Call state is %s!", state)
        else:
            if blocking:
                # Timeout to reach desired state
                msg = "Check Call state to %s timeout !" % state
                self.get_logger().error(msg)
                raise TestEquipmentException(TestEquipmentException.TIMEOUT_REACHED, msg)
            else:
                # Timeout to reach desired state (Test failed no TestEquipmentException raised)
                self.get_logger().info("Check Call state to %s timeout !", state)

    def check_call_connected(self, timeout=0, blocking=True):
        """
        Checks that call is established between equipment test and DUT before
        timeout seconds. If timeout is <= 0, only one test is performed.
        :type timeout: integer
        :param timeout: allowed time in seconds to establish the call
        :raise: raises TestEquipmentException (error code, error message) in case of failure.
        """
        self.check_call_state("CONN", timeout, blocking=True)

    def include_calling_party_number(self, state):
        """
        Sets whether to include the calling party number information record.
        :type state: str
        :param state: If "on" the calling party number parameters is sent to
            the mobile station. If "no" the calling party number parameters is not
            sent to the mobile station.
        :raise exception: AcsBaseException if the parameter is neither on or
            off.
        """
        self.get_logger().info("Setting inclusion of calling party info to:"
                               " %s" % state)
        # Storing the GPIB command name.
        gpib_command = "CALL:CPNumber:INCLusion"
        # Checking if the input is in expected range.
        if state.upper() == "ON":
            gpib_parameter = "INCL"
            self.get_logger().info("The calling party number parameters will"
                                   " be sent to the DUT")
        elif state.upper() == "OFF":
            gpib_parameter = "EXCL"
            self.get_logger().info("The calling party number parameters won't"
                                   " be sent to the DUT")
        else:
            # Otherwise raise an exception.
            raise AcsBaseException(AcsBaseException.INVALID_PARAMETER,
                                   "Wrong parameter passed to the"
                                   " \"include_calling_party_number\""
                                   " method should be on or off is: %s"
                                   % gpib_parameter)
        self.get_logger().debug("Sending the following GPIB command %s %s"
                                % (gpib_command, gpib_parameter))
        # Sending the GPIB Command to the equipment.
        self.get_root().send_command("%s %s" % (gpib_command, gpib_parameter))

    def set_calling_party_pi(self, state):
        """
        Sets the presentation indicator (PI) used for the calling party number.
        The value is included in the SETUP message to the called mobile station
        when INCLude is selected by CALL:CPNumber:INCLusion
        :type state: str
        :param state: the wanted state for the PI used for the calling party
            number. Should be either ALLOWED, RESTRICTED or NNAVAILABLE.
        :raise AcsBaseException: If the input parameter is not in the expected
            range.
        """
        self.get_logger().info("Setting the calling party presentation"
                               " indicator to: %s" % state)
        # Storing the GPIB command name.
        gpib_command = "CALL:CPNumber:PRESentation"
        # Checking if the input is in the expected range.
        if state.upper() == "ALLOWED":
            gpib_parameter = "ALL"
            self.get_logger().info("The presentation indicator (PI) used for"
                                   " the calling party number is set to:"
                                   " Allowed")
        elif state.upper() == "RESTRICTED":
            gpib_parameter = "REST"
            self.get_logger().info("The presentation indicator (PI) used for"
                                   " the calling party number is set to:"
                                   " Restricted")
        elif state.upper() == "NNAVAILABLE":
            gpib_parameter = "NNAV"
            self.get_logger().info("The presentation indicator (PI) used for"
                                   " the calling party number is set to:"
                                   " Number Non Available.")
        else:
            # Otherwise raise an exception.
            raise AcsBaseException(AcsBaseException.INVALID_PARAMETER,
                                   "Wrong parameter passed to the"
                                   " \"set_calling_party_pi\" method should"
                                   " be ALLOWED, RESTRICTED or NNAVailable"
                                   " is: %s" % gpib_parameter)
        self.get_logger().debug("Sending the following GPIB command %s %s"
                                % (gpib_command, gpib_parameter))
        # Sending the GPIB Command to the equipment.
        self.get_root().send_command("%s %s" % (gpib_command, gpib_parameter))

    def set_calling_party_number(self, number):
        """
        Sets the ASCII representation of the calling party number.
        The value is included in the SETUP message to the called mobile
        station when INCLude is selected by CALL:CPNumber:INCLusion.
        It is displayed on the called mobile station's screen when "ALLowed"
        is selected by CALL:CPNumber:PRESentation[:INDicator].
        :type number: str
        :param number: Range: 0 to 20 characters, each character from the set
        of 0123456789abc*# .
        :raise AcsBaseException: if the number passed as parameter is not in
        the expected range.
        """
        self.get_logger().info("Setting the calling party phone number to:"
                               " %s" % number)
        # Storing the GPIB command name.
        gpib_command = "CALL:CPNumber"
        # Checking if the input is in the expected range.
        regular_exp = re.compile('^[0-9abc*#]{0,20}$')
        if not regular_exp.match(number):
            raise AcsBaseException(AcsBaseException.INVALID_PARAMETER,
                                   "Wrong parameter passed to the"
                                   " \"set_calling_party_number\" method"
                                   " should be 0 to 20 characters, each"
                                   " character from the set of"
                                   " 0123456789abc*# , is: %s" % number)
        self.get_logger().debug("Sending the following GPIB command %s %s"
                                % (gpib_command, number))
        # Sending the GPIB Command to the equipment.
        self.get_root().send_command("%s \'%s\'" % (gpib_command, number))

    def voice_call_network_release(self):
        """
        Releases a voice call.
        """
        (err, msg) = W.VoiceCallNetworkRelease(self.get_root())
        self.__error_check(err, msg)