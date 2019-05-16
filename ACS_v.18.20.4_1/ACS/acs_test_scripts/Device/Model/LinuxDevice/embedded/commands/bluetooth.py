COMMANDS = {
        "find_device":          {"description": "scan for a specific device",
                                 "function": {"_module": "bt.scan.handler",
                                              "_class": "ScanHandler",
                                              "_name": ["scan", "get_result"],
                                              "_args": {"addr": str, "timeout": int}},
                                 "requires": ["adapter"]},
        "scan":                 {"description": "scan for a duration",
                                 "function": {"_module": "bt.scan.handler",
                                              "_class": "ScanHandler",
                                              "_name": ["scan", "get_result"],
                                              "_args": {"timeout": int}},
                                 "requires": ["adapter"]},
        "set_scan_mode":        {"description": "set_scan_mode",
                                 "function": {"_module": None,
                                              "_class": "Adapter",
                                              "_name": "set_scan_mode",
                                              "_args": {"mode": str}}},
        "list_devices":         {"description": "list the scanned devices",
                                 "function": {"_module": None,
                                              "_class": "adapter",
                                              "_name": "list_devices",
                                              "_args": {}}},
        "paired_devices":       {"description": "list paired devices",
                                 "function": {"_module": None,
                                              "_class": "adapter",
                                              "_name": "paired_devices",
                                              "_args": {}}},
        "pair":                 {"description": "pair to a device",
                                 "function": {"_module": "bt.pair.handler",
                                              "_class": "BtPairHandler",
                                              "_name": ["pair", "get_result"],
                                              "_args": {"passkey": str, "pin_code": str, "timeout": int, "reply": str, "addr": str}},
                                 "requires": ["adapter"]},
        "wait_pairing":         {"description": "waits for a pairing request",
                                 "function": {"_module": "bt.pair.handler",
                                              "_class": "BtPairHandler",
                                              "_name": ["wait_for_pairing", "get_result"],
                                              "_args": {"passkey": str, "addr": str, "pin_code": str, "timeout": int, "reply": str}},
                                 "requires": ["adapter"]},
        "remove":               {"description": "removes a device",
                                 "function": {"_module": None,
                                              "_class": "adapter",
                                              "_name": "remove_device",
                                              "_args": {"addr": str}}},
        "getprop":              {"description": "get a property",
                                 "function": {"_module": None,
                                              "_class": "adapter",
                                              "_name": "getprop",
                                              "_args": {"name": str}}},
        "setprop":              {"description": "sets a property",
                                 "function": {"_module": None,
                                              "_class": "adapter",
                                              "_name": "setprop",
                                              "_args": {"name": str, "value": str}}},
        "device_getprop":       {"description": "get a device property",
                                 "function": {"_module": None,
                                              "_class": "adapter",
                                              "_name": "device_getprop",
                                              "_args": {"addr": str, "name": str}}},
        "device_setprop":       {"description": "sets a device property",
                                 "function": {"_module": None,
                                              "_class": "adapter",
                                              "_name": "device_setprop",
                                              "_args": {"addr": str, "name": str, "value": str}}},
        "connect":              {"description": "connects to a bluetooth device",
                                 "function": {"_module": "bt.connect.handler",
                                              "_class": "BtConnectHandler",
                                              "_name": "connect",
                                              "_args": {"addr": str}},
                                 "requires": ["adapter"]},
        "disconnect":           {"description": "disconnects from a device",
                                 "function": {"_module": "bt.connect.handler",
                                              "_class": "BtConnectHandler",
                                              "_name": "disconnect",
                                              "_args": {"addr": str}},
                                 "requires": ["adapter"]},
        "wait_for_connection": {"description": "wait for a bluetooth device incoming connection",
                                 "function": {"_module": "bt.connect.handler",
                                              "_class": "BtConnectHandler",
                                              "_name": ["wait_for_connection", "get_result"],
                                              "_args": {"timeout": int, "addr": str}},
                                 "requires": ["adapter"]},
        "wait_for_disconnection": {"description": "wait for a bluetooth device incoming disconnection",
                                 "function": {"_module": "bt.connect.handler",
                                              "_class": "BtConnectHandler",
                                              "_name": ["wait_for_disconnection", "get_result"],
                                              "_args": {"timeout": int, "addr": str}},
                                 "requires": ["adapter"]},
        "start_nap":        {"description": "starts NAP service",
                                 "function": {"_module": "bt.network_server",
                                              "_class": "NetworkServer",
                                              "_name": "register",
                                              "_args": {}},
                                 "requires": ["adapter"]},
        "stop_nap":         {"description": "stops NAP service",
                                 "function": {"_module": "bt.network_server",
                                              "_class": "NetworkServer",
                                              "_name": "unregister",
                                              "_args": {}},
                                 "requires": ["adapter"]},
        "set_network_bridge":
                            {"description": "Enable/Disable tethering of wifi connection over PAN",
                                 "function": {"_module": "bt.network_server",
                                              "_class": "NetworkServer",
                                              "_name": "set_network_bridge",
                                              "_args": {"state": str}},
                                 "requires": ["adapter"]},
        "get_network_bridge_state":
                            {"description": "Get state of wifi connection tethering over PAN",
                                 "function": {"_module": "bt.network_server",
                                              "_class": "NetworkServer",
                                              "_name": "get_network_bridge_state",
                                              "_args": {}},
                                 "requires": ["adapter"]},
        "start_spp_server": {"description": "start SPP server",
                                 "function": {"_module": "bt.profiles.spp",
                                      "_class": "BtSppProfile",
                                      "_name": "start",
                                      "_args": {}}},
        "stop_spp_server":  {"description": "stop SPP server",
                                 "function": {"_module": "bt.profiles.spp",
                                      "_class": "BtSppProfile",
                                      "_name": "stop",
                                      "_args": {}}},
        "spp_send":         {"description": "send data through SPP. If send from client side, addr argument is mandatory",
                                 "function": {"_module": "bt.profiles.spp",
                                      "_class": "BtSppProfile",
                                      "_name": "send",
                                      "_args": {"addr": str}}},
        "spp_receive":
                            {"description": "receive data through SPP. If receive from client side, addr argument is mandatory",
                                 "function": {"_module": "bt.profiles.spp",
                                      "_class": "BtSppProfile",
                                      "_name": "receive",
                                      "_args": {"addr": str}}},
        "spp_get_data":
                            {"description": "receive data through SPP. If receive from client side, addr argument is mandatory",
                                 "function": {"_module": "bt.profiles.spp",
                                      "_class": "BtSppProfile",
                                      "_name": "get_data",
                                      "_args": {}}},
        "enable_ip_forwarding":
                            {"description": "Get state of wifi connection tethering over PAN",
                                 "function": {"_module": "bt.network_server",
                                              "_class": "NetworkServer",
                                              "_name": "enable_ip_forwarding",
                                              "_args": {}},
                                 "requires": ["adapter"]},
    }