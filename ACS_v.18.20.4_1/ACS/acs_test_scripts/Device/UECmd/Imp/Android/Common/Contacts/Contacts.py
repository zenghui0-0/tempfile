"""
@copyright: (c)Copyright 2014, Intel Corporation All Rights Reserved.
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

@organization: INTEL MCG PSI
@summary: This script is the interface of contacts uecmd.
@since: 14/10/2014
@author: ssavrim
"""

from acs_test_scripts.Device.UECmd.Imp.Android.Common.BaseV2 import BaseV2
from acs_test_scripts.Device.UECmd.Interface.Contacts.IContacts import IContacts


class Contacts(BaseV2, IContacts):

    """
    Abstract class that defines the interface to be implemented
    by device contacts operations handling sub classes.

    All method that shall be redefined in sub-classes raise a
    I{DeviceException} error.
    """

    def __init__(self, device):
        """
        Initializes this instance.

        Nothing to be done in abstract class.

        :type device: DeviceBase
        :param device: The DUT
        """
        BaseV2.__init__(self, device)
        IContacts.__init__(self, device)

        self.__contacts_module = "acscmd.contacts.ContactsModule"

    def contact_operation(self, contact):
        """
        Contact operation with contact number.
        First insert contacts into phone, and then update a contact, search the
        updated contact, delete a contact, delete all contacts. Each step will check
        the contact number is correct or not.

        :type contact: str
        :param contact: The number of contact

        :rtype: list
        :return: operation status & output log
        """
        target_method = "contactOperate"
        cmd_args = "--ei contact {0}".format(contact)
        cmd_timeout = int(contact) * 5
        result = self._internal_exec_v2(self.__contacts_module, target_method, cmd_args, cmd_timeout)

        output_msg = result.get('output')
        return output_msg if output_msg else "No error"

    def contact_insert(self, contact, first_name="", family_name="", home_phone="", mobile_phone="", email=""):
        """
        Create contact with specified info.
        This will insert a contact label and, optionally, first name, family name,
        home phone number, mobile phone number and email.
        If set to "RANDOM", optional info is auto generated

        :type contact: String
        :param contact: The contact's label

        :type first_name: String
        :param first_name: The contact's name

        :type family_name: String
        :param family_name: The contact's family name

        :type home_phone: String
        :param home_phone: The contact's home phone number

        :type mobile_phone: String
        :param mobile_phone: The contact's mobile phone number

        :type email: String
        :param email: The contact's email
        """
        target_method = "contactInsert"
        cmd_args = ("--es contact {0} "
                    "--es first_name {1} "
                    "--es family_name {2} "
                    "--es home_phone {3} "
                    "--es mobile_phone {4} "
                    "--es email {5}".format(contact, first_name, family_name, home_phone, mobile_phone, email))

        self._internal_exec_v2(self.__contacts_module, target_method, cmd_args)

    def contact_display(self, contact):
        """
        Display a contact

        :type contact: String
        :param contact: The contact's name
        """
        target_method = "contactDisplay"
        cmd_args = "--es contact {0}".format(contact)
        self._internal_exec_v2(self.__contacts_module, target_method, cmd_args)

    def contact_delete(self, contact):
        """
        Delete a contact

        :type contact: str
        :param contact: The contact's name
        """
        target_method = "contactDelete"
        cmd_args = "--es contact {0}".format(contact)
        self._internal_exec_v2(self.__contacts_module, target_method, cmd_args)

    def contact_all_delete(self):
        """
        Delete all contact
        """
        target_method = "contactAllDelete"
        self._internal_exec_v2(self.__contacts_module, target_method)

    def check_contact_in_list(self, contact):
        """
        Check if "contact" appears in contact list

        :type contact: String
        :param contact: The contact's name

        :rtype: String
        return: contact_number
        """
        target_method = "checkContactInList"
        cmd_args = "--es contact {0}".format(contact)
        result = self._internal_exec_v2(self.__contacts_module, target_method, cmd_args)
        return result["contactNumber"]
