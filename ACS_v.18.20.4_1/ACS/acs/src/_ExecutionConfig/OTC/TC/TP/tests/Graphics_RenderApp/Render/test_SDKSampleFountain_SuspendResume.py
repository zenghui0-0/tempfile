# -*- coding: utf-8 -*-
'''
@summary: This case will not throw Exception,
need framework support check the crash issue.
@since: 03/26/2015
@author: Yingjun Jin
'''
from testlib.graphics.test_template.render_app_testbase import RenderAppTestBase
from testlib.graphics.render_impl import RenderImpl


class Render(RenderAppTestBase):

    def setUp(self):
        super(Render, self).setUp()
        self._test_name = __name__
        print "[Setup]: %s" % self._test_name
        self._render = RenderImpl()
        self._render.install_apk("RsFountain")

    def tearDown(self):
        print "[Teardown]: %s" % self._test_name
        super(Render, self).tearDown()

    def test_sdksamplefountain_suspendresume(self):
        ''' refer TC test_SDKSampleFountain_SuspendResume
        '''
        print "[RunTest]: %s" % self.__str__()
        self._render.launch_fountain_am()
        self._render.suspend_and_resume()
        self._render.stop_fountain_am()
