# -*- coding: utf-8 -*-
'''
@summary: This case will not throw Exception,
need framework support check the crash issue.
@since: 02/25/2015
@author: Yingjun Jin
'''

from testlib.util.uiatestbase import UIATestBase
from testlib.chromecast.chromescastmovies_impl import ChromeCastImpl

class ChromeCast(UIATestBase):

    def setUp(self):
        super(ChromeCast, self).setUp()
        self._test_name = __name__
        print "[Setup]: %s" % self._test_name
        self._chromecast = ChromeCastImpl()
        self._chromecast.set_environment()

    def tearDown(self):
        print "[Teardown]: %s" % self._test_name
        super(ChromeCast, self).tearDown()

    def test_googleplaymovie_playvideo(self):
        ''' refer TC test_GooglePlayMovie_PlayAvideoClip
        '''
        self._chromecast.launch_app_am()
        self._chromecast.play_video_via_chromecast()
        self._chromecast.check_chromecast_status()
        self._chromecast.pause_chromecast()
        self._chromecast.check_chromecast_pause()
        self._chromecast.play_chromecast()
        self._chromecast.check_chromecast_play()
        self._chromecast.stop_casting()
        self._chromecast.stop_app_am()
