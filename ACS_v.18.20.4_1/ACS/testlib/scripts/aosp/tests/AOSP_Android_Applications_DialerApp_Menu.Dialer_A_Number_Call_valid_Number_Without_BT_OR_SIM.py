
#!/usr/bin/env python
#######################################################################
#
# @filename: AOSP_Android_Applications_DialerApp_Menu.Dialer_A_Number_Call_Valid_Number_Without_BT_OR_SIM.py
# @description: Dial a valid number without BT or SIM
# @author:      nidhi.anupama@intel.com
#
#
#
#######################################################################
import sys
# Used defined libraries
from testlib.base.base_utils import get_args
from testlib.scripts.android.ui import ui_steps
import time
# ############# Get parameters ############
globals().update(vars(get_args(sys.argv)))
args = {}
if script_args[0].upper() != 'NONE':
    for entry in script_args:
        key, val = entry.split("=")
        args[key] = val
# Setup
ui_steps.press_home(serial=serial)()
ui_steps.press_car(serial=serial)()
ui_steps.press_dialer(serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"Phone"},second_view_to_find={"className":"android.widget.ImageButton"},serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"Dial a number"},view_to_check={"text":"Dial a number"},serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"7"},serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"6"},serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"2"},serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"5"},serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"0"},serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"6"},serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"3"},serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"7"},serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"4"},serial=serial)()
ui_steps.click_button_common(view_to_find={"text":"7"},serial=serial)()
ui_steps.wait_for_view_common(view_to_find={"text":"(762) 506-3747"}, serial=serial)()
ui_steps.click_button_common(view_to_find={"className":"android.widget.ImageButton"},view_to_check={"text":"Phone"},serial=serial)()
