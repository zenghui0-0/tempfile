import sys

from testlib.base.base_utils import get_args
from testlib.scripts.android.adb import adb_steps
from testlib.scripts.android.adb import adb_utils
from testlib.scripts.gms.google_search import google_search_steps
from testlib.scripts.android.ui import ui_utils
from testlib.scripts.android.ui import ui_steps
from testlib.scripts.gms import gms_utils
from testlib.scripts.gms.PlayStore import playstore_steps
from testlib.scripts.wireless.wifi import wifi_steps


################################################################################
# Fetch parameters passed to the script
################################################################################
args = get_args(sys.argv)
globals().update(vars(args))
globals().update(eval(script_args[0]))
adb_steps.root_connect_device(serial = serial, port = adb_server_port)()
globals().update({"version": adb_utils.get_android_version()})

ACCOUNT = account
PASSWORD = password
WHERE = 'name = "{0}"'.format(ACCOUNT)

account_exists = ui_utils.google_account_exists(serial = serial, where = WHERE)
total_account_no = gms_utils.get_google_account_number(serial = serial)

if account_exists:
    account_synced = ui_steps.sync_google_account(serial = serial,
                            account = ACCOUNT,
                            password = PASSWORD)()

if (total_account_no >= 2) or (not account_exists) or (account_exists and not account_synced):
    ui_steps.remove_all_google_accounts(serial = serial)()
    ui_steps.add_google_account_for_L(serial = serial,
                                account = ACCOUNT,
                                password = PASSWORD,
                                prefer_sync = True)()

wifi_steps.set_airplane_mode(serial = serial, state = "ON")()

google_search_steps.search_tablet_from_home(serial = serial,
                                keyword = "Maps")()
wifi_steps.set_airplane_mode(serial = serial, state = "OFF")()
