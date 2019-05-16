# -*- coding: utf-8 -*-
'''
@summary: This case will not throw Exception,
need framework support check the crash issue.
@since: 04/13/2015
@author: Yingjun Jin
'''

from testlib.graphics.test_template.render_app_testbase import RenderAppTestBase
from testlib.graphics.game_impl import GameImpl


class Game(RenderAppTestBase):

    def setUp(self):
        super(Game, self).setUp()
        self._test_name = __name__
        print "[Setup]: %s" % self._test_name
        self._game = GameImpl()
        self._game.install_apk("Plumber")

    def tearDown(self):
        print "[Teardown]: %s" % self._test_name
        super(Game, self).tearDown()
        self._game.return_normal_screen()
        self._game.uninstall_plumber()

    def test_2dgame_plumber(self):
        ''' refer TC test_2DGame_Plumber
        '''
        print "[RunTest]: %s" % self.__str__()
        self._game.launch_plumber_am()
        self._game.play_plumber()
        self._game.stop_plumber_am()
