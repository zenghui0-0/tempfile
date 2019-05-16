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
:summary: Use Case GSM SMS Base for SMOKE and BAT tests
:since: 28/09/2010
:author: dgonzalez
"""
from acs_test_scripts.Utilities.CommunicationUtilities import ConfigsParser

import acs_test_scripts.Utilities.RegistrationUtilities as RegUtil
import time

from acs_test_scripts.UseCase.UseCaseBase import UseCaseBase
from UtilitiesFWK.Utilities import Global, str_to_bool
from acs_test_scripts.Equipment.EquipmentManager import EquipmentManager as EM
from acs_test_scripts.Utilities.PhoneOnOffUtilities import PhoneOnOff
from acs_test_scripts.Utilities.EquipmentUtilities import get_nw_sim_bench_name


class LabGsmCamp(UseCaseBase):

    """
    Lab Gsm Camp base class.
    """

    def __init__(self, tc_name, global_config):
        """
        Constructor
        """

        # Call UseCase base Init function
        UseCaseBase.__init__(self, tc_name, global_config)

        # Read mode from test case xml file (str)
        self._switch_mode = self._tc_parameters.get_param_value("SWITCH_MODE", "softshutdown")

        # Read registrationTimeout from Device_Catalog.xml
        self._registration_timeout = \
            int(self._dut_config.get("registrationTimeout"))

        # Read CELLULAR_NETWORK parameters from BenchConfig.xml
        self._network = \
            global_config.benchConfig.get_parameters("CELLULAR_NETWORK")
        self._apn = self._network.get_param_value("APN")
        self._ssid = self._network.get_param_value("SSID")

        # Retrieve valid bench name for 2G capability
        self._bench_name = get_nw_sim_bench_name("2G", global_config, self._logger)

        # Read NETWORK_SIMULATOR from BenchConfig.xml
        self._ns_node = \
            global_config.benchConfig.get_parameters(self._bench_name)

        # Read Band from test case xml file (str)
        self._band = self._tc_parameters.get_param_value("CELL_BAND")

        # Read BCH_ARFCN from test case xml file
        self._bch_arfcn = int(self._tc_parameters.get_param_value("BCH_ARFCN"))

        # Read CELL_SERVICE from test case xml file
        self._cell_service = \
            str(self._tc_parameters.get_param_value("CELL_SERVICE"))

        # Read CELL_POWER from test case xml file
        self._cell_power = \
            int(self._tc_parameters.get_param_value("CELL_POWER"))

        # Read Mobile Country Code (MCC) from test case xml file
        self._mcc = \
            int(self._tc_parameters.get_param_value("MCC"))

        # Read Mobile Network Code (MNC) from test case xml file
        self._mnc = \
            int(self._tc_parameters.get_param_value("MNC"))

        # Read PDP Activation from test case xml file
        self._pdp_activation = str_to_bool(self._tc_parameters.get_param_value("PDP_ACTIVATION"))

        # Instantiate the network simulator
        eqt_man = EM()
        self._ns = eqt_man.get_cellular_network_simulator(self._bench_name)
        self._ns_cell_2g = self._ns.get_cell_2g()
        self._ns_data_2g = self._ns_cell_2g.get_data()

        # Instantiate generic UECmd for camp
        self._modem_api = self._device.get_uecmd("Modem")

        # Instantiate generic UECmd for camp
        self._networking_api = self._device.get_uecmd("Networking")

        # retrieve SIM card UE commands
        self.sim_card_api = self._device.get_uecmd("SimCard")
        self._sim_states = self.sim_card_api.POSSIBLE_SIM_STATES

        # Instantiate Phone On/OFF utilities
        self.phoneonoff_util = PhoneOnOff(self._networking_api, self._device, self._logger)

        # init wanted registration parameters to a value that
        # will make the uecmd that used it to raise an error
        self._wanted_reg_state = "None"

#------------------------------------------------------------------------------
    def set_up(self):
        """
        Set up the test configuration
        """
        # Call UseCase base Setup function
        UseCaseBase.set_up(self)

        # Ensure flight mode off so that GSM sim operator info can be retrieved
        self._networking_api.set_flight_mode("off")
        time.sleep(self._wait_btwn_cmd)

        # Determinates the kind of registration state to wait
        # by comparing test case MCC/MNC parameters to sim MCC/MNC
        sim_info = self._modem_api.get_sim_operator_info()
        if sim_info["MCC"] != self._mcc or\
                sim_info["MNC"] != self._mnc:
            self._wanted_reg_state = "roaming"
        else:
            self._wanted_reg_state = "registered"

        # Clear all data connections
        self._networking_api.clean_all_data_connections()
        time.sleep(self._wait_btwn_cmd)

        if self._switch_mode == "airplane":
            # Switch off according to the mode chosen
            self.phoneonoff_util.switch_off(self._switch_mode)

        # Connect to equipment using GPIBAddress and GPIBBoardId
        self._ns.init()

        # Set the equipment application format GSM/GPRS
        self._ns.switch_app_format("GSM/GPRS")

        # Perform a full preset
        self._ns.perform_full_preset()

        # Set cell off
        self._ns_cell_2g.set_cell_off()

        # Pas indispensable pour tester le nouveau design
        # Set Frequency points using frequency list
        # Set Amplitude Offset correction using offset list
        # Turning amplitude offset state to ON
        self._ns.configure_amplitude_offset_table()

        # Set Cell Band  using CELL_BAND parameter
        self._ns_cell_2g.set_band(self._band)

        # Set Broadcast Channel Arfcn using BCH_ARFCN parameter
        self._ns_cell_2g.set_bcch_arfcn(self._bch_arfcn)

        # Set cell service using CELL_SERVICE parameter
        self._ns_cell_2g.set_cell_service(self._cell_service)

        # Set Cell Power using CELL_POWER parameter
        self._ns_cell_2g.set_cell_power(self._cell_power)

        # Set Mobile Country Code (MCC)
        self._ns_cell_2g.set_mcc(self._mcc)

        # Set Mobile Network Code (MNC)
        self._ns_cell_2g.set_mnc(self._mnc)

        # Check phone is not registered
        self._modem_api.check_cdk_no_registration_bfor_timeout(self._registration_timeout)

        # Set cell on
        self._ns_cell_2g.set_cell_on()

        return Global.SUCCESS, "No errors"

#------------------------------------------------------------------------------
    def run_test(self):
        """
        Execute the test
        """
        # Call UseCase base run_test function
        UseCaseBase.run_test(self)

        if self._switch_mode == "airplane":
            # Switch on according to the mode chosen
            self.phoneonoff_util.switch_on(self._switch_mode)

        elif self._switch_mode in ("hardshutdown", "softshutdown"):
            # Reboot according to the mode chosen
            self.phoneonoff_util.reboot(self._switch_mode)
        else:
            self._logger.info("No actions required to do a switch On/Off")

        # save initial time
        init_time = time.time()

        # Check registration state is connected using
        # registrationTimeout from Device_Catalog.xml
        self._logger.info("Check network registration status is %s on DUT" %
                          self._wanted_reg_state)
        self._modem_api.check_cdk_state_bfor_timeout(
            self._wanted_reg_state,
            self._registration_timeout)

        # time needed to reach registered state
        reg_time = time.time() - init_time
        self._logger.info("DUT registered in less than %3.2f seconds!", reg_time)

        # Adapt attachment procedure to CIRCUIT or PACKET
        if self._cell_service != "GSM":
            if self._pdp_activation:
                # Set the APN
                time.sleep(self._wait_btwn_cmd)
                self._logger.info("Setting APN " + str(self._apn) + "...")
                self._networking_api.set_apn(self._ssid, self._apn)
                # Activate PDP context
                time.sleep(self._wait_btwn_cmd)
                self._logger.info("Active PDP Context...")
                self._networking_api.activate_pdp_context(self._ssid, check=False)

                # Check Data Connection State => PDP_ACTIVE before timeout
                RegUtil.check_dut_data_connection_state_before_timeout("PDP_ACTIVE",
                                                                       self._ns_cell_2g,
                                                                       self._networking_api,
                                                                       self._logger,
                                                                       self._registration_timeout,
                                                                       flightmode_cycle=False,
                                                                       blocking=False)

            else:
                # Check Data Connection State => ATTACHED before timeout
                RegUtil.check_dut_data_connection_state_before_timeout("ATTACHED",
                                                                       self._ns_cell_2g,
                                                                       self._networking_api,
                                                                       self._logger,
                                                                       self._registration_timeout,
                                                                       flightmode_cycle=False,
                                                                       blocking=False)

                # time needed to reach attach state after registration
                attach_time = time.time() - init_time
                self._logger.info("DUT attached in less than %3.2f seconds!", attach_time)

        # Get RAT from Equipment
        network_type = self._ns_data_2g.get_network_type()

        # Check that DUT is registered on the good RAT
        self._modem_api.check_network_type_before_timeout(network_type,
                                                          self._registration_timeout)

        if self._switch_mode == "airplane":
            # Switch off according to the switch mode chosen
            self.phoneonoff_util.switch_off(self._switch_mode)
            # Check that DUT is no longer camped on Network
            self._modem_api.check_cdk_no_registration_bfor_timeout(self._registration_timeout)

        return Global.SUCCESS, "No errors"

#------------------------------------------------------------------------------
    def tear_down(self):
        """
        End and dispose the test
        """

        # Call UseCase base tear_down function
        UseCaseBase.tear_down(self)

        # Set cell off
        self._ns_cell_2g.set_cell_off()

        # DisConnect from equipment
        self._ns.release()

        if self._switch_mode == "airplane":
            # Switch on according to the switch mode chosen
            self.phoneonoff_util.switch_on(self._switch_mode)

        return Global.SUCCESS, "No errors"
