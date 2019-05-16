#! /usr/bin/env python
# coding:utf-8

import os
import sys
import time
from testlib.util.uiatestbase import UIATestBase
from testlib.sensor.sensor_impl import SensorImpl

class jitter_rotation_vector_ui(UIATestBase):
    '''
    calculate the jitter of rotation vector sensor UI delay time
    '''

    def setUp(self):
        self._test_name = __name__
        print "[Setup]: %s" % self._test_name
        configuration = "tests.tablet.sensor.conf"
        self.cfg_file = configuration
        self.sensorImpl = SensorImpl()
        super(jitter_rotation_vector_ui, self).setUp()

    def tearDown(self):
        print "[Teardown]: %s" % self._test_name
        super(jitter_rotation_vector_ui, self).tearDown()

    def test_jitter_rotation_vector_ui(self):

        fileName = os.path.split(os.path.realpath(__file__))[1]
        sensor_type = fileName.split('_')[1].strip() + " vector"

        self.sensorImpl.sensor_log(self.config.read(self.cfg_file, "artifactory"), "UI", sensor_type)
        self.sensorImpl.check_log()

