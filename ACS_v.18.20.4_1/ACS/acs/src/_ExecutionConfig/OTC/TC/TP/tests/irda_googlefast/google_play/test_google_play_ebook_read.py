#Copyright (C) 2014  Yi, GraceX <gracex.yi@intel.com>
#Intel Corporation All Rights Reserved.

#The source code contained or described herein and
#all documents related to the source code ("Material") are owned by
#Intel Corporation or its suppliers or licensors.

#Title to the Material remains with Intel Corporation or
#its suppliers and licensors.
#The Material contains trade secrets and proprietary and
#confidential information of Intel or its suppliers and licensors.
#The Material is protected by worldwide copyright and
#trade secret laws and treaty provisions.
#No part of the Material may be used, copied, reproduced, modified,
#published, uploaded, posted, transmitted, distributed
#or disclosed in any way without Intel's prior express written permission.
#No license under any patent, copyright, trade secret or
#other intellectual property right is granted to
#or conferred upon you by disclosure or delivery of the Materials,
#either expressly, by implication, inducement, estoppel or otherwise.

#Any license under such intellectual property rights must be express
#and approved by Intel in writing.

"""
@summary: Test google play application
@since: 08/21/2014
@author: Grace Yi (gracex.yi@intel.com)
"""
from testlib.google_play.google_play_impl import GooglePlayImpl
from testlib.util.uiatestbase import UIATestBase
import os

class GooglePlayEbookReadTest(UIATestBase):
    """
    @summary: Test google play application
    """
    def setUp(self):
        cfg_file = 'tests.tablet.google_fast.conf'
        super(GooglePlayEbookReadTest, self).setUp()
        self._test_name = __name__
        print "[Setup]: %s" % self._test_name
        self.googleplay = GooglePlayImpl(\
            self.config.read(cfg_file, 'google_play'))
        self.googleplay.set_orientation_n()

    def tearDown(self):
        super(GooglePlayEbookReadTest, self).tearDown()
        print "[Teardown]: %s" % self._test_name


    def testGooglePlayEBookRead(self):
        """
        This test case is to test read a book in google play book list

        Test Case Precondition:
        1. Connect to abroad ap
        2. The Account has been signed in

        Test Case Step:
        1.Launch google play and click free book list
        2.Click read button to read the ebook

        Expect Result:
        1.The book main page can be read

        """
        print "[RunTest]: %s" % self.__str__()

        self.googleplay.google_play_read_book()
        self.googleplay.quit_by_backkey()
