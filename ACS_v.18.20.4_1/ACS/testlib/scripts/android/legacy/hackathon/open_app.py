#!/usr/bin/env python
#######################################################################
#
# @filename:    view_tree.py
# @description: Hackaton script
# @author:      ion-horia.petrisor@intel.com
#
# python view_tree.py --serial 10.237.104.142:5555
#                     --script-args app-to-test=Shazam
#                                   wait-time=2000
#
#######################################################################

from testlib.scripts.android.adb import adb_steps
from testlib.scripts.android.adb import adb_utils
from testlib.scripts.android.ui import ui_steps
from testlib.base.base_utils import get_args
from testlib.utils.ui.uiandroid import UIDevice as ui_device
import sys
import time
import xml.etree.ElementTree as ET

nodes = []
clicked_nodes = []
dumps = []

def is_node_in_nodes(node):
    global nodes

    for n in nodes:
        if n["text"] == node["text"] and\
           n["class"] == node["class"] and\
           n["id"] == node["id"] and\
           n["desc"] == node["desc"]:
            return True
    return False


def recursive_xml_tree(uidevice, activity, level):

    global nodes
    global clicked_nodes
    global dumps

    print level

    current_dump = uidevice.dump()
    dumps.append(current_dump)

    root = ET.fromstring(current_dump)

    for node in root.iter('node'):
        if (node.get("clickable") == "true" or node.get("long-clickable") == "true")\
            and node.get("class") != "android.widget.ListView":
            new_node = {}
            new_node["class"] = node.get("class")
            new_node["text"] = node.get("text")
            new_node["desc"] = node.get("content-desc")
            new_node["id"] = node.get("resource-id")

            if is_node_in_nodes(new_node):
                nodes.append(new_node)

    for node in nodes:
        if node in clicked_nodes and node["level"] < level:
            continue
        node_filter = {}
        node_filter["className"] = node["class"]
        if node["text"] and len(node["text"]) > 0 and node["text"] is not "null":
            node_filter["text"] = node["text"]
        if node["id"] and len(node["id"]) > 0 and node["id"] is not "null":
            node_filter["resourceId"] = node["id"]
        if node["desc"] and len(node["desc"]) > 0 and node["desc"] is not "null":
            node_filter["description"] = node["desc"]

        ui_steps.click_button(view_to_find = node_filter)()
        clicked_nodes.append(node)
        uidevice.wait.update()
        if node["text"] == "Decline":
            ui_steps.open_app_from_allapps(view_to_find = {"textContains": app_to_test})()
            continue
        current_activity = adb_utils.get_running_activities()
        if current_activity != activity:
            uidevice.press.back()
            uidevice.wait.update()
        else:
            for n in nodes:
                print n
            next_dump = uidevice.dump()
            if next_dump not in dumps:
                recursive_xml_tree(uidevice, activity, level + 1)
                print "back to " + str(level)
                uidevice.press.back()

globals().update(vars(get_args(sys.argv)))

adb_steps.connect_device(
    serial = serial,
    port = adb_server_port
)()

args = {}
for entry in script_args:
    key, val = entry.split("=")
    args[key] = val

app_to_test = args["app-to-test"]
wait_time = int(args["wait-time"])/1000

ui_steps.press_home()()

################## Openning app to test
ui_steps.open_app_from_allapps(view_to_find = {"textContains": app_to_test})()
time.sleep(wait_time)

recursive_xml_tree(ui_device(), adb_utils.get_running_activities(), 0)

#ui_steps.press_home()()

