"""

:copyright: (c)Copyright 2015, Intel Corporation All Rights Reserved.
The source code contained or described herein and all documents related
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

:organization: INTEL OTC ANDROID QA

:since: 2/3/15
:author: mmaraci
"""
import Queue
import time

from ErrorHandling.AcsConfigException import AcsConfigException
from acs_test_scripts.UseCase.LocalConnectivity.LIVE_DUAL_PHONE_BT_BASE import LiveDualPhoneBTBase
from UtilitiesFWK.Utilities import Global
from acs_test_scripts.Utilities.BluetoothConnectivity import BluetoothConnectivity
from acs_test_scripts.Utilities.LocalConnectivityUtilities import ThreadOPPTransferFile
from acs_test_scripts.Device.UECmd.UECmdTypes import BtProfile
from acs_test_scripts.Utilities.ThreadBrowseWifiChrome import ThreadBrowseWifiChrome


class BluetoothPanNapOpp(LiveDualPhoneBTBase):
    """
    Bluetooth PAN Usecase class
    """
    _SLEEP_TIME_SECS = 1
    _DEFAULT_TIMEOUT_SECS = 5

    def __init__(self, tc_name, global_config):
        """
        Constructor
        """
        LiveDualPhoneBTBase.__init__(self, tc_name, global_config)

        #Get TC parameters
        #wifi activity is set to WIFI_WEB_BROWSING for all PAN/NAP/PANU tests
        self._wifi_activity = str(self._tc_parameters.get_param_value("WIFI_ACTIVITY")).upper()
        if self._wifi_activity == "WIFI_WEB_BROWSING":
            self._wifi_url = str(self._tc_parameters.get_param_value("URL_TO_BROWSE"))
        self._thread_wifi_activity = None

        self._wifi_access_point = str(self._tc_parameters.get_param_value("WIFI_ACCESS_POINT", ""))

        # Read DUT_STATE from test case xml file: server or client
        self._dut_state = str(self._tc_parameters.get_param_value("DUT_STATE")).upper()
        # Read OPP_LOCAL_FILE from test case xml file
        self._opp_local_file = str(self._tc_parameters.get_param_value("OPP_LOCAL_FILE"))

        self._nap_or_pan_test = str(self._tc_parameters.get_param_value("NAP_OR_PAN_TEST")).upper()
        self._connection_to_share = str(self._tc_parameters.get_param_value("CONNECTION_TO_SHARE")).upper()
        self._pairing_initiator = str(self._tc_parameters.get_param_value("PAIRING_INITIATOR")).upper()
        self._bt_tethering_deactivation_test = \
            str(self._tc_parameters.get_param_value("ENABLE_BT_TETHERING_DEACTIVATION_TEST", default_value=False))
        self._who_disconnect = str(self._tc_parameters.get_param_value("WHO_DISCONNECT", default_value="NAP")).upper()
        self._fail_if = self._tc_parameters.get_param_value("PAIRING_CHECK_FAIL_IF", default_value="disconnected")

        self._interleave_search = self._tc_parameters.get_param_value("IS_INTERLEAVE_SEARCH", default_value=False)

        self._browse_retries = 2

        # Initialize data
        self._thread_opp_transfer = None
        self._thread_scan_bt = None
        self._thread_scan_wifi = None
        self._thread_connect_to_nap = None

        self._nap_api = None
        self._panu_api = None
        self._nap_addr = None
        self._panu_addr = None
        self._wifi_api = None
        self._panu_net_api = None
        self._paired_api = None
        self._pair_requester_api = None

        self._queue = Queue.Queue()
        self.__global_config = global_config
        self._wait_btwn_cmd = 5.0
        self._duration = 60
        self._replyval = True
        self._accept_connection = True
        self._must_find = True
        self._status = None
        self._sleep_time = self._SLEEP_TIME_SECS
        self._start_time = None
        self._timeout = self._DEFAULT_TIMEOUT_SECS

        self._bluetooth_connectivity_obj = BluetoothConnectivity(self._device, self._wait_btwn_cmd)


    def set_up(self):
        """
        Initialize the test
        """

        LiveDualPhoneBTBase.set_up(self)

        if self._dut_state not in ["DUT_CLIENT", "DUT_SERVER"]:
            msg = "DUT state configuration unknown - DUT should be client or server"
            self._logger.error(msg)
            raise AcsConfigException(AcsConfigException.INVALID_PARAMETER, msg)

        # defines NAP / PAN-User roles
        if self._nap_or_pan_test == "NAP":
            self._nap_api = self._bt_api
            self._nap_addr = self._phone1_addr
            self._panu_api = self._bt_api2
            self._panu_addr = self._phone2_addr
            self._wifi_api = self._networking_api
            self._panu_net_api = self._networking_api2
        elif self._nap_or_pan_test == "PAN":
            self._nap_api = self._bt_api2
            self._nap_addr = self._phone2_addr
            self._panu_api = self._bt_api
            self._panu_addr = self._phone1_addr
            self._wifi_api = self._networking_api2
            self._panu_net_api = self._networking_api
        else:
            raise AcsConfigException(AcsConfigException.INVALID_TEST_CASE_FILE, "You did not provide a valid value for the NAP_OR_PAN_TEST parameter. It must pe NAP or PAN.")

        # Handle External connection (WIFI or CELLULAR)
        self._bluetooth_connectivity_obj.handle_external_connection(self._connection_to_share, self._wifi_api, self.__global_config, self._wifi_access_point)
        time.sleep(self._wait_btwn_cmd)

        #initialize phone for PAN
        if self._interleave_search is False:
            self._bluetooth_connectivity_obj.search_for_device_until_found(self._panu_api, self._nap_api, self._nap_addr, self._must_find)
        elif self._interleave_search is True:
            self._bluetooth_connectivity_obj.search_for_device_interleave(self._panu_api, self._nap_api, self._nap_addr, self._must_find)

        # Pair the DUT with the device
        self._bluetooth_connectivity_obj.try_until_paired(self._panu_api, self._nap_api, self._panu_addr, self._nap_addr, self._replyval, self._accept_connection)
        # # 4) Set tethering power to on, PAN connect
        # PAN connect the devices
        # Enable BT tethering
        #check devices are truly paired
        self._bluetooth_connectivity_obj.check_paired(self._panu_api, self._nap_addr)
        self._nap_api.set_bt_tethering_power("on")
        time.sleep(self._wait_btwn_cmd)
        #connect PAN way
        self._panu_api.connect_bt_device(self._nap_addr, BtProfile.PAN)
        #check profiles are connected
        keep_going = True
        self._start_time = time.time()
        while keep_going:
            self._status = self._panu_api.get_bt_connection_state(self._nap_addr, BtProfile.PAN)
            keep_going = self._bluetooth_connectivity_obj._keep_going(self._status, self._start_time, self._timeout)
        self._bluetooth_connectivity_obj._raise_error_if_fail_when_profiles_not_connected(self._status, self._fail_if)

        result, output = Global.SUCCESS, ""
        return result, output

    def run_test(self):
        """
        As of right now, at the beginning of the RUN part, we have connected the 2 phones in
        a PAN-NAP way and we are also connected to the internet.
        """
        LiveDualPhoneBTBase.run_test(self)

         # Configure Wifi Browse threads
        if self._wifi_activity == "WIFI_WEB_BROWSING":
            self._thread_wifi_activity = ThreadBrowseWifiChrome(self._queue, self._panu_net_api, self._duration, self._browse_retries, self._wifi_url)
        else:
            msg = "Unknown WIFI_ACTIVITY : %s" % self._wifi_activity
            self._logger.error(msg)
            raise AcsConfigException(AcsConfigException.INVALID_PARAMETER, msg)

        # Configure BT OPP Transfer
        if self._dut_state == "DUT_SERVER":
            self._thread_opp_transfer = ThreadOPPTransferFile(self._queue, self._device, self._phone2,
                                                              self._opp_local_file, self._device.multimedia_path, initialize=True)
        elif self._dut_state == "DUT_CLIENT":
            self._thread_opp_transfer = ThreadOPPTransferFile(self._queue, self._phone2, self._device,
                                                              self._opp_local_file, self._phone2.multimedia_path)

        self._thread_opp_transfer.start()
        time.sleep(20)
        self._thread_wifi_activity.start()
        time.sleep(self._wait_btwn_cmd)
        self._thread_opp_transfer.join()
        # This function waits all threads are dead or timeout is over before finish
        self._exception_reader(self._queue, [self._thread_wifi_activity, self._thread_opp_transfer])

        result, output = Global.SUCCESS, ""
        return result, output

    def tear_down(self):

        #disconnect tethering
        self._bluetooth_connectivity_obj.disconnect_bt_tethering_and_pan(self._bt_tethering_deactivation_test, self._nap_api, self._who_disconnect, self._panu_api, self._nap_addr, self._panu_addr)
        # Bluetooth unpairing
        self._logger.info("Unpair both devices")
        paired = False
        list_paired_devices = self._panu_api.list_paired_device()
        for element in list_paired_devices:
            if str(element.address).upper() == str(self._phone2_addr).upper():
                paired = True
        if paired:
            self._bt_api.unpair_bt_device(self._phone2_addr)
            self._bt_api2.unpair_bt_device(self._phone1_addr)
        else:
            pass
        # Disconnect and clear WiFi networks
        if self._connection_to_share == "WIFI":
            self._wifi_api.wifi_remove_config("all")
            self._wifi_api.set_wifi_power("off")

        LiveDualPhoneBTBase.tear_down(self)

        result, output = Global.SUCCESS, ""
        return result, output