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
:summary: Use Case LAB MMS Base to perform MO / MT MMS over Network simulator
(for 2G / 3G RAT)
:since: 19/06/2013
:author: lvacheyx
"""
import time
import os
from UtilitiesFWK.Utilities import Global
from acs_test_scripts.UseCase.UseCaseBase import UseCaseBase
from acs_test_scripts.Equipment.EquipmentManager import EquipmentManager as EM
from acs_test_scripts.Utilities.EquipmentUtilities import NetworkSimulatorIP
import acs_test_scripts.Utilities.RegistrationUtilities as RegUtil
from ErrorHandling.DeviceException import DeviceException
from ErrorHandling.AcsConfigException import AcsConfigException
from acs_test_scripts.Device.UECmd.UECmdTypes import MMS_ATTACH_TYPE_LIST
from acs_test_scripts.Utilities.EquipmentUtilities import get_nw_sim_bench_name


class LabMmsBase(UseCaseBase):

    """
    Constructor
    """

    def __init__(self, tc_name, global_config):

        # Call UseCaseBase init function.
        UseCaseBase.__init__(self, tc_name, global_config)

        # init following variable with it's default value:
        self._wanted_reg_state = "registered"

        # Read the configuration from test case
        self._registration_timeout = \
            int(self._dut_config.get("registrationTimeout"))

        # Read MMS APN parameters from BenchConfig.xml to use NowSMS Server
        self._mms_apn = \
            global_config.benchConfig.get_parameters("NOWSMS_SERVER")
        self._apn_ssid = self._mms_apn.get_param_value("SSID")
        self._apn_name = self._mms_apn.get_param_value("APN")
        self._apn_user = self._mms_apn.get_param_value("username")
        self._apn_password = self._mms_apn.get_param_value("password")
        self._apn_ip_address = self._mms_apn.get_param_value("IP")
        self._apn_port = self._mms_apn.get_param_value("APN_PORT")
        self._destination_number = self._mms_apn.get_param_value("MMS_DESTINATION_NUMBER", "")

        # Compose the mmsc value using Now Sms Server URL, APN_PORT, APN_USER, APN_PASSWORD
        self._apn_mmsc = self._apn_ip_address + ":" + self._apn_port + "/" + self._apn_user + "=" + self._apn_password

        # Set apn type to "default,mms" according to UC definition (test of MO / MT MMS)
        self._apn_type = "default,mms"

        # Get NowSMS Server port
        self._nowsms_port = self._mms_apn.get_param_value("PORT")
        # Compose the complete NowSms Server URL with the connection port
        self._nowsms_url = self._apn_ip_address + ":" + self._nowsms_port

        # Get NOWSMS user name
        self._user_name = self._tc_parameters.get_param_value("NOWSMS_USER_NAME")
        # Get NOWSMS user password
        self._user_password = self._tc_parameters.get_param_value("NOWSMS_USER_PASSWORD")

        # Read NS_CELL_TECH from test case xml file
        self._cell_tech = \
            str(self._tc_parameters.get_param_value("CELL_TECH", "3G"))

        # Read CELL_BAND from xml UseCase parameter file
        self._cell_band = self._tc_parameters.get_param_value("CELL_BAND")

        # NS_CELL_REL
        self._ns_cell_rel = 7

        # Read CELL_SERVICE from test case xml file
        self._cell_service = \
            str(self._tc_parameters.get_param_value("CELL_SERVICE"))

        # Read CELL_POWER from xml UseCase parameter file
        self._cell_power = \
            int(self._tc_parameters.get_param_value("CELL_POWER"))

        # Read the DL_ARFCN value from UseCase xml Parameter
        self._arfcn = \
            int(self._tc_parameters.get_param_value("ARFCN"))

        # Read the CELL_LAC value from UseCase xml Parameter
        self._lac = int(self._tc_parameters.get_param_value("LAC"))
        if self._lac is None:
            self._lac = 10

        # Read the CELL_RAC value from UseCase xml Parameter
        self._rac = int(self._tc_parameters.get_param_value("RAC"))
        if self._rac is None:
            self._rac = 20

        # Read the CELL_MCC value from UseCase xml Parameter
        self._mcc = int(self._tc_parameters.get_param_value("MCC"))
        if self._mcc is None:
            self._mcc = 1

        # Read the CELL_MNC value from UseCase xml Parameter
        self._mnc = int(self._tc_parameters.get_param_value("MNC"))
        if self._mnc is None:
            self._mnc = 1

        # Read optional MOVE_OUT_OF_COVERAGE parameter from UseCase xml Parameter
        self._move_out_of_coverage = self._tc_parameters.get_param_value("MOVE_OUT_OF_COVERAGE", 0, int)
        if self._move_out_of_coverage != 1 and self._move_out_of_coverage != 2:
            self._move_out_of_coverage = 0

        # Read optional OUT_OF_COVERAGE_TIMER parameter from UseCase xml Parameter
        self._out_of_coverage_timer = self._tc_parameters.get_param_value("OUT_OF_COVERAGE_TIMER", 0, int)

        # Retrieve valid bench name for capability
        self._bench_name = get_nw_sim_bench_name(self._cell_tech, global_config, self._logger)
        # bench_name should be either NETWORK_SIMULATOR1 or NETWORK_SIMULATOR2
        # In both cases, we need to retrieve the NS number (position in the bench config, either 1 or 2)
        self._ns_number = int(self._bench_name[-1])

        # Read NETWORK_SIMULATOR from BenchConfig.xml
        self._ns_node = \
            global_config.benchConfig.get_parameters(self._bench_name)

        # Create cellular network simulator
        self._em = EM()
        self._ns = self._em.get_cellular_network_simulator(self._bench_name)

        # Retrieve the model of the equipment
        self._ns_model = self._ns_node.get_param_value("Model")

        # Retrieve the model IP addresses
        ns_ips = NetworkSimulatorIP(self._logger)
        ns_ips.setup_config(global_config, self._ns_number)
        (self._ns_ip_lan1, self._ns_ip_lan2, self._ns_dut_ip_address, self._ns_dut_ip_address2, self._ns_dns1,
         self._ns_dns2, self._ns_subnet_mask, self._ns_default_gateway) = ns_ips.get_config()

        # Instantiate UECmd API
        self._modem_api = self._device.get_uecmd("Modem")
        self._phonesystem_api = self._device.get_uecmd("PhoneSystem")
        self._networking_api = self._device.get_uecmd("Networking")
        self._mms_messaging = self._device.get_uecmd("MmsMessaging")

#------------------------------------------------------------------------------
    def set_up(self):
        """
        Setting up the test
        """
        # Call UseCaseBase set_up function.
        UseCaseBase.set_up(self)

        # Ensure flight mode off so that GSM sim operator info can be retrieved
        self._networking_api.set_flight_mode("off")

        time.sleep(self._wait_btwn_cmd)

        # Determinate the kind of registration state to wait
        # by comparing test case MCC/MNC parameters to sim MCC/MNC
        sim_info = self._modem_api.get_sim_operator_info()
        if sim_info["MCC"] != self._mcc or\
                sim_info["MNC"] != self._mnc:
            self._wanted_reg_state = "roaming"
            self._networking_api.set_roaming_mode("ON")
        else:
            self._wanted_reg_state = "registered"

        # Clear all data connections
        self._networking_api.clean_all_data_connections()
        time.sleep(self._wait_btwn_cmd)

        # Enable flight mode
        self._networking_api.set_flight_mode("on")

        # Instantiate Network Simulator APIs and
        # Initialize the Network Simulator
        self.set_ns_apis_instances()

        # Perform full preset
        self._ns.perform_full_preset()

        # Set cell off
        self._ns_cell.set_cell_off()

        # Set the Equipment IP Address 1
        self._ns.set_ip4_lan_address(self._ns_ip_lan1)

        # Set the equipment IP_Lan2 to the equipment
        self._ns.set_ip4_lan_address2(self._ns_ip_lan2)

        # Set the Equipment Subnet mask
        self._ns.set_ip4_subnet_mask(self._ns_subnet_mask)

        # Set the Equipment gateway
        self._ns.set_ip4_default_gateway(self._ns_default_gateway)

        # Set the DUT IP address 1
        self._ns_data.set_dut_ip_address(1, self._ns_dut_ip_address)
        # Set the DUT IP address 2 if not empty str.
        if self._ns_dut_ip_address2 != "":
            self._ns_data.set_dut_ip_address(2, self._ns_dut_ip_address2)

        # Set HTTP Input ON for Nowsms
        # Set HTTP output ON for Nowsms
        self._ns.set_sms_http("ON", "ON")

        # Call specific configuration functions
        RegUtil.setup_cell(self._ns_number,
                           self._ns_model,
                           self._cell_tech,
                           self._cell_band,
                           self._ns_cell_rel,
                           self._logger)

        # Set Cell Band and ARFCN using CELL_BAND
        # and ARFCN parameters
        # Set cell service using CELL_SERVICE parameter
        # Set Cell Power using CELL_POWER parameter
        # Set Cell LAC using LAC parameter
        # Set Cell RAC using RAC parameter
        # Set Cell MCC using MCC parameter
        # Set Cell MNC using MNC parameter
        self._ns_cell.configure_basic_cell_parameters(
            self._cell_service, self._cell_band,
            self._arfcn, self._cell_power,
            self._lac, self._rac, self._mcc, self._mnc)

        # Set cell on
        self._ns_cell.set_cell_on()

        # Disable flight mode
        self._networking_api.set_flight_mode("off")

        # Set the MMS APN in the DUT
        time.sleep(self._wait_btwn_cmd)
        self._logger.info("Setting APN " + str(self._apn_name) + "...")
        self._networking_api.set_apn(self._apn_ssid,
                                     self._apn_name,
                                     self._apn_user,
                                     self._apn_password,
                                     protocol=None,
                                     mmsc=self._apn_mmsc,
                                     apn_type=self._apn_type)

        # Activate PDP context
        time.sleep(self._wait_btwn_cmd)
        self._logger.info("Active PDP Context...")
        self._networking_api.activate_pdp_context(self._apn_ssid, check=False)

        # Check DUT is register
        verdict, output = self._check_network_registration()
        if verdict == Global.FAILURE:
            return verdict, output

        # Set display to "on"
        self._phonesystem_api.display_on()

        return Global.SUCCESS, "No error"

#------------------------------------------------------------------------------
    def tear_down(self):
        """
        Tear down
        """
        # Call UseCaseBase tear_down function.
        UseCaseBase.tear_down(self)

        # deactivate PDP context status
        self._networking_api.deactivate_pdp_context()
        if self._wanted_reg_state == "roaming":
            self._networking_api.set_roaming_mode("OFF")
        time.sleep(self._wait_btwn_cmd)

        return Global.SUCCESS, "No error"

#------------------------------------------------------------------------------
    def set_ns_apis_instances(self):
        """
        Instantiate Network Simulator Apis based on
        NS_CELL_TECH parameter value
        """
        if self._cell_tech == "2G":

            self._ns_cell = self._ns.get_cell_2g()
            self._ns_data = self._ns_cell.get_data()
            self._ns_vc = self._ns_cell.get_voice_call()
            self._ns_messaging = self._ns_cell.get_messaging()

            # Connect to equipment
            self._ns.init()

            # Set the equipment application format depending on 3GSM_CELL_TECH.
            self._ns.switch_app_format("GSM/GPRS")

        elif self._cell_tech == "3G":

            self._ns_cell = self._ns.get_cell_3g()
            self._ns_data = self._ns_cell.get_data()
            self._ns_vc = self._ns_cell.get_voice_call()
            self._ns_messaging = self._ns_cell.get_messaging()

            # Connect to equipment
            self._ns.init()

            # Set the equipment application format depending on 3GSM_CELL_TECH.
            self._ns.switch_app_format("WCDMA")

    def check_mms_attachment(self, mms):
        """
        Checks the presence of the attachment in the DUT's memory
        """
        if mms._attachment_file != "":
            if "MO" in mms._direction:
                # Check that attachment file of the MMS exists (on DUT's sdcard)
                if mms._media.upper() in MMS_ATTACH_TYPE_LIST:
                    # Checks if the attachment file exist.
                    self._phonesystem_api.check_file_exist(mms._attachment_file)
            else:
                # check file exist on local computer (os.path.exists(path))
                if os.path.exists(mms._attachment_file):
                    self._logger.info("File \" %s \" exists !" % str(mms._attachment_file))
                else:
                    raise AcsConfigException(AcsConfigException.FILE_NOT_FOUND,
                                             "The file \"%s\" is missing !" % str(mms._attachment_file))

    def _check_network_registration(self):
        """
        Check DUT state is registered before registration timeout, and check it is register with
        the good RAT.

        :return: Verdict, message
        """
        # Check that DUT is attached on NS => ATTACHED before timeout
        #self._ns_data.check_data_connection_state("ATTACHED", self._registration_timeout, blocking=True)

        # Check that DUT is registered on the good RAT
        self._modem_api.check_network_type_before_timeout(self._ns_data.get_network_type(), self._registration_timeout)

        # Check Data Connection State => PDP_ACTIVE before timeout
        self._ns_data.check_data_connection_state("PDP_ACTIVE", self._registration_timeout, blocking=True)

        # Check registration state is connected using
        # registrationTimeout from Device_Catalog.xml
        self._logger.info("Check network registration status is %s on DUT" % self._wanted_reg_state)
        try:
            if self._wanted_reg_state == "roaming":
                    reg_state= self._modem_api.check_cdk_state_bfor_timeout(self._wanted_reg_state, self._registration_timeout)
                    if "roaming" in reg_state:
                        return Global.SUCCESS, "DUT is register onb Network in roaming state."
                    else:
                        return Global.FAILURE, "DUT is register on Network but in  %s state instead of roaming state." % str(reg_state)
            else:
                self._modem_api.check_cdk_registration_bfor_timeout(self._registration_timeout)
                return Global.SUCCESS, "DUT is register on Network in registered state."
        except DeviceException as exception:
            return Global.FAILURE, str(exception)

#------------------------------------------------------------------------------
    def _go_out_of_coverage(self, timeout=None, cell_limit_power=-115):
        """

        """
        if timeout is None:
            timeout = self._registration_timeout

        # Decrease Cell power to go out of coverage
        self._ns_cell.set_cell_power(cell_limit_power)
        self._logger.info("Going to no coverage zone")

        start_time = time.time()
        while (time.time() - start_time) <= timeout:
            # Wake up screen
            self._phonesystem_api.wake_screen()

            # verify the DUT status is "unregistered"
            status_dut = self._modem_api.get_network_registration_status()
            self._logger.info("Current DUT registration status is: %s", status_dut)
            if "unregistered" in status_dut:
                verdict = Global.SUCCESS
                output = "DUT is unregistered from Network in %d seconds." % (time.time() - start_time)
                self._logger.info(output)
                return verdict, output

            # wait for 1 second
            time.sleep(1)

        # Timeout is reached
        verdict = Global.FAILURE
        output = "DUT is still register on Network after %d seconds." % timeout
        self._logger.error(output)
        return verdict, output
