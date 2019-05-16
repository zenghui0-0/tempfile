# -*- coding: utf-8 -*-
'''
@summary: This case will not throw Exception,
need framework support check the crash issue.
@since: 03/27/2015
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
        self._render.install_apk("RsBalls")

    def tearDown(self):
        print "[Teardown]: %s" % self._test_name
        super(Render, self).tearDown()

    def test_sdksampleballs_appswitching(self):
        ''' refer TC test_SDKSampleBalls_AppSwitching
        '''
        print "[RunTest]: %s" % self.__str__()
        self._render.launch_rsballs_am()
        self._render.launch_photos_am()
        self._render.back_to_rsballs()
        self._render.stop_rsballs_am()