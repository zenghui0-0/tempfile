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

:organization: INTEL QCTV
:summary: Error codes for Anritsu M8475A cellular network simulator
:since: 24 March 2015
:author: Martin Brisbarre
"""
AnritsuM8475A_ErrorCodes = {0: "No errors occurred.",
                            2: "The specified file does not exist.",
                            14: "The buffer size is insufficient.",
                            29: "The save destination is a write-protected file.",
                            80: "A file with the same name already exists. (If Overwrite is specified to 0.)",
                            87: "The specified value is wrong.",
                            112: "The disk space is insufficient.",
                            183: "SmartStudio is already running.",
                            1060: "The control software has not been started or has already terminated.",
                            1067: "SmartStudio, control software or SMS Centre could not start due to a problem or problems resulting from OS or the MD8475A system.",
                            1229: "Connecting to the server failed.",
                            1235: "A request is suspended.",
                            1460: "The operation is terminated due to the expiration of the timeout period.",
                            9999: "A GPIB command error occurred.",
                            536870912: "The license could not be confirmed.",
                            536870913: "The specified file cannot be loaded by the SmartStudio.",
                            536870914: "The specified process ID does not exist.",
                            536870915: "The received data does not exist.",
                            536870916: "Simulation is not running.",
                            536870917: "Simulation is running.",
                            536870918: "Test Case has never been executed.",
                            536870919: "The resource cannot be obtained.",
                            536870920: "A resource protocol error, such as download error or license error, occurred.",
                            536870921: "The function call has been in invalid status.",
                            536870922: "The current Simulation Model does not allow the operation.",
                            536870923: "The Cell name to be set does not exist.",
                            536870924: "The test is being executed.",
                            536870925: "The current UE status does not correspond to the test parameters.",
                            536870926: "There is no LOG information because the simulation has not been executed.",
                            536870927: "The Export process is already running.",
                            536870928: "SmartStudio is not connected to the SMS Centre.",
                            536870929: "SmartStudio failed to send an SMS message to the SMS Centre.",
                            536870930: "SmartStudio has successfully sent an SMS message to the SMS Centre, but the SMS Centre judges it as an error.",
                            536870931: "The processing that is unavailable with the current system status has been executed.",
                            536870932: "The option could not be confirmed.",
                            536870933: "The Export process has not yet started.",
                            536870934: "SmartStudio cannot load the specified file because the version is old.",
                            536870935: "The data with the specified PDN number does not exist.",
                            536870936: "The data with the specified Dedicated number does not exist.",
                            536870937: "The PDN data cannot be added because the upper limit of the number of PDN data has been reached.",
                            536870938: "The number of antennas, which cannot be set to the current Simulation Model, has been specified.",
                            536870939: "Calibration of path loss failed.",
                            536870940: "There is a parameter conflict.",
                            536870941: "The DL Ref Power setting is out of the setting range at W-CDMA (Evolution).",
                            536870942: "DC-HSDPA is not available for the current channel setting.",
                            536870943: "The specified Packet Rate cannot be used by the current Simulation Model.",
                            536870944: "The W-CDMA cell parameter F-DPCH is set to Enable.",
                            536870945: "Target is invalid.",
                            536870946: "The PWS/CB Centre detects an error.",
                            536870947: "The Ec/Ior setting is invalid.",
                            536870948: "The combination of Attach Type and TA Update Type is invalid.",
                            536870949: "The license of the option has expired.",
                            536870950: "The Ping command is being executed.",
                            536870951: "The Ping command is not being executed.",
                            536870952: "The current Test Case parameter setting is wrong.",
                            536870953: "The specified IP address is the same as that of Default Gateway specified by Simulation parameter.",
                            536870954: "TFT IE conversion failed.",
                            536870955: "Saving the settings to the scenario failed.",
                            536870956: "The command contains an undefined parameter.",
                            536870957: "The command contains duplicate Cells.",
                            536870958: "The number of Cells has exceeded the upper limit.",
                            536870959: "The Downlink Band setting for the Carrier Aggregation mode is invalid.",
                            536870960: "The current setting does not allow operation in TS09 Mode.",
                            536870961: "The current setting does not allow operation in AWGN Mode.",
                            536870962: "The GPIB function cannot connect to Slave MD8475A(s) that is interlocked with the other MD8475A(s).",
                            536870963: "There is a version conflict between Master and Slave MD8475As that are interlocked. When the Simulation Model is W-CDMA - W-CDMA, the Memory Partitioning cannot be set to Explicit.",
                            536870964: "SmartStudio cannot operate normally since the version of WnsCtrlApi.dll is old.",
                            536875008: "An error exists in the parameter configuration. (This error applies only to the current version.)",
                            536936448: "License verification failed.",
                            536936449: "IMS Services failed to load the specified file.",
                            536936462: "Simulation is not performed and no log information exists.",
                            536936467: "The executed process is inoperable in the current status of Visual User Agent.",
                            536936707: "The specified Virtual Network is not running.",
                            536936709: "The specified Virtual Network is running. Any one of the Virtual Networks is running.",
                            536936727: "The specified Virtual Network does not exist.",
                            536936729: "The Virtual Network already exists.",
                            537001984: "The license cannot be confirmed.",
                            537001985: "WLAN Offload Services failed to load the specified file.",
                            537002003: "The processing that is unavailable with the current Virtual User Agent status has been executed.",
                            537002243: "The specified Virtual Network has not started.",
                            537002245: "The specified Virtual Network has already started.",
                            537001998: "The LOG information does not exist.",
                            537002263: "The specified Virtual Network does not exist.",
                            537002265: "The number of Virtual Networks has reached the upper limit. A new Virtual Network cannot be added.",
                            537002498: "WLAN Offload Services have already started.",
                            554762241: "The RF Measurement launcher cannot be accessed.",
                            554762242: "License verification of RF Measurement failed.",
                            554762243: "Function is called when RF Measurement cannot be set.",
                            554762244: "RF Measurement has been already started.",
                            554762245: "RF Measurement cannot start due to a problem with OS or system of the MD8475A.",
                            554762246: "RF Measurement has not started or has already terminated.",
                            554762247: "There is a version mismatch between RF Measurement and CAL.",
                            554827777: "The specified value for RF Measurement is abnormal.",
                            554827778: "GPIB command error has occurred in RF Measurement.",
                            554827779: "Invalid file path was specified to RF Measurement.",
                            554827780: "RF Measurement argument is NULL pointer.",
                            555810817: "RF Measurement is now performing the measurement.",
                            555810818: "RF Measurement is now not performing the measurement.",
                            555810819: "RF Measurement is not measured yet. (There is no result information since measurement is not performed.)",
                            555810820: "An error has occurred when RF Measurement starts the measurement.",
                            555810821: "Simulation has stopped when RF Measurement is performing the measurement.",
                            555810822: "An error has been retrieved from the Platform when RF Measurement is performing the measurement.",
                            555810823: "Measurement has been started in the system state where RF Measurement is invalid.",
                            556859393: "RF Measurement is now saving a file.",
                            556859394: "There is insufficient disk space when saving a Measure Result file of RF Measurement.",
                            556859395: "An internal error has occurred or USB cable has been disconnected when saving a Measure Result file of RF Measurement.",
                            556859396: "A write-protected file was specified as the save destination when saving a Measure Result file of RF Measurement.",
                            568328193: "An internal error has occurred in RF Measurement.",
                            687865857: "Calibration Measure DSP is now being measured.",
                            687865858: "Calibration measurement failed.",
                            687865859: "Calibration slot is empty or its system does not apply.",
                            687865860: "Unexpected command is received from Calibration HWC.",
                            687865861: "Failed to receive the Calibration measurement result.",
                            687865862: "Failed to open the correction value file on the Calibration HDD.",
                            687865863: "Failed to move the pointer on the Calibration correction value table.",
                            687865864: "Failed to write the correction value to the Calibration correction value file on the Calibration HDD.",
                            687865865: "Failed to load the correction value from the Calibration HDD.",
                            687865866: "Failed to create a directory to which the correction value file on the Calibration HDD is saved.",
                            687865867: "Correction data has not been written in the Calibration-specified correction table.",
                            687865868: "Data received from Calibration HWC does not exist.",
                            687865869: "Data has not been written to the Flash ROM of Calibration BASE UNIT.",
                            687865870: "Correction data has not been written to the Calibration-specified sector.",
                            687866111: "An calibration error other than described above occurred."}
