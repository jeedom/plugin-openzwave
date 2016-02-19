#!flask/bin/python
"""
Copyright (c) 2014
author: Thomas Martinez tmartinez69009@gmail.com
author: Jean-Francois Auger jeanfrancois.auger@gmail.com
SOFTWARE NOTICE AND LICENSE This file is part of Plugin openzwave for jeedom project
Plugin openzwave for jeedom is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
Plugin openzwave for jeedom is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.
You should have received a copy of the GNU General Public License along with Plugin openzwave for jeedom.
If not, see http://www.gnu.org/licenses.
"""
import sys
import os
import time
import math
from os.path import join

_log_level = 'Debug'


def add_log_entry(message, level="info"):
    if _log_level == 'Error' and level != 'error':
        return
    if _log_level == 'Info' and level == 'debug':
        return
    print('%s | %s | %s' % (time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()), '{:^5}'.format(level), message.encode('utf8'),))

add_log_entry("Check flask dependency")
try:
    from flask import Flask, jsonify, abort, request, make_response, redirect, url_for
    add_log_entry("--> pass")
except Exception as e:
    add_log_entry('The dependency of openzwave plugin are not installed. Please, \
    check the plugin openzwave configuration page for instructions', 'error')
    add_log_entry("Error: %s" % str(e), 'error')
    sys.exit(1)

add_log_entry("Check other dependency")
try:
    import logging
    import os.path
    import shutil
    import platform
    import datetime
    import binascii
    import threading
    from threading import Event, Thread
    import socket
    from lxml import etree
    import signal
    import requests
    from louie import dispatcher, All
    add_log_entry("--> pass")
except Exception as e:
    add_log_entry("The dependency of openzwave plugin are not installed. Please, \
    check the plugin openzwave configuration page for instructions", 'error')
    add_log_entry("Error: %s" % str(e), 'error')
    sys.exit(1)

if not os.path.exists('/tmp/python-openzwave-eggs'):
    os.makedirs('/tmp/python-openzwave-eggs')
    
os.environ['PYTHON_EGG_CACHE'] = '/tmp/python-openzwave-eggs'

logging.basicConfig(level=logging.ERROR)
_logger = logging.getLogger('openzwave')

reload(sys)  
sys.setdefaultencoding('utf8')

add_log_entry("Check Openzwave")
# import openzwave
# from openzwave.node import ZWaveNode
# from openzwave.value import ZWaveValue
# from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
# from openzwave.group import ZWaveGroup
add_log_entry("--> pass")

    
_device = "auto"
# noinspection PyRedeclaration
_log_level = "None"
_port_server = 8083
_config_folder = None
_data_folder = None
_pid_file = None
_callback = None
_apikey = None
_server_id = 0

# default_poll_interval = 1800000  # 30 minutes
_default_poll_interval = 300000  # 5 minutes
_maximum_poll_intensity = 1
_controller_state = -1

# maximum time (in seconds) allowed for a background refresh
_refresh_timeout = 120
# background refresh interval step in seconds
_refresh_interval = 3
# post topology loaded delay tasks
_refresh_configuration_timer = 360.0
_refresh_user_values_timer = 120.0
_validate_association_groups_timer = 45.0
_recovering_failed_nodes_timer = 900.0  # 15 minutes
# perform sanitary jobs
_recovering_failed_nodes_jobs_timer = 900.0  # 15 minutes

_network = None
_network_information = None

_force_refresh_nodes = []
_changes_async = {'device': {}}
_cycle = 0.5
_ghost_node_id = None

COMMAND_CLASS_NO_OPERATION              = 0  # 0x00
COMMAND_CLASS_BASIC                     = 32  # 0x20
COMMAND_CLASS_CONTROLLER_REPLICATION    = 33  # 0x21
COMMAND_CLASS_APPLICATION_STATUS        = 34  # 0x22
# COMMAND_CLASS_ZIP_SERVICES              = 35  # 0x23
# COMMAND_CLASS_ZIP_SERVER                = 36  # 0x24
COMMAND_CLASS_SWITCH_BINARY             = 37  # 0x25
COMMAND_CLASS_SWITCH_MULTILEVEL         = 38  # 0x26
COMMAND_CLASS_SWITCH_ALL                = 39  # 0x27
COMMAND_CLASS_SWITCH_TOGGLE_BINARY      = 40  # 0x28
COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL  = 41  # 0x29
# COMMAND_CLASS_CHIMNEY_FAN               = 42  # 0x2A
COMMAND_CLASS_SCENE_ACTIVATION          = 43  # 0x2B
# COMMAND_CLASS_SCENE_ACTUATOR_CONF       = 44  # 0x2C
# COMMAND_CLASS_SCENE_CONTROLLER_CONF     = 45  # 0x2D
# COMMAND_CLASS_ZIP_CLIENT                = 46  # 0x2E
# COMMAND_CLASS_ZIP_ADV_SERVICES          = 47  # 0x2F
COMMAND_CLASS_SENSOR_BINARY             = 48  # 0x30
COMMAND_CLASS_SENSOR_MULTILEVEL         = 49  # 0x31
COMMAND_CLASS_METER                     = 50  # 0x32
COMMAND_CLASS_COLOR                     = 51  # 0x33
# COMMAND_CLASS_ZIP_ADV_CLIENT            = 52  # 0x34
COMMAND_CLASS_METER_PULSE               = 53  # 0x35
# COMMAND_CLASS_THERMOSTAT_HEATING        = 56  # 0x38
# COMMAND_CLASS_METER_TBL_CONFIG          = 60  # 0x3C
# COMMAND_CLASS_METER_TBL_MONITOR         = 61  # 0x3D
# COMMAND_CLASS_METER_TBL_PUSH            = 62  # 0x3E
COMMAND_CLASS_THERMOSTAT_MODE           = 64  # 0x40
COMMAND_CLASS_THERMOSTAT_OPERATING_STATE = 66  # 0x42
COMMAND_CLASS_THERMOSTAT_SET_POINT       = 67  # 0x43
COMMAND_CLASS_THERMOSTAT_FAN_MODE       = 68  # 0x44
COMMAND_CLASS_THERMOSTAT_FAN_STATE      = 69  # 0x45
COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE  = 70  # 0x46
# COMMAND_CLASS_THERMOSTAT_SETBACK        = 71  # 0x47
COMMAND_CLASS_DOOR_LOCK_LOGGING         = 76  # 0x4C
# COMMAND_CLASS_SCHEDULE_ENTRY_LOCK       = 78  # 0x4E
COMMAND_CLASS_BASIC_WINDOW_COVERING     = 80  # 0x50
# COMMAND_CLASS_MTP_WINDOW_COVERING       = 81  # 0x51
COMMAND_CLASS_CRC_16_ENCAP              = 86  # 0x56
COMMAND_CLASS_DEVICE_RESET_LOCALLY      = 90  # 0x5A
COMMAND_CLASS_CENTRAL_SCENE              = 91  # 0x5B
COMMAND_CLASS_ZWAVE_PLUS_INFO           = 94  # 0x5E
COMMAND_CLASS_MULTI_INSTANCE            = 96  # 0x60
COMMAND_CLASS_DOOR_LOCK                 = 98  # 0x62
COMMAND_CLASS_USER_CODE                 = 99  # 0x63
COMMAND_CLASS_BARRIER_OPERATOR          = 102  # 0x66
COMMAND_CLASS_CONFIGURATION             = 112  # 0x70
COMMAND_CLASS_ALARM                     = 113  # 0x71
COMMAND_CLASS_MANUFACTURER_SPECIFIC     = 114  # 0x72
COMMAND_CLASS_POWER_LEVEL                = 115  # 0x73
COMMAND_CLASS_PROTECTION                = 117  # 0x75
COMMAND_CLASS_LOCK                      = 118  # 0x76
COMMAND_CLASS_NODE_NAMING               = 119  # 0x77
# COMMAND_CLASS_FIRMWARE_UPDATE_MD        = 122  # 0x7A
# COMMAND_CLASS_GROUPING_NAME             = 123  # 0x7B
# COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE =124  # 0x7C
# COMMAND_CLASS_REMOTE_ASSOCIATION        = 125  # 0x7D
COMMAND_CLASS_BATTERY                   = 128  # 0x80
COMMAND_CLASS_CLOCK                     = 129  # 0x81
COMMAND_CLASS_HAIL                      = 130  # 0x82
COMMAND_CLASS_WAKE_UP                   = 132  # 0x84
COMMAND_CLASS_ASSOCIATION               = 133  # 0x85
COMMAND_CLASS_VERSION                   = 134  # 0x86
COMMAND_CLASS_INDICATOR                 = 135  # 0x87
COMMAND_CLASS_PROPRIETARY               = 136  # 0x88
COMMAND_CLASS_LANGUAGE                  = 137  # 0x89
# COMMAND_CLASS_TIME                      = 138  # 0x8A
COMMAND_CLASS_TIME_PARAMETERS           = 139  # 0x8B
# COMMAND_CLASS_GEOGRAPHIC_LOCATION       = 150  # 0x8C
# COMMAND_CLASS_COMPOSITE                 = 141  # 0x8D
COMMAND_CLASS_MULTI_INSTANCE_ASSOCIATION = 142  # 0x8E
COMMAND_CLASS_MULTI_CMD                 = 143  # 0x8F
COMMAND_CLASS_ENERGY_PRODUCTION         = 144  # 0x90
# COMMAND_CLASS_MANUFACTURER_PROPRIETARY  = 145  # 0x91
# COMMAND_CLASS_SCREEN_MD                 = 146  # 0x92
# COMMAND_CLASS_SCREEN_ATTRIBUTES         = 147  # 0x93
# COMMAND_CLASS_SIMPLE_AV_CONTROL         = 148  # 0x94
# COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD   = 149  # 0x95
# COMMAND_CLASS_AV_RENDERER_STATUS        = 150  # 0x96
# COMMAND_CLASS_AV_CONTENT_SEARCH_MD      = 151  # 0x97
COMMAND_CLASS_SECURITY                  = 152  # 0x98
# COMMAND_CLASS_AV_TAGGING_MD             = 153  # 0x99
# COMMAND_CLASS_IP_CONFIGURATION          = 154  # 0x9A
COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION = 155  # 0x9B
COMMAND_CLASS_SENSOR_ALARM              = 156  # 0x9C
# COMMAND_CLASS_SILENCE_ALARM             = 157  # 0x9D
# COMMAND_CLASS_SENSOR_CONFIGURATION      = 158  # 0x9E
# COMMAND_CLASS_MARK                      = 239  # 0xEF
# COMMAND_CLASS_NON_INTEROPERABLE         = 240  # 0xF0

add_log_entry("validate startup arguments")

for arg in sys.argv:
    if arg.startswith("--device="):
        temp, _device = arg.split("=")
    elif arg.startswith("--port="):
        temp, _port_server = arg.split("=")
    elif arg.startswith("--log="):
        temp, _log_level = arg.split("=")
    elif arg.startswith("--config_folder="):
        temp, _config_folder = arg.split("=")
    elif arg.startswith("--data_folder="):
        temp, _data_folder = arg.split("=")
    elif arg.startswith("--pidfile"):
        temp, _pid_file = arg.split("=")
    elif arg.startswith("--callback="):
        temp, _callback = arg.split("=")
    elif arg.startswith("--apikey="):
        temp, _apikey = arg.split("=")
    elif arg.startswith("--serverId="):
        temp, _server_id = arg.split("=")
    elif arg.startswith("--help"):
        print("help: ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug|Error")
add_log_entry("--> pass")

def find_tty_usb(id_vendor, id_product):
    """find_tty_usb('0658', '0200') -> '/dev/ttyUSB021' for Sigma Designs, Inc."""
    # Note: if searching for a lot of pairs, it would be much faster to search
    # for the entire lot at once instead of going over all the usb devices
    # each time.
    # print('check for idVendor:%s idProduct: %s' % (id_vendor, id_product,))
    for device_base in os.listdir('/sys/bus/usb/devices'):
        dn = join('/sys/bus/usb/devices', device_base)
        if not os.path.exists(join(dn, 'idVendor')):
            continue
        idv = open(join(dn, 'idVendor')).read().strip()
        if idv != id_vendor:
            continue
        idp = open(join(dn, 'idProduct')).read().strip()
        if idp != id_product:
            continue
        for subdir in os.listdir(dn):
            if subdir.startswith(device_base+':'):
                for sub_subdir in os.listdir(join(dn, subdir)):
                    if sub_subdir.startswith('ttyUSB'):
                        return join('/dev', sub_subdir)

def debug_print(message):
    add_log_entry(message, 'debug')

add_log_entry("check if port is available")     
_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_available = _sock.connect_ex(('127.0.0.1', int(_port_server)))
if port_available == 0:
    add_log_entry('The port %s is already in use. Please check your openzwave configuration plugin page' % (_port_server,), 'error')
    sys.exit(1) 
add_log_entry("--> pass")   

# device = 'auto'
if _device == 'auto':
    know_sticks = [{'idVendor': '0658', 'idProduct': '0200', 'name': 'Sigma Designs, Inc'},
                   {'idVendor': '10c4', 'idProduct': 'ea60', 'name': 'Cygnal Integrated Products, Inc. CP210x UART Bridge'}]
    
    for stick in know_sticks:
        _device = find_tty_usb(stick['idVendor'], stick['idProduct'])
        if _device is not None:
            add_log_entry('USB Z-Wave Stick found:%s' % (stick['name'],))
            break
    if _device is None:
        add_log_entry('No USB Z-Wave Stick detected', 'error')
        sys.exit(1)

Idle = 0
AddDevice = 1
RemoveDevice = 5

_not_supported_nodes = [0, 255]

_user_values_to_refresh = ["Level", "Sensor", "Switch", "Power", "Temperature", "Alarm Type", "Alarm Type", "Power Management"]


class ControllerMode:
    def __init__(self):
        pass

    class Idle:
        def __init__(self):
            pass

    class AddDevice:
        def __init__(self):
            pass

    class RemoveDevice:
        def __init__(self):
            pass

  
class NetworkInformation(object):

    def __init__(self):
        self._actualMode = ControllerMode.Idle
        self._start_time = int(time.time())
        self._awake_time = None
        self._config_file_save_in_progress = False
        self._controller_is_busy = False
        self._controller_state = ZWaveController.STATE_STARTING
        self._last_controller_notification = {"state": self._controller_state, "details": '', "error": None, "error_description": None, "timestamp": int(time.time())}
        self._error = None
        self._error_description = None
    
    @property
    def actual_mode(self):
        return self._actualMode
    
    @actual_mode.setter
    def actual_mode(self, value):
        self._actualMode = value
        
    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, value):
        self._start_time = value
        
    @property
    def config_file_save_in_progress(self):
        return self._config_file_save_in_progress
    
    @config_file_save_in_progress.setter
    def config_file_save_in_progress(self, value):
        self._config_file_save_in_progress = value
        
    @property
    def controller_is_busy(self):
        return self._controller_is_busy
    
    @controller_is_busy.setter
    def controller_is_busy(self, value):
        self._controller_is_busy = value
        
    @property
    def controller_state(self):
        return self._controller_state
    
    @property
    def last_controller_notification(self):
        return self._last_controller_notification
    
    @property
    def error(self):        
        return self._error
    
    @property
    def error_description(self):        
        return self._error_description
    
    def set_as_awake(self):
        self._awake_time = int(time.time())
        self.assign_controller_notification(ZWaveController.SIGNAL_CTRL_NORMAL, "Network is awake")
        
    @property
    def controller_awake_delay(self):
        if self._awake_time is not None:
            return self._awake_time - self._start_time
        return None
    
    def assign_controller_notification(self, state, details, error=None, error_description=None):
        self._controller_state = state
        self._last_controller_notification['state'] = state
        self._last_controller_notification['details'] = details
        if error == 'None':
            self._last_controller_notification['error'] = None
            self._last_controller_notification['error_description'] = None
        else:
            self._last_controller_notification['error'] = error
            self._last_controller_notification['error_description'] = error_description
        self._last_controller_notification['timestamp'] = int(time.time())
        self._error = error
        self._error_description = error_description
        
        if state == ZWaveController.STATE_WAITING:
            self.controller_is_busy = True
        elif state == ZWaveController.STATE_INPROGRESS:
            self.controller_is_busy = True
        elif state == ZWaveController.STATE_STARTING:
            self.controller_is_busy = True
        else:
            self.controller_is_busy = False
            # reset flag
            self.actual_mode = ControllerMode.Idle
            
    def generate_jeedom_message(self):
        if self.actual_mode == ControllerMode.AddDevice:
            return AddDevice         
        elif self.actual_mode == ControllerMode.RemoveDevice:
            return RemoveDevice
        else:
            return Idle

    def reset(self):
        self._actualMode = ControllerMode.Idle
        self._start_time = int(time.time())
        self._awake_time = None
        self._config_file_save_in_progress = False
        self._controller_is_busy = False
        self._controller_state = ZWaveController.STATE_STARTING
        self._last_controller_notification = {"state": self._controller_state, "details": '', "error": None, "error_description": None, "timestamp": int(time.time())}
        self._error = None
        self._error_description = None


class PendingConfiguration(object):
    
    def __init__(self, expected_data, timeout):
        self._startTime = int(time.time())
        self._expected_data = expected_data
        self._timeOut = timeout
        self._data = None 
        
    @property
    def expected_data(self):        
        return self._expected_data
    
    @property
    def data(self):        
        return self._data
    
    @data.setter
    def data(self, value):        
        self._data = value
        
    @property
    def state(self):  
        if self._data is None:
            # is pending
            return 3
        if self._data != self._expected_data:
            # the node reject changes and set a default
            return 2
        # the parameter have be set successfully
        return 1

            
class NodeNotification(object):
    
    def __init__(self, code, wake_up_time=None):
        self._code = code 
        self._description = code 
        self._help = code 
        self._wake_up_time = wake_up_time
        self._next_wake_up = None
        self.refresh(code, wake_up_time)
        self._receive_time = None
        
    def refresh(self, code, wake_up_time):
        # save notification
        self._code = code
        # reset time stamp
        self._receive_time = int(time.time())
        if self.code == 0:
            self._description = "Completed"
            self._help = "Completed messages"
        elif self.code == 1:
            self._description = "Timeout"
            self._help = "Messages that timeout will send a Notification with this code"
        elif self.code == 2:
            self._description = "NoOperation"
            self._help = "Report on NoOperation message sent completion"
        elif self.code == 3:
            self._description = "Awake"
            self._help = "Report when a sleeping node wakes"
            self._next_wake_up = None  # clear and wait sleep to compute next expected wake up
        elif self.code == 4:
            self._description = "Sleep"
            self._help = "Report when a node goes to sleep"
            # if they go to sleep, compute the next expected wake up time
            if wake_up_time is not None and wake_up_time > 0:
                self._next_wake_up = self._receive_time + wake_up_time
        elif self.code == 5:
            self._description = "Dead"
            self._help = "Report when a node is presumed dead"
        elif self.code == 6:
            self._description = "Alive"
            self._help = "Report when a node is revived"
        else:
            self._description = "Unknown state"
            self._help = ""
            
    @property
    def code(self):        
        return self._code
    
    @property
    def receive_time(self):        
        return self._receive_time
    
    @property
    def description(self):        
        return self._description
    
    @property
    def help(self):        
        return self._help
    
    @property
    def next_wake_up(self):
        return self._next_wake_up
        

def start_network():
    global _network_information, _force_refresh_nodes
    # reset flags
    _force_refresh_nodes = []
    if _network_information is None:
        _network_information = NetworkInformation()
    else:
        _network_information.reset()
    add_log_entry('******** The ZWave network is being started ********')
    _network.start()


def cleanup_configuration_file(filename):
    global _data_folder
    add_log_entry('validate configuration file: %s' % (filename,))
    if os.path.isfile(filename):
        try:            
            tree = etree.parse(filename)
            nodes = tree.findall(".//{http://code.google.com/p/open-zwave/}Product")
            for node in nodes:
                if node.get("id")[:7] in _not_supported_nodes:
                    tree.getroot().remove(node.getparent().getparent())
                elif node.get("name")[:7] == "Unknown":
                    tree.getroot().remove(node.getparent().getparent())
            working_file = open(filename, "w")
            working_file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
            working_file.writelines(etree.tostring(tree, pretty_print=True))
            working_file.close()
        except Exception as exception:
            add_log_entry(str(exception), 'error')
            add_log_entry('Trying to find the most recent valid xml in backups')
            backup_folder = _data_folder + "/xml_backups"
            # noinspection PyBroadException
            try:
                os.stat(backup_folder)
            except:
                os.mkdir(backup_folder)
            pattern = "_zwcfg_"
            filters = ['xml']
            path = os.path.join(backup_folder, "")
            actual_backups = os.listdir(backup_folder)
            actual_backups.sort(reverse=True)
            found_valid_backup = 0
            for candidateBackup in actual_backups:
                if candidateBackup[-3:] in filters and pattern in candidateBackup:
                    try:            
                        tree = etree.parse(os.path.join(backup_folder, candidateBackup))
                        final_filename = candidateBackup[candidateBackup.find('zwcfg'):]
                        shutil.copy2(os.path.join(backup_folder, candidateBackup), os.path.join(_data_folder, final_filename))
                        os.chmod(final_filename, 0777)
                        add_log_entry('Found one valid backup. Using it')
                        found_valid_backup = 1
                        break
                    except Exception as exception:
                        add_log_entry(str(exception), 'error')
                        continue
            if found_valid_backup == 0:
                add_log_entry('No valid backup found. Regenerating')


def check_config_files():
    global _data_folder
    root = _data_folder
    pattern = "zwcfg_"
    filters = ['xml']
    path = os.path.join(root, "")
    actual_configurations = os.listdir(root)
    for configuration_file in actual_configurations:
        if configuration_file[-3:] in filters and pattern in configuration_file:
            cleanup_configuration_file(os.path.join(root, configuration_file))


def backup_xml_config(mode, home_id):
    global _data_folder
    # backup xml config file
    add_log_entry('Backup xml config file with mode: %s' % (mode,))
    # prepare all variables
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
    xmm_to_backup = _data_folder + "/zwcfg_" + home_id + ".xml"
    if not os.path.isfile(xmm_to_backup):
        add_log_entry('No config file found to backup', "error")
        return format_json_result(False, 'No config file found to backup')
    backup_folder = _data_folder + "/xml_backups"
    backup_name = timestamp + "_" + mode + "_zwcfg_" + home_id + ".xml"
    # check if folder exist (more efficient way)
    # noinspection PyBroadException
    try:
        os.stat(backup_folder)
    except:
        os.mkdir(backup_folder)
    # check if we need to clean the folder
    actual_backups = os.listdir(backup_folder)
    actual_backups.sort()
    for backup in actual_backups:
        if 'manual' in backup:
            actual_backups.remove(backup)
    if len(actual_backups) > 12:
        add_log_entry('More than 12 auto backups found. Cleaning the folder')
        for fileToDelete in actual_backups[:-11]:
            os.unlink(os.path.join(backup_folder, fileToDelete))
    # make the backup
    try:
        final_path = os.path.join(backup_folder, backup_name)
        tree = etree.parse(xmm_to_backup)
        shutil.copy2(xmm_to_backup, final_path)
    except Exception as error:
        add_log_entry('Backup xml failed %s' % (str(error),), "error")
        return format_json_result(False, 'Backup xml failed')
    add_log_entry('Xml config file successfully backup')
    return format_json_result(True, 'Xml config file successfully backup')


def graceful_stop_network():
    add_log_entry('Graceful stopping the ZWave network.')   
    global _network
    home_id = _network.home_id_str
    if _network is not None:
        _network.stop()
        # We disconnect to the louie dispatcher
        # noinspection PyBroadException
        try:
            dispatcher.disconnect(network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
            dispatcher.disconnect(network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
            dispatcher.disconnect(network_failed, ZWaveNetwork.SIGNAL_DRIVER_FAILED)
            dispatcher.disconnect(network_awaked, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
            dispatcher.disconnect(network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
            dispatcher.disconnect(node_new, ZWaveNetwork.SIGNAL_NODE_NEW)
            dispatcher.disconnect(node_added, ZWaveNetwork.SIGNAL_NODE_ADDED)
            dispatcher.disconnect(node_removed, ZWaveNetwork.SIGNAL_NODE_REMOVED)
            dispatcher.disconnect(value_added, ZWaveNetwork.SIGNAL_VALUE_ADDED)
            dispatcher.disconnect(value_update, ZWaveNetwork.SIGNAL_VALUE_CHANGED)
            dispatcher.disconnect(value_refreshed, ZWaveNetwork.SIGNAL_VALUE_REFRESHED)
            # dispatcher.disconnect(value_polling_enabled, ZWaveNetwork.SIGNAL_POLLING_ENABLED)
            dispatcher.disconnect(node_event, ZWaveNetwork.SIGNAL_NODE_EVENT)
            dispatcher.disconnect(scene_event, ZWaveNetwork.SIGNAL_SCENE_EVENT)
            dispatcher.disconnect(essential_node_queries_complete, ZWaveNetwork.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE)
            dispatcher.disconnect(node_queries_complete, ZWaveNetwork.SIGNAL_NODE_QUERIES_COMPLETE)
            dispatcher.disconnect(nodes_queried, ZWaveNetwork.SIGNAL_AWAKE_NODES_QUERIED)
            dispatcher.disconnect(nodes_queried, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED)
            dispatcher.disconnect(nodes_queried_some_dead, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD)
            dispatcher.disconnect(button_on, ZWaveNetwork.SIGNAL_BUTTON_ON)
            dispatcher.disconnect(button_off, ZWaveNetwork.SIGNAL_BUTTON_OFF)
            dispatcher.disconnect(node_notification, ZWaveNetwork.SIGNAL_NOTIFICATION) 
            dispatcher.disconnect(node_group_changed, ZWaveNetwork.SIGNAL_GROUP)
            dispatcher.disconnect(controller_waiting, ZWaveNetwork.SIGNAL_CONTROLLER_WAITING)
            dispatcher.disconnect(controller_command, ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND)
            dispatcher.disconnect(controller_message_complete, ZWaveNetwork.SIGNAL_MSG_COMPLETE)
        except Exception:
            pass
        _network.destroy()
        # avoid a second pass
        _network = None
    add_log_entry('The Openzwave REST-server was stopped in a normal way')
    backup_xml_config('stop', home_id)

# Define some manager options
options = ZWaveOption(_device, config_path=_config_folder, user_path=_data_folder, cmd_line="")
options.set_log_file("openzwave.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level(_log_level)
options.set_logging(True)
options.set_associate(True)                       
options.set_save_configuration(True)              
options.set_poll_interval(_default_poll_interval)
options.set_interval_between_polls(False)         
options.set_notify_transactions(True)  # Notifications when transaction complete is reported.
options.set_suppress_value_refresh(False)  # if true, notifications for refreshed (but unchanged) values will not be sent.
options.set_driver_max_attempts(5) 
options.addOptionBool("AssumeAwake", False)        
# options.addOptionInt("RetryTimeout", 6000)  # Timeout before retrying to send a message. Defaults to 40 Seconds
options.addOptionString("NetworkKey", "0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10", True)
options.set_security_strategy('CUSTOM')  # The security strategy: SUPPORTED | ESSENTIAL | CUSTOM
options.set_custom_secured_cc('0x62,0x4c,0x63')  # What List of Custom CC should we always encrypt if SecurityStrategy is CUSTOM
options.addOptionBool('EnforceSecureReception', False)  # if we receive a clear text message for a CC that is Secured, should we drop the message
options.addOptionBool('RefreshAllUserCodes', False)  # Some Devices have a big UserCode Table, that can mean startup times when refreshing Session Variables is very long
options.addOptionBool('ThreadTerminateTimeout', 5000)  #
options.lock()


check_config_files()


def send_changes_async():
    global _changes_async
    global _server_id
    try:
        start_time = datetime.datetime.now()
        changes = _changes_async
        _changes_async = {}
        if 'device' in changes or 'controller' in changes or 'network' in changes:
            changes['serverId'] = _server_id
            # debug_print('Send data async to jeedom %s => %s' % (callback+'?apikey='+apikey,str(changes),))
            debug_print('Push data to jeedom')
            try:
                r = requests.post(_callback + '?apikey=' + _apikey, json=changes, timeout=(0.5, 120), verify=False)
                if r.status_code != requests.codes.ok:
                    add_log_entry('Error on send request to jeedom, return code %s' % (str(r.status_code),), "error")
            except Exception as error:
                add_log_entry('Error on send request to jeedom %s' % (str(error),), "error")
        dt = datetime.datetime.now() - start_time
        ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
        timer_duration = _cycle - ms
        if timer_duration < 0.1:
            timer_duration = 0.1
        resend_changes = threading.Timer(timer_duration, send_changes_async)
        resend_changes.start() 
    except Exception as error:
        add_log_entry('Critical error on  send_changes_async %s' % (str(error),), "error")
        resend_changes = threading.Timer(_cycle, send_changes_async)
        resend_changes.start() 

send_changes_async()


def save_node_value_event(node_id, timestamp, command_class, value_index, standard_type, value, instance):
    global _changes_async
    if 'device' not in _changes_async:
        _changes_async['device'] = {}
    if node_id not in _changes_async['device']:
        _changes_async['device'][node_id] = {}
    _changes_async['device'][node_id][str(hex(command_class)) + str(instance) + str(value_index)] = {'node_id': node_id, 'instance': instance, 'CommandClass': hex(command_class), 'index': value_index, 'value': value, 'type': standard_type, 'updateTime': timestamp}


def save_node_event(node_id, value):
    global _controller_state
    global _changes_async
    if value == "removed":
        if 'controller' not in _changes_async:
            _changes_async['controller'] = {}
        _changes_async['controller']['excluded'] = {"value": node_id}
    elif value == "added":
        if 'controller' not in _changes_async:
            _changes_async['controller'] = {}
        _changes_async['controller']['included'] = {"value": node_id}
    elif value in [0, 1, 5] and _controller_state != value:
        # save controller state
        _controller_state = value
        # not controller notification before network is at least awaked
        if _network.state >= 7:
            if 'controller' not in _changes_async:
                _changes_async['controller'] = {}
            _changes_async['controller']['state'] = {"value": value}


def save_network_state(network_state):
    # STATE_STOPPED = 0
    # STATE_FAILED = 1
    # STATE_RESET = 3
    # STATE_STARTED = 5
    # STATE_AWAKED = 7
    # STATE_READY = 10
    global _changes_async
    if 'network' not in _changes_async:
        _changes_async['network'] = {}
    _changes_async['network']['state'] = {"value": network_state}


def push_node_notification(node_id, notification_code):
    # check for notification Dead or Alive
    if notification_code in [5, 6]:
        if notification_code == 5:
            # Report when a node is presumed dead
            alert_type = 'node_dead'
        else:
            # Report when a node is revived
            alert_type = 'node_alive'
        changes = {'alert': {'type': alert_type , 'id': node_id, 'serverId': _server_id}}
        try:
            r = requests.post(_callback + '?apikey=' + _apikey, json=changes, timeout=(0.5, 120), verify=False)
            if r.status_code != requests.codes.ok:
                add_log_entry('Error on send request to jeedom, return code %s' % (str(r.status_code),), "error")
        except Exception as error:
            add_log_entry('Error on send request to jeedom %s' % (str(error),), "error")


def network_started(network):
    add_log_entry("Openzwave network are started with homeId %0.8x." % (network.home_id,))    
    _network_information.assign_controller_notification(ZWaveController.SIGNAL_CTRL_STARTING, "Network is started")
    save_network_state(network.state)
    if network.manager.getPollInterval() != _default_poll_interval:
        network.set_poll_interval(_default_poll_interval, False)


def network_failed(network):
    add_log_entry("Openzwave network can't load", "error")
    _network_information.assign_controller_notification(ZWaveController.SIGNAL_CTRL_ERROR, "Network have failed")
    save_network_state(network.state)


def validate_association_groups_asynchronous():
    debug_print("Check association")
    for node_id in list(_network.nodes):
        if validate_association_groups(node_id):
            # avoid stress network
            time.sleep(3)


def recovering_failed_nodes_asynchronous():
    global _ghost_node_id
    # wait 15 seconds on first launch
    time.sleep(15.0)    
    while True: 
        # if controller is busy skip this run
        if can_execute_network_command(0):      
            debug_print("Perform network sanity test/check")
            for node_id in list(_network.nodes):
                my_node = _network.nodes[node_id]
                # first check if a ghost node wait to be removed
                if _ghost_node_id is not None and node_id == _ghost_node_id and my_node.is_failed:
                    add_log_entry('* Try to remove a Ghost node (nodeId: %s)' % (node_id,))
                    _network.manager.removeFailedNode(_network.home_id, node_id)
                    time.sleep(10)
                    if _ghost_node_id not in _network.nodes:
                        # reset ghost node flag
                        _ghost_node_id = None
                        add_log_entry('=> Ghost node removed (nodeId: %s)' % (node_id,))
                    continue
                if node_id in _not_supported_nodes:
                    debug_print('=> Remove not valid nodeId: %s' % (node_id,))
                    _network.manager.removeFailedNode(_network.home_id, node_id)
                    time.sleep(10)
                    continue
                if my_node.is_failed:
                    debug_print('=> Try recovering, presumed Dead, nodeId: %s' % (node_id,))
                    # a ping will try to revive the node
                    _network.manager.testNetworkNode(_network.home_id, node_id, 1)
                    # avoid stress network
                    time.sleep(5)
                    if _network.manager.hasNodeFailed(_network.home_id, node_id):
                        # avoid stress network
                        time.sleep(5)
                elif my_node.is_listening_device and my_node.is_ready:
                    # check if a ping is require
                    if hasattr(my_node, 'last_notification'):
                        # debug_print('=> last_notification for nodeId: %s is: %s(%s)' % (node_id, my_node.last_notification.description, my_node.last_notification.code,))
                        # is in timeout or dead
                        if my_node.last_notification.code in [1, 5]:
                            debug_print('=> Do a test on node %s' % (node_id,))
                            # a ping will try to resolve this situation with a NoOperation CC. 
                            _network.manager.testNetworkNode(_network.home_id, node_id, 3)
                            # avoid stress network
                            time.sleep(10)
                elif not my_node.is_listening_device and my_node.is_ready :
                    if hasattr(my_node, 'last_notification'):
                        # check if controller think is awake
                        if my_node.is_awake or my_node.last_notification.code == 3 :
                            debug_print('trying to lull the node %s' % (node_id,))
                            # a ping will force the node to return sleep after the NoOperation CC. Will force node notification update
                            _network.manager.testNetworkNode(_network.home_id, node_id, 1)

            debug_print("Network sanity test/check completed!")
        else:
            debug_print("Network is loaded, skip sanity check this time")
        # wait for next run    
        time.sleep(_recovering_failed_nodes_timer)


def refresh_configuration_asynchronous():
    if can_execute_network_command(0):
        for node_id in list(_force_refresh_nodes):
            if node_id in _network.nodes and not _network.nodes[node_id].is_failed:
                debug_print('Request All Configuration Parameters for nodeId: %s' % (node_id,)) 
                _network.manager.requestAllConfigParams(_network.home_id, node_id)
                time.sleep(3)
    else:
        # I will try again in 2 minutes
        retry_job = threading.Timer(240.0, refresh_configuration_asynchronous)
        retry_job.start()        


def refresh_user_values_asynchronous():
    debug_print("Refresh User Values of powered devices")
    if can_execute_network_command(0):
        for node_id in list(_network.nodes):
            my_node = _network.nodes[node_id]
            if my_node.is_ready and my_node.is_listening_device and not my_node.is_failed:
                debug_print('Refresh User Values for nodeId: %s' % (node_id,))
                for val in my_node.get_values():
                    current_value = my_node.values[val]
                    if current_value.genre == 'User':
                        if current_value.type == 'Button':
                            continue
                        if current_value.is_write_only:
                            continue   
                        if current_value.label in _user_values_to_refresh:
                            current_value.refresh()
                while not can_execute_network_command(0):
                    debug_print("BackgroundWorker is waiting others tasks has be completed before proceeding")
                    time.sleep(30)
    else:
        debug_print("Network is loaded, do not execute this time")
        # I will try again in 2 minutes
        retry_job = threading.Timer(240.0, refresh_user_values_asynchronous)
        retry_job.start()           


def network_awaked(network):
    add_log_entry("Openzwave network is awake: %d nodes were found (%d are sleeping). All listening nodes are queried, but some sleeping nodes may be missing." % (network.nodes_count, get_sleeping_nodes_count(),))
    add_log_entry("Controller is: %s" % (network.controller,))
    _network_information.set_as_awake()
    configuration = threading.Timer(_refresh_configuration_timer, refresh_configuration_asynchronous)
    configuration.start() 
    add_log_entry("Refresh configuration parameters will starting in %d sec" % (_refresh_configuration_timer,))
    user_values = threading.Timer(_refresh_user_values_timer, refresh_user_values_asynchronous)
    user_values.start() 
    add_log_entry("Refresh user values will starting in %d sec" % (_refresh_user_values_timer,))
    association = threading.Timer(_validate_association_groups_timer, validate_association_groups_asynchronous)
    association.start()
    add_log_entry("Validate association groups will starting in %d sec" % (_validate_association_groups_timer,))
    threading.Thread(target=recovering_failed_nodes_asynchronous).start()
    # start listening for group changes
    dispatcher.connect(node_group_changed, ZWaveNetwork.SIGNAL_GROUP)
    save_network_state(network.state)


def network_ready(network):
    add_log_entry("Openzwave network is ready with %d nodes (%d are sleeping). All nodes are queried, the network is fully functional." % (network.nodes_count, get_sleeping_nodes_count(),))
    write_config()
    _network_information.assign_controller_notification(ZWaveController.SIGNAL_CTRL_NORMAL, "Network is ready")
    save_network_state(network.state)


def button_on(network, node):
    add_log_entry('Controller button on pressed event') 


def button_off(network, node):
    add_log_entry('Controller button off pressed event') 


def nodes_queried(network):    
    write_config() 


def nodes_queried_some_dead(network):
    write_config()  
    add_log_entry("All nodes have been queried, but some node ar mark dead") 


def node_new(network, node_id):
    if node_id in _not_supported_nodes:
        return
    add_log_entry('A new node (%s), not already stored in zwcfg*.xml file, was found.' % (node_id,))
    _force_refresh_nodes.append(node_id)


def node_added(network, node):    
    add_log_entry('A node has been added to OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
    if node.node_id in _not_supported_nodes:
        debug_print('remove fake nodeId: %s' % (node.node_id,))
        node_cleaner = threading.Timer(60.0, network.manager.removeFailedNode, [network.home_id, node.node_id])
        node_cleaner.start()        
        return
    node.last_update = time.time()
    if network.state >= 7:  # STATE_AWAKE
        save_node_event(node.node_id, "added")


def node_removed(network, node):
    add_log_entry('A node has been removed from OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
    if node.node_id in _not_supported_nodes:
        return
    if network.state >= 7:  # STATE_AWAKE
        save_node_event(node.node_id, "removed")


def get_standard_value_type(value_type):
    if value_type == "Int":
        return 'int'
    elif value_type == "Decimal":
        return 'float'
    elif value_type == "Bool":
        return 'bool'
    elif value_type == "Byte":
        return 'int'
    elif value_type == "Short":
        return 'int'
    elif value_type == "Button":
        return 'bool'
    elif value_type == "Raw":
        return 'binary'
    else:
        return value_type


def change_instance(my_value):
    if my_value.instance > 1:
        return my_value.instance - 1
    return 0


def normalize_short_value(value):
    my_result = value
    # noinspection PyBroadException
    try:
        if int(value) < 0:
            my_result = 65536 + int(value)
    except:
        pass
    return my_result


def convert_fahrenheit_celsius(value):
    if value.precision is None or value.precision == 0:
        power = 1
    else:
        power = math.pow(10, value.precision)
    return int(((float(value.data_as_string) - 32) * 5.0 / 9.0) * int(power)) / power


def extract_data(value, display_raw=False, convert_fahrenheit=True):
    if value.type == "Bool":
        return value.data    
    elif value.label == 'Temperature' and value.units == 'F' and convert_fahrenheit:
        return convert_fahrenheit_celsius(value)
    elif value.type == "Raw":
        my_result = binascii.b2a_hex(value.data)
        if display_raw:
            add_log_entry('Raw Signal: %s' % my_result)
        return my_result
    if value.type == "Decimal":
        if value.precision is None or value.precision == 0:
            power = 1
        else:
            power = math.pow(10, value.precision)
        return int(value.data * int(power)) / power
    return value.data


def can_execute_network_command(allowed_queue_count=5):
    global _network
    if _network is None:
        return False
    if not _network.controller.is_primary_controller:
        return True
    if _network.controller.send_queue_count > allowed_queue_count:
        return False
    if _network_information.controller_is_busy:
        return False
    if _network_information.actual_mode != ControllerMode.Idle:
        return False
    if _network.state < _network.STATE_STARTED:
        return False
    return True


def write_config():  
    watchdog = 0
    while _network_information.config_file_save_in_progress and watchdog < 10:
        if _log_level == 'Debug':
            add_log_entry('.')
        time.sleep(1)
        watchdog += 1
    if _network_information.config_file_save_in_progress:
        return        
    _network_information.config_file_save_in_progress = True
    try:
        _network.write_config()
        add_log_entry('write configuration file')
        time.sleep(1)
    except Exception as error:
        add_log_entry('write_config %s' % (str(error),), "error")
    finally:
        _network_information.config_file_save_in_progress = False


def essential_node_queries_complete(network, node):   
    debug_print('The essential queries on a node have been completed. id:[%s] model:[%s].' % (node.node_id, node.product_name,))   
    my_node = network.nodes[node.node_id]
    my_node.last_update = time.time()
    # at this time is not good to save value, I skip this step


def node_queries_complete(network, node):
    add_log_entry('All the initialisation queries on a node have been completed. id:[%s] model:[%s].' % (node.node_id, node.product_name,))        
    node.last_update = time.time()
    # save config
    write_config()       


def save_value(node, value, last_update):
    # debug_print('A node value has been updated. nodeId:%s value:%s' % (node.node_id, value.label))
    if node.node_id in _network.nodes:
        my_node = _network.nodes[node.node_id]
        # check if am the really last update
        if my_node.last_update > last_update:
            return
        # mark as seen flag
        my_node.last_update = last_update
        # if value.genre != 'Basic':
        value.last_update = last_update
        save_node_value_event(node.node_id, int(time.time()), value.command_class, value.index, get_standard_value_type(value.type), extract_data(value, False), change_instance(value))    


def value_added(network, node, value):  
    if node.node_id in _not_supported_nodes:
        return
    # debug_print('value_added. %s %s' % (node.node_id, value.label,))
    # mark initial data for skip notification during interview
    value.lastData = value.data 


def value_polling_enabled(network, node, value):
    # not yet handle correctly ozw lib and wrapper must updated to use this check
    # check if old polling is outside authorized range
    if value.poll_intensity > _maximum_poll_intensity:
        changes_value_polling(_maximum_poll_intensity, value)
    # check if old polling is at lower index for CC and instance
    if value.poll_intensity > 0:
        debug_print('Poll intensity on nodeId:%s value %s command_class %s instance %s index %s' % (node.node_id, value.label, value.command_class, value.instance, value.index))
        # get all CC of node
        for val in node.get_values(class_id=value.command_class):
            # filter on same instance
            if node.values[val].instance == value.instance:
                my_value = node.values[val]
                # check is is the lower index is have polling attribute
                if my_value.index < value.index & my_value.poll_intensity == 0:
                    poll_intensity = value.poll_intensity
                    # reset last polling
                    value.disable_poll()
                    # set polling of lower index
                    changes_value_polling(poll_intensity, my_value)
                    debug_print('Changes poll intensity on nodeId:%s form %s to %s' % (node.node_id, value.label, my_value.label,))
                    break


def prepare_value_notification(node, value):
    if hasattr(value, 'pendingConfiguration'):
        if value.pendingConfiguration is not None:
            # mark result
            data = value.data
            if value.type == 'Short':
                data = normalize_short_value(value.data)
            value.pendingConfiguration.data = data
            
    if not node.is_ready:
        # check if have the attribute
        if hasattr(value, 'lastData') and value.lastData == value.data:
            # we skip notification to avoid value refresh during the interview process
            return
    # update for next run
    value.lastData = value.data    
    if value.genre == 'System':
        value.last_update = time.time()
        return
    command_class = _network.manager.COMMAND_CLASS_DESC[value.command_class].replace("COMMAND_CLASS_", "").replace("_", " ").lower().capitalize()
    debug_print("Received %s report from node %s: %s=%s%s" % (command_class, node.node_id, value.label, extract_data(value, False, False), value.units))
    thread = None
    try:
        save_value(node, value, time.time())
    except Exception as error:
        add_log_entry('prepare_value_notification %s' % (str(error), ), "error")
        if thread is not None:
            thread.stop()


def value_update(network, node, value): 
    if node.node_id in _not_supported_nodes:
        return
    # debug_print('value_update. %s %s' % (node.node_id, value.label,))
    prepare_value_notification(node, value)


def value_refreshed(network, node, value): 
    if node.node_id in _not_supported_nodes:
        return
    # debug_print('value_refreshed. %s %s' % (node.node_id, value.label,))
    value_update(network, node, value)


def scene_event(network, node, scene_id):
    add_log_entry('Scene Activation: %s' % (scene_id,))
    standard_type = 'int'
    save_node_value_event(node.node_id, int(time.time()), COMMAND_CLASS_CENTRAL_SCENE, 0, standard_type, scene_id, 0)
    save_node_value_event(node.node_id, int(time.time()), COMMAND_CLASS_SCENE_ACTIVATION, 0, standard_type, scene_id, 0)


def controller_message_complete(network):
    debug_print('The last message that was sent is now complete')


def controller_waiting(network, controller, state_int, state, state_full):
    debug_print(state_full)
    # save actual state
    _network_information.assign_controller_notification(state, state_full)
    # notify jeedom
    save_node_event(network.controller.node_id, _network_information.generate_jeedom_message())


def controller_command(network, controller, node, node_id, state_int, state, state_full, error_int, error, error_full):
    debug_print('%s (%s)' % (state_full, state))
    if error_int > 0:
        add_log_entry('%s (%s)' % (error_full, error,), "error")
    
    # save actual state
    _network_information.assign_controller_notification(state, state_full, error, error_full)
    # notify jeedom
    save_node_event(network.controller.node_id, _network_information.generate_jeedom_message())
    debug_print('Controller is busy: %s' % (_network_information.controller_is_busy,))


def node_event(network, node, value):
    debug_print('NodeId %s sends a Basic_Set command to the controller with value %s' % (node.node_id, value,)) 
    for val in network.nodes[node.node_id].get_values():
        my_value = network.nodes[node.node_id].values[val]
        if my_value.genre == "User" and not my_value.is_write_only:
            value_update(network, node, my_value)
    '''
    the value is actually the event data, not a zwave value object.
    This is commonly caused when a node sends a Basic_Set command to the controller.
    '''
    standard_type = 'int'
    save_node_value_event(node.node_id, int(time.time()), COMMAND_CLASS_BASIC, 0, standard_type, value, 0)


def node_group_changed(network, node):
    debug_print('Group changed for nodeId %s' % (node.node_id,)) 
    # TODO: reset group changed for pending associations
    validate_association_groups(node.node_id)


def get_wake_up_interval(node_id):
    interval = get_value_by_label(node_id, COMMAND_CLASS_WAKE_UP, 1, 'Wake-up Interval', False)
    if interval is not None:
        return interval.data
    return None


def force_sleeping(node_id, count=1):
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        debug_print('check if node %s still awake' % (node_id,))
        # check if still awake
        if my_node.is_awake or (hasattr(my_node, 'last_notification') and my_node.last_notification.code == 3):
            debug_print('trying to lull the node %s' % (node_id,))
            # a ping will force the node to return sleep after the NoOperation CC. Will force notification update too
            _network.manager.testNetworkNode(_network.home_id, node_id, count)


def node_notification(args):
    code = int(args['notificationCode'])
    node_id = int(args['nodeId'])
    if node_id in _not_supported_nodes:
        return
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        # mark as updated
        my_node.last_update = time.time()
        # try auto remove unsupported nodes
        if node_id in _not_supported_nodes and _network.state >= 7:   # STATE_AWAKE
            debug_print('remove fake nodeId: %s' % (node_id,))
            _network.manager.removeFailedNode(_network.home_id, node_id)
            return
        
        wake_up_time = get_wake_up_interval(node_id)
        if not hasattr(my_node, 'last_notification'):
            my_node.last_notification = NodeNotification(code, wake_up_time)
        else:
            # I refresh notification, the wake up time can be modified from last time, we need to calculate the next expected wake up time
            my_node.last_notification.refresh(code, wake_up_time)
        if code == 3: 
            # get the device Wake-up Interval Step
            my_value = get_value_by_label(node_id, COMMAND_CLASS_WAKE_UP, 1, 'Wake-up Interval Step', False)
            if my_value is not None:
                # add 2 seconds at device Wake-up Interval Step
                wake_up_interval_step = my_value.data + 2.0
            else:
                # assume a default Wake-up Interval Step     
                wake_up_interval_step = 60.0
            # perform a ping to avoid device still awake after the Wake-up Interval Step
            threading.Timer(interval=wake_up_interval_step, function=force_sleeping, args=(node_id, 1)).start()
        debug_print('NodeId %s send a notification: %s' % (node_id, my_node.last_notification.description,))
        push_node_notification(node_id, code)

app = Flask(__name__, static_url_path='/static')

# Create a network object
# noinspection PyRedeclaration
_network = ZWaveNetwork(options, autostart=False)

# We connect to the louie dispatcher
dispatcher.connect(network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
dispatcher.connect(network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(network_failed, ZWaveNetwork.SIGNAL_DRIVER_FAILED)
dispatcher.connect(network_awaked, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
dispatcher.connect(network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

start_network()

# a new node has been found (not already stored in zwcfg*.xml file).
dispatcher.connect(node_new, ZWaveNetwork.SIGNAL_NODE_NEW)
# add node to the network, during node discovering and after a inclusion
dispatcher.connect(node_added, ZWaveNetwork.SIGNAL_NODE_ADDED)
# a node is fully removed from network.
dispatcher.connect(node_removed, ZWaveNetwork.SIGNAL_NODE_REMOVED)
# value is add, changed or is refreshed.

# A new node value has been added to OpenZWave's list. 
# These notifications occur after a node has been discovered, and details of its command classes have been received. 
# Each command class may generate one or more values depending on the complexity of the item being represented.
dispatcher.connect(value_added, ZWaveNetwork.SIGNAL_VALUE_ADDED)
# A node value has been updated from the Z-Wave network and it is different from the previous value.
dispatcher.connect(value_update, ZWaveNetwork.SIGNAL_VALUE_CHANGED)
# A node value has been updated from the Z-Wave network.
dispatcher.connect(value_refreshed, ZWaveNetwork.SIGNAL_VALUE_REFRESHED)
# Polling of a node value has been successfully turned on.
# dispatcher.connect(value_polling_enabled, ZWaveNetwork.SIGNAL_POLLING_ENABLED)
# when a node sends a Basic_Set command to the controller.
dispatcher.connect(node_event, ZWaveNetwork.SIGNAL_NODE_EVENT)
# scene event
dispatcher.connect(scene_event, ZWaveNetwork.SIGNAL_SCENE_EVENT)
# the essential node query are completed
dispatcher.connect(essential_node_queries_complete, ZWaveNetwork.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE)
# all node query are completed, the node is fully operational, is ready!
dispatcher.connect(node_queries_complete, ZWaveNetwork.SIGNAL_NODE_QUERIES_COMPLETE)
# is network notification same as SIGNAL_NETWORK_AWAKE, we don't need
dispatcher.connect(nodes_queried, ZWaveNetwork.SIGNAL_AWAKE_NODES_QUERIED)
# is network notification same as SIGNAL_NETWORK_READY, we don't need
dispatcher.connect(nodes_queried, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED)

dispatcher.connect(nodes_queried_some_dead, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD)
# a button is pressed
dispatcher.connect(button_on, ZWaveNetwork.SIGNAL_BUTTON_ON)
dispatcher.connect(button_off, ZWaveNetwork.SIGNAL_BUTTON_OFF)

# Called when an error happened, or node changed (awake, sleep, death, no operation, timeout).
dispatcher.connect(node_notification, ZWaveNetwork.SIGNAL_NOTIFICATION)

# Controller is waiting for a user action
dispatcher.connect(controller_waiting, ZWaveNetwork.SIGNAL_CONTROLLER_WAITING)
# keep a track of actual network command in progress
dispatcher.connect(controller_command, ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND)
# The command has completed successfully
dispatcher.connect(controller_message_complete, ZWaveNetwork.SIGNAL_MSG_COMPLETE)

add_log_entry('OpenZwave Library Version %s' % (_network.manager.getOzwLibraryVersionNumber(),))
add_log_entry('Python-OpenZwave Wrapper Version %s' % (_network.manager.getPythonLibraryVersionNumber(),))

# We wait for the network.
add_log_entry('Waiting for network to become ready')


def get_value_by_label(node_id, command_class, instance, label, trace=True):
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        for value_id in my_node.get_values(class_id=command_class):
            if my_node.values[value_id].instance == instance and my_node.values[value_id].label == label:
                return my_node.values[value_id]
    if trace:
        debug_print("get_value_by_label Value not found for node_id:%s, cc:%s, instance:%s, label:%s" % (node_id, command_class, instance, label,))
    return None


def get_value_by_index(node_id, command_class, instance, index_id, trace=True):
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        for value_id in my_node.get_values(class_id=command_class):
            if my_node.values[value_id].instance == instance and my_node.values[value_id].index == index_id:
                return my_node.values[value_id]
    if trace:
        debug_print("get_value_by_index Value not found for node_id:%s, cc:%s, instance:%s, index:%s" % (node_id, command_class, instance, index_id,))
    return None


def get_value_by_id(node_id, value_id):
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        if value_id in my_node.values:
            return my_node.values[value_id]
    debug_print("get_value_by_id Value not found for node_id:%s, value_id:%s" % (node_id, value_id,))
    return None


def mark_pending_change(my_value, data, wake_up_time=0):
    if my_value is not None and not my_value.is_write_only:
        my_value.pendingConfiguration = PendingConfiguration(data, wake_up_time)


def build_network_busy_message():
    return format_json_result(False, 'Controller is too busy', _network_information.generate_jeedom_message())


def concatenate_list(list_values, separator=';'):
    try:
        if list_values is None:
            return ""
        else:
            if isinstance(list_values, set):
                return separator.join(str(s) for s in list_values)
            return list_values
    except Exception as error:
        add_log_entry(str(error), "error")
    return ""


def convert_query_stage_to_int(stage):    
    if stage == "None":
        return 0
    elif stage == "ProtocolInfo":
        return 1
    elif stage == "Probe":
        return 2
    elif stage == "WakeUp":
        return 3
    elif stage == "ManufacturerSpecific1":
        return 4
    elif stage == "NodeInfo":
        return 5
    elif stage == "SecurityReport":
        return 6
    elif stage == "ManufacturerSpecific2":
        return 7
    elif stage == "Versions":
        return 8
    elif stage == "Instances":
        return 9
    elif stage == "Static":
        return 10
    elif stage == "Probe1":
        return 11
    elif stage == "Associations":
        return 12
    elif stage == "Neighbors":
        return 13
    elif stage == "Session":
        return 14
    elif stage == "Dynamic":
        return 15
    elif stage == "Configuration":
        return 16
    elif stage == "Complete":
        return 17
    return 0 


def serialize_neighbour_to_json(node_id):
    json_result = {}
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        json_result['data'] = {}
        json_result['data']['product_name'] = {'value': my_node.product_name}
        json_result['data']['location'] = {'value': my_node.location}
        node_name = my_node.name
        if _network.controller.node_id == node_id:
            node_name = my_node.product_name
        if is_none_or_empty(node_name):
            node_name = my_node.product_name
        if is_none_or_empty(node_name):
            node_name = 'Unknown'
        json_result['data']['name'] = {'value': node_name}
        json_result['data']['neighbours'] = {'value': list(my_node.neighbors), 'enabled': my_node.generic != 1}
        json_result['data']['isDead'] = {'value': my_node.is_failed}
        if _network.controller.node_id == node_id and my_node.basic == 1:
            json_result['data']['basicType'] = {'value': 2}
        else:
            json_result['data']['basicType'] = {'value': my_node.basic}
        json_result['data']['genericType'] = {'value': my_node.generic}
        json_result['data']['specificType'] = {'value': my_node.specific}
        json_result['data']['type'] = {'value': my_node.type}
        json_result['data']['state'] = {'value': convert_query_stage_to_int(my_node.query_stage)}
        json_result['data']['isListening'] = {'value': my_node.is_listening_device}
        json_result['data']['isRouting'] = {'value': my_node.is_routing_device}
        
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return json_result


def validate_association_groups(node_id):
    fake_found = False
    if _network is not None and _network.state >= 7:
        if node_id in _network.nodes:
            my_node = _network.nodes[node_id]
            query_stage_index = convert_query_stage_to_int(my_node.query_stage)
            if query_stage_index >= 12:
                debug_print("validate_association_groups for nodeId: %s" % (node_id,))
                for group_index in list(my_node.groups):
                    group = my_node.groups[group_index]
                    for target_node_id in list(group.associations):
                        if target_node_id in _network.nodes and target_node_id not in _not_supported_nodes:
                            continue
                        debug_print("Remove association for nodeId: %s index %s with not exist target: %s" % (node_id, group_index, target_node_id,))
                        _network.manager.removeAssociation(_network.home_id, node_id, group_index, target_node_id)
                        fake_found = True
    return fake_found


def serialize_node_to_json(node_id):
    json_result = {}
    if node_id in _not_supported_nodes:
        return json_result
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        try:
            timestamp = int(my_node.last_update)
        except TypeError:
            timestamp = int(1)
        try:
            manufacturer_id = int(my_node.manufacturer_id, 16)
        except ValueError:
            manufacturer_id = None
        try:
            product_id = int(my_node.product_id, 16)
        except ValueError:
            product_id = None
        try:
            product_type = int(my_node.product_type, 16)
        except ValueError:
            product_type = None
                    
        json_result['data'] = {}
        json_result['data']['manufacturerId'] = {'value': manufacturer_id, 'hex': my_node.manufacturer_id}
        json_result['data']['vendorString'] = {'value': my_node.manufacturer_name}
        json_result['data']['manufacturerProductId'] = {'value': product_id, 'hex': my_node.product_id}
        json_result['data']['product_name'] = {'value': my_node.product_name}
        json_result['data']['location'] = {'value': my_node.location}
        json_result['data']['name'] = {'value': my_node.name}
        json_result['data']['version'] = {'value': my_node.version}
        json_result['data']['manufacturerProductType'] = {'value': product_type, 'hex': my_node.product_type}
        json_result['data']['neighbours'] = {'value': list(my_node.neighbors)}
        json_result['data']['isVirtual'] = {'value': ''}
        if _network.controller.node_id == node_id and my_node.basic == 1:
            json_result['data']['basicType'] = {'value': 2}
        else:
            json_result['data']['basicType'] = {'value': my_node.basic}
        json_result['data']['genericType'] = {'value': my_node.generic}
        json_result['data']['specificType'] = {'value': my_node.specific}
        json_result['data']['type'] = {'value': my_node.type}
        json_result['data']['state'] = {'value': str(my_node.query_stage)}
        json_result['data']['isAwake'] = {'value': my_node.is_awake, "updateTime": timestamp}
        json_result['data']['isReady'] = {'value': my_node.is_ready, "updateTime": timestamp}
        json_result['data']['isInfoReceived'] = {'value': my_node.is_info_received}
             
        json_result['data']['can_wake_up'] = {'value': my_node.can_wake_up()}
        json_result['data']['battery_level'] = {'value': my_node.get_battery_level()}
        json_result['data']['isFailed'] = {'value': my_node.is_failed}
        json_result['data']['isListening'] = {'value': my_node.is_listening_device}
        json_result['data']['isRouting'] = {'value': my_node.is_routing_device}
        json_result['data']['isSecurity'] = {'value': my_node.is_security_device}
        json_result['data']['isBeaming'] = {'value': my_node.is_beaming_device}
        json_result['data']['isFrequentListening'] = {'value': my_node.is_frequent_listening_device}
        json_result['data']['security'] = {'value': my_node.security}
        json_result['data']['lastReceived'] = {'updateTime': timestamp}
        json_result['data']['maxBaudRate'] = {'value': my_node.max_baud_rate}
        
        json_result['instances'] = {"updateTime": timestamp}
        json_result['groups'] = {"updateTime": timestamp}
        for groupIndex in list(my_node.groups):
            group = my_node.groups[groupIndex]
            json_result['groups'][groupIndex] = {"label": group.label, "maximumAssociations": group.max_associations, "associations": concatenate_list(group.associations)}
        if hasattr(my_node, 'last_notification'):
            notification = my_node.last_notification
            json_result['last_notification'] = {"receiveTime": notification.receive_time,
                                                "code": notification.code,
                                                "description": notification.description,
                                                "help": notification.help,
                                                "next_wakeup": notification.next_wake_up
                                                }
        else:
            json_result['last_notification'] = {}
            
        json_result['command_classes'] = {}
        for command_class in my_node.command_classes:
            json_result['command_classes'][command_class] = {'name': my_node.get_command_class_as_string(command_class), 'hex': '0x' + convert_user_code_to_hex(command_class)}
            
        for val in my_node.get_values():
            my_value = my_node.values[val]
            if my_value.genre != 'Basic':
                standard_type = get_standard_value_type(my_value.type)
            else:
                standard_type = 'int'

            if my_value.is_write_only:
                value2 = None
            else:
                if my_value.type == 'Short':
                    value2 = normalize_short_value(my_value.data)
                else:
                    value2 = extract_data(my_value)
            if my_value.label == 'Temperature' and my_value.units == 'F':
                value_units = 'C'
            else:
                value_units = my_value.units
            instance2 = change_instance(my_value)
            if my_value.index:
                index2 = my_value.index
            else:
                index2 = 0            
            pending_state = None
            expected_data = None
            data_items = concatenate_list(my_value.data_items)
            if hasattr(my_value, 'pendingConfiguration'):
                if my_value.pendingConfiguration is not None:
                    pending_state = my_value.pendingConfiguration.state
                    expected_data = my_value.pendingConfiguration.expected_data
            try:
                timestamp = int(my_value.last_update)
            except TypeError:
                timestamp = int(1)
            
            if my_value.command_class is None:
                continue    
            if instance2 not in json_result['instances']:
                json_result['instances'][instance2] = {"updateTime": timestamp}
                json_result['instances'][instance2]['commandClasses'] = {"updateTime": timestamp}
                json_result['instances'][instance2]['commandClasses']['data'] = {"updateTime": timestamp}
                json_result['instances'][instance2]['commandClasses'][my_value.command_class] = {"name": my_node.get_command_class_as_string(my_value.command_class)}
                json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data'] = {"updateTime": timestamp}
                if not my_node.is_ready:
                    json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']['interviewDone'] = {}
                if my_value.command_class in [COMMAND_CLASS_BATTERY]:
                    json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']['supported'] = {"value": True, "type": "bool", "updateTime": timestamp}
                    json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']['last'] = {"value": value2, "type": "int", "updateTime": timestamp}
                if my_value.command_class in [COMMAND_CLASS_WAKE_UP]:
                    json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']['interval'] = {"value": value2, "type": "int", "updateTime": timestamp}
                json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data'][index2] = {"val": value2, "name": my_value.label, "help": my_value.help, "type": standard_type, "typeZW": my_value.type, "units": value_units, "data_items": data_items, "read_only": my_value.is_read_only, "write_only": my_value.is_write_only, "updateTime": timestamp, "genre": my_value.genre, "value_id": my_value.value_id, "poll_intensity": my_value.poll_intensity, "pendingState": pending_state, "expected_data": expected_data}
                
            elif my_value.command_class not in json_result['instances'][instance2]['commandClasses']:
                json_result['instances'][instance2]['commandClasses'][my_value.command_class] = {"updateTime": timestamp}
                json_result['instances'][instance2]['commandClasses'][my_value.command_class] = {"name": my_node.get_command_class_as_string(my_value.command_class)}
                json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data'] = {"updateTime": timestamp}
                if not my_node.is_ready:
                    json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']['interviewDone'] = {}
                if my_value.command_class in [COMMAND_CLASS_BATTERY]:
                    json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']['supported'] = {"value": True, "type": "bool", "updateTime": timestamp}
                    json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']['last'] = {"value": value2, "type": "int", "updateTime": timestamp}
                if my_value.command_class in [COMMAND_CLASS_WAKE_UP]:
                    json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']['interval'] = {"value": value2, "type": "int", "updateTime": timestamp}
                json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data'][index2] = {"val": value2, "name": my_value.label, "help": my_value.help, "type": standard_type, "typeZW": my_value.type, "units": value_units, "data_items": data_items, "read_only": my_value.is_read_only, "write_only": my_value.is_write_only, "updateTime": timestamp, "genre": my_value.genre, "value_id": my_value.value_id, "poll_intensity": my_value.poll_intensity, "pendingState": pending_state, "expected_data": expected_data}
                
            elif index2 not in json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']:
                if my_value.command_class in [COMMAND_CLASS_BATTERY]:
                    json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']['supported'] = {"value": True, "type": "bool", "updateTime": timestamp}
                    json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']['last'] = {"value": value2, "type": "int", "updateTime": timestamp}
                if my_value.command_class in [COMMAND_CLASS_WAKE_UP]:
                    json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']['interval'] = {"value": value2, "type": "int", "updateTime": timestamp}
                json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data'][index2] = {"val": value2, "name": my_value.label, "help": my_value.help, "type": standard_type, "typeZW": my_value.type, "units": value_units, "data_items": data_items, "read_only": my_value.is_read_only, "write_only": my_value.is_write_only, "updateTime": timestamp, "genre": my_value.genre, "value_id": my_value.value_id, "poll_intensity": my_value.poll_intensity, "pendingState": pending_state, "expected_data": expected_data}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return json_result


def serialize_node_health(node_id):
    json_result = {}
    if node_id in _not_supported_nodes:
        return json_result
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        if my_node.basic == 2:  # STATIC_CONTROLLER   = 0x02
            return json_result
        try:
            timestamp = int(my_node.last_update)
        except TypeError:
            timestamp = int(1)
        query_stage_index = convert_query_stage_to_int(my_node.query_stage)
        json_result['data'] = {}
        node_name = my_node.name
        if _network.controller.node_id == node_id:
            node_name = my_node.product_name
        if is_none_or_empty(node_name):
            node_name = 'Unknown'
        json_result['data']['description'] = {'name': node_name, 'location': my_node.location, 'product_name': my_node.product_name}
        json_result['data']['type'] = {'basic': my_node.basic, 'generic': my_node.generic}
        json_result['data']['state'] = {'value': my_node.query_stage, 'index': query_stage_index}
        json_result['data']['isAwake'] = {'value': my_node.is_awake}
        json_result['data']['isReady'] = {'value': my_node.is_ready}
        try:            
            can_wake_up = my_node.can_wake_up()
        except RuntimeError:
            can_wake_up = False               
        json_result['data']['can_wake_up'] = {'value': can_wake_up}
        battery_level_data = None
        battery_level_last_update = None
        try:            
            battery_level = get_value_by_index(node_id, COMMAND_CLASS_BATTERY, 1, 0, False)
            if battery_level is not None:
                battery_level_data = battery_level.data
                battery_level_last_update = battery_level.last_update            
        except RuntimeError:
            pass
        json_result['data']['battery_level'] = {'value': battery_level_data, 'updateTime': battery_level_last_update}
        next_wake_up = None
        if hasattr(my_node, 'last_notification'):
            notification = my_node.last_notification
            next_wake_up = notification.next_wake_up
            json_result['last_notification'] = {"receiveTime": notification.receive_time,
                                                "description": notification.description,
                                                "help": notification.help
                                                }
        else:
            json_result['last_notification'] = {}
        json_result['data']['wakeup_interval'] = {'value': get_wake_up_interval(node_id), 'next_wakeup': next_wake_up}
        json_result['data']['isFailed'] = {'value': my_node.is_failed}
        json_result['data']['isListening'] = {'value': my_node.is_listening_device}
        json_result['data']['isRouting'] = {'value': my_node.is_routing_device}
        json_result['data']['isBeaming'] = {'value': my_node.is_beaming_device}
        json_result['data']['isFrequentListening'] = {'value': my_node.is_frequent_listening_device}
        json_result['data']['lastReceived'] = {'updateTime': timestamp}
        json_result['data']['maxBaudRate'] = {'value': my_node.max_baud_rate}
                        
        statistics = _network.manager.getNodeStatistics(_network.home_id, node_id)
        sent_ok = statistics['sentCnt']
        sent_failed = statistics['sentFailed']
        send_total = sent_ok + sent_failed
        if send_total > 0:
            percent_delivered = (sent_ok * 100) / send_total
        else:
            percent_delivered = 0            
        average_request_rtt = statistics['averageRequestRTT']
        json_result['data']['statistics'] = {'total': send_total, 'delivered': percent_delivered, 'deliveryTime': average_request_rtt}

        have_group = False
        if my_node.groups and query_stage_index >= 12 and my_node.generic != 2:
            check_for_group = len(my_node.groups) > 0
            for groupIndex in list(my_node.groups):
                if len(my_node.groups[groupIndex].associations) > 0:
                    have_group = True
                    break            
        else:
            check_for_group = False
        json_result['data']['is_groups_ok'] = {'value': have_group, 'enabled': check_for_group}
        is_neighbours_ok = query_stage_index > 13
        if my_node.generic == 1:
            is_neighbours_ok = False
        if my_node.generic == 8 and not my_node.is_listening_device:
            is_neighbours_ok = False
        json_result['data']['is_neighbours_ok'] = {'value': len(my_node.neighbors) > 0, 'neighbors': len(my_node.neighbors), 'enabled': is_neighbours_ok}
        json_result['data']['is_manufacturer_specific_ok'] = {'value': not is_none_or_empty(my_node.manufacturer_id) and not is_none_or_empty(my_node.product_id) and not is_none_or_empty(my_node.product_type), 'enabled': query_stage_index >= 7}  # ManufacturerSpecific2
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return json_result


def get_network_mode():
    """
    if the controller is flag as busy I set the corresponding networkInformation.controllerState,
    if not yet busy, I ignore the actual ControllerMode and assume is idle
    """
    if _network_information.controller_is_busy:
        if _network_information.actual_mode == ControllerMode.AddDevice:
            return AddDevice
        elif _network_information.actual_mode == ControllerMode.RemoveDevice:
            return RemoveDevice
        else:
            return Idle
    else:
        return Idle


def serialize_controller_to_json():    
    json_result = {'data': {}}
    json_result['data']['roles'] = {'isPrimaryController': _network.controller.is_primary_controller,
                                    'isStaticUpdateController': _network.controller.is_static_update_controller,
                                    'isBridgeController': _network.controller.is_bridge_controller
                                    }
    json_result['data']['nodeId'] = {'value': _network.controller.node_id}
    json_result['data']['mode'] = {'value': get_network_mode()}
    json_result['data']['softwareVersion'] = {'ozw_library': _network.controller.ozw_library_version, 'python_library': _network.controller.python_library_version}
    json_result['data']['notification'] = _network_information.last_controller_notification
    json_result['data']['isBusy'] = {"value": _network_information.controller_is_busy}
    json_result['data']['networkstate'] = {"value": _network.state}
    return json_result


def changes_value_polling(intensity, value):
    if intensity == 0:  # disable the value polling for any value
        if value.poll_intensity > 0:
            value.disable_poll()
    elif value.genre == "User" and not value.is_write_only:  # we activate the value polling only on user genre value and is not a writeOnly
        if intensity > _maximum_poll_intensity:
            intensity = _maximum_poll_intensity
        value.enable_poll(intensity)


def convert_user_code_to_hex(value, length=2):
    value1 = int(value)
    my_result = hex(value1)[length:]
    if len(my_result) == 1:
        my_result = '0' * (length - 1) + my_result
    return my_result


def set_value(node_id, value_id, data):
    debug_print("set a value for nodeId:%s valueId:%s data:%s" % (node_id, value_id, data,))
    # check for a valid node_id
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        if not my_node.is_ready:
            return format_json_result(False, 'The node must be Ready') 
        for value in my_node.get_values():
            if value == value_id:
                zwave_value = my_node.values[value]
                # cast data in desired type
                data = zwave_value.check_data(data=data)
                if data is None:
                    return jsonify({'result': False, 'reason': 'cant convert in desired dataType'})
                my_result = _network.manager.setValue(zwave_value.value_id, data)
                if my_result == 0:
                    result_message = 'fails'
                elif my_result == 1:
                    result_message = 'succeed'
                elif my_result == 2:
                    result_message = 'fails (valueId not exist)'
                else:
                    result_message = 'fails (unknown error)'
                if my_result == 1:
                    return format_json_result()                    
                return format_json_result(False, result_message)
        return format_json_result(False, 'valueId not exist')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')

refresh_workers = {}


def create_worker(node_id, value_id, target_value, starting_value, counter):
    # create a new refresh worker
    worker = threading.Timer(interval=_refresh_interval, function=refresh_background, args=(node_id, value_id, target_value, starting_value, counter))
    # save worker
    refresh_workers[value_id] = worker
    # start refresh timer
    worker.start() 


def prepare_refresh(node_id, value_id, target_value=None):
    # debug_print("prepare_refresh for nodeId:%s valueId:%s data:%s" % (node_id, value_id, target_value,))
    stop_refresh(node_id, value_id)
    starting_value = _network.nodes[node_id].values[value_id].data
    create_worker(node_id, value_id, target_value, starting_value, 0)
    _network.nodes[node_id].values[value_id].start_refresh_time = int(time.time())


def refresh_background(node_id, value_id, target_value, starting_value, counter):
    do_refresh = True
    actual_value = _network.nodes[node_id].values[value_id].data
    if target_value is not None:
        if isinstance(target_value, basestring):
            # color CC test
            do_refresh = actual_value != target_value
            # debug_print("delta %s: %s" % (actual_value, target_value,))
        else:
            # check if target is reported
            delta = abs(actual_value - target_value)
            # debug_print("delta for nodeId:%s valueId:%s is: %s" % (node_id, value_id, delta,))
            if delta < 2:
                # if delta is too small don't refresh
                do_refresh = False
                # debug_print("delta is too small don't refresh")
    if do_refresh:
        # debug_print("check for changes, actual: %s , starting: %s (retry %s)" % (actual_value, starting_value, counter,))
        # check if won't changes
        if starting_value == actual_value:
            counter += 1
            if counter > 3:
                do_refresh = False
        else:
            counter = 0                
    if do_refresh:
        # debug_print("refresh")
        _network.nodes[node_id].values[value_id].refresh()
        # check if someone stop this refresh or we reach the timeout
        timeout = int(time.time()) - _network.nodes[node_id].values[value_id].start_refresh_time
        if timeout < _refresh_timeout:
            # I will start again a refresh timer
            create_worker(node_id, value_id, target_value, starting_value, counter)
    else:
        # remove worker the flag is set
        del refresh_workers[value_id]


def stop_refresh(node_id, value_id):
    # check if for a existing worker
    worker = refresh_workers.get(value_id)
    if worker is not None:
        # debug_print("Stop the timer")
        # Stop the timer, and cancel the execution of the timer action. This will only work if the timer is still in its waiting stage.
        worker.cancel()
        # remove worker
        del refresh_workers[value_id]
    # reset start time if refresh is running to avoid start again
    _network.nodes[node_id].values[value_id].start_refresh_time = 0


def get_sleeping_nodes_count():
    sleeping_nodes_count = 0
    for idNode in list(_network.nodes):
        if not _network.nodes[idNode].is_awake:
            sleeping_nodes_count += 1
    return sleeping_nodes_count  


def convert_level_to_color(level):
    if level > 99:
        return 255
    return level * 255 / 99


def convert_color_to_level(color):
    if color > 255:
        color = 255
    if color < 0:
        color = 0
    return color * 99 / 255


def is_none_or_empty(value):
    if value is None:
        return True
    if value:
        return False
    else:
        return True


def format_json_result(success=True, detail=None, log_level=None, code=0):
    if log_level is not None and not is_none_or_empty(detail):
        add_log_entry(detail, log_level)
    if detail is not None:
        return jsonify({'result': success, 'data': detail, 'code': code})
    return jsonify({'result': success}) 

'''
default routes
'''


@app.before_first_request
def _run_on_start():    
    pass


@app.route('/', methods=['GET'])
def default_index():
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'index.html')), 'rb') as f:
        content = f.read()
    return content


@app.errorhandler(400)
def not_found400(error):
    add_log_entry('%s %s' % (error, request.url), "error")
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found404(error):
    add_log_entry('%s %s' % (error, request.url), "error") 
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def close_network(error):
    return error

'''
devices routes
'''


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[133].Get()', methods=['GET'])
def refresh_assoc(node_id):
    debug_print("refresh_assoc for nodeId: %s" % (node_id,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=COMMAND_CLASS_ASSOCIATION):
            _network.nodes[node_id].values[val].refresh()
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[133].data', methods=['GET'])
def get_assoc(node_id):
    debug_print("get_assoc for nodeId: %s" % (node_id,))
    timestamp = int(time.time())
    config = {}
    if node_id in _network.nodes:
        if _network.nodes[node_id].groups:
            config['supported'] = {'value': True}
            for group in list(_network.nodes[node_id].groups):
                config[_network.nodes[node_id].groups[group].index] = {}
                config[_network.nodes[node_id].groups[group].index]['nodes'] = {'value': list(_network.nodes[node_id].groups[group].associations), 'updateTime': int(timestamp), 'invalidateTime': 0}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return jsonify(config)


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0x85].Remove(<int:value>,<int:value2>)', methods=['GET'])
def remove_assoc(node_id, value, value2):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy') 
    group_index = value
    target_node_id = value2
    debug_print("remove_assoc to nodeId: %s in group %s with nodeId: %s" % (node_id, group_index, target_node_id,))
    if node_id in _network.nodes:
        _network.manager.removeAssociation(_network.home_id, node_id, group_index, target_node_id)
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0x85].Add(<int:value>,<int:value2>)', methods=['GET'])
def add_assoc(node_id, value, value2):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')   
    group_index = value
    target_node_id = value2
    debug_print("add_assoc to nodeId: %s in group %s with nodeId: %s" % (node_id, group_index, target_node_id,))
    if node_id in _network.nodes:
        _network.manager.addAssociation(_network.home_id, node_id, group_index, target_node_id)
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetPolling()', methods=['GET'])
def get_polling(node_id):
    polling = 0
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values():
            if _network.nodes[node_id].values[val].poll_intensity > polling:
                polling = _network.nodes[node_id].values[val].poll_intensity
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return str(polling)


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].ResetPolling()', methods=['GET'])
def reset_polling(node_id):
    debug_print("reset_polling for nodeId: %s" % (node_id,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values():
            my_value = _network.nodes[node_id].values[val]
            changes_value_polling(0, my_value)
        return format_json_result()  
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetPolling(<int:value_id>,<frequency>)', methods=['GET'])
def set_polling2(node_id, value_id, frequency):
    debug_print("set_polling for nodeId: %s ValueId %s at: %s" % (node_id, value_id, frequency,))
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        for val in my_node.get_values():
            my_value = my_node.values[val]
            if my_value.value_id == value_id:
                changes_value_polling(frequency, my_value)
                # reset other polling for this CC and instance
                for value_id in my_node.get_values(class_id=my_value.command_class):
                    if my_node.values[value_id].instance == my_value.instance and my_node.values[value_id].index != my_value.index_id:
                        changes_value_polling(0, value_id)
                return format_json_result()
        return format_json_result(False, 'valueId not found') 
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route(
    '/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].SetPolling(<int:frequency>)', methods=['GET'])
def set_polling_value(node_id, instance_id, cc_id, index, frequency):
    debug_print("set_polling_value for nodeId: %s instance: %s cc:%s index:%s at: %s" % (node_id, instance_id, cc_id, index, frequency,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=int(cc_id, 16)):
            if _network.nodes[node_id].values[val].instance - 1 == instance_id:
                my_value = _network.nodes[node_id].values[val]
                if frequency == 0 & my_value.poll_intensity > 0:
                    # disable the value polling for any values for this CC and instance
                    my_value.disable_poll()
                else:
                    if _network.nodes[node_id].values[val].index == index :
                        changes_value_polling(frequency, my_value)
                    else:
                        # disable the value polling for other index of same instance
                        if my_value.poll_intensity > 0:
                            my_value.disable_poll()
        write_config()  
        return format_json_result()      
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[132].data.interval.value', methods=['GET'])
def get_wake_up(node_id):
    if node_id in _network.nodes:
        return str(get_wake_up_interval(node_id))
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return str('')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetWakeup(<wake_up_time>)', methods=['GET'])
def set_wake_up(node_id, wake_up_time):
    debug_print("set wakeup interval for nodeId %s at: %s" % (node_id, wake_up_time,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=COMMAND_CLASS_WAKE_UP):
            my_value = _network.nodes[node_id].values[val]
            # we need to find the right valueId
            if my_value.label == "Wake-up Interval":
                return format_json_result(set_value(node_id, my_value.value_id, int(wake_up_time)))
        return format_json_result(False, 'Wake-up Interval not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].SetChangeVerified(<int:index>,<int:verified>)', methods=['GET'])
def set_change_verified(node_id, instance_id, cc_id, index, verified):
    # Sets a flag indicating whether value changes noted upon a refresh should be verified
    debug_print("set_change_verified nodeId:%s instance:%s commandClasses:%s index:%s verified:%s" % (node_id, instance_id, cc_id, index, verified,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=int(cc_id, 16)):
            my_value = _network.nodes[node_id].values[val]
            if my_value.instance - 1 == instance_id and my_value.index == index:
                _network.manager.setChangeVerified(my_value.value_id, bool(verified))
                return format_json_result()
        return format_json_result(False, 'value not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Refresh()', methods=['GET'])
def request_all_config_params(node_id):
    # Request the values of all known configurable parameters from a device
    debug_print("Request the values of all known configurable parameters from nodeId %s" % (node_id,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION):
            configuration_item = _network.nodes[node_id].values[val]
            if hasattr(configuration_item, 'pendingConfiguration'):
                if configuration_item.pendingConfiguration is not None:
                    configuration_item.pendingConfiguration = None
        _network.manager.requestAllConfigParams(_network.home_id, node_id)
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Get(<int:index_id>)', methods=['GET'])
def refresh_config(node_id, index_id):
    debug_print("refresh_config for nodeId:%s index_id:%s" % (node_id, index_id,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION):
            if _network.nodes[node_id].values[val].index == index_id:
                _network.nodes[node_id].values[val].refresh()
        return format_json_result()  
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetDeviceName(<string:location>,<string:name>)', methods=['GET'])
def set_device_name(node_id, location, name):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')
    debug_print("setName for node_id:%s New Name ; '%s'" % (node_id, name,))
    if node_id in _network.nodes:
        name = name.encode('utf8')
        name = name.replace('+', ' ')
        _network.nodes[node_id].set_field('name', name)
        location = location.encode('utf8')
        location = location.replace('+', ' ')
        _network.nodes[node_id].set_field('location', location)
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].data', methods=['GET'])
def get_config(node_id):
    debug_print("get_config for nodeId:%s" % (node_id,))
    timestamp = int(time.time())
    config = {}
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].values:
            list_values = []
            if _network.nodes[node_id].values[val].command_class == COMMAND_CLASS_CONFIGURATION:
                config[_network.nodes[node_id].values[val].index] = {}
                if _network.nodes[node_id].values[val].type == "List":
                    result_data = _network.manager.getValueListSelectionNum(_network.nodes[node_id].values[val].value_id)
                    values = _network.nodes[node_id].values[val].data_items
                    for index_item, value_item in enumerate(values):
                        list_values.append(value_item)
                        if value_item == _network.nodes[node_id].values[val].data_as_string:
                            result_data = index_item
                elif _network.nodes[node_id].values[val].type == "Bool" and not _network.nodes[node_id].values[val].data:
                    result_data = 0
                elif _network.nodes[node_id].values[val].type == "Bool" and _network.nodes[node_id].values[val].data:
                    result_data = 1
                else:
                    result_data = _network.nodes[node_id].values[val].data
                config[_network.nodes[node_id].values[val].index]['val'] = {'value2': _network.nodes[node_id].values[val].data, 'value': result_data, 'value3': _network.nodes[node_id].values[val].label, 'value4': list_values, 'updateTime': int(timestamp), 'invalidateTime': 0}
                config[_network.nodes[node_id].values[val].index]['size'] = {'value': len(str(result_data))}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return jsonify(config)


@app.route('/ZWaveAPI/Run/devices[<int:source_id>].CopyConfigurations(<int:target_id>)', methods=['GET'])
def copy_configuration(source_id, target_id):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')
    debug_print("copy_configuration from source_id:%s to target_id:%s'" % (source_id, target_id,))
    items = 0
    if source_id in _network.nodes:
        if target_id in _network.nodes:
            source = _network.nodes[source_id]
            target = _network.nodes[target_id]
            if source.manufacturer_id == target.manufacturer_id and source.product_type == target.product_type and source.product_id == target.product_id:
                for val in source.get_values():
                    configuration_value = source.values[val]
                    if configuration_value.genre == 'Config':
                        if configuration_value.type == 'Button':
                            continue
                        if configuration_value.is_write_only:
                            continue                
                        try:
                            target_value = get_value_by_index(target_id, COMMAND_CLASS_CONFIGURATION, 1, configuration_value.index)
                            if target_value is not None:
                                if configuration_value.type == 'List':
                                    _network.manager.setValue(target_value.value_id, configuration_value.data)
                                    accepted = True
                                else:
                                    accepted = target.set_config_param(configuration_value.index, configuration_value.data)
                                if accepted:
                                    items += 1
                                    mark_pending_change(target_value, configuration_value.data)
                        except Exception as error:
                            add_log_entry('Copy configuration %s (index:%s): %s' % (configuration_value.label, configuration_value.index, str(error), ), "error")
                my_result = items != 0
            else:
                return format_json_result(False, 'The two nodes must be with same: manufacturer_id, product_type and product_id', 'warning')
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (target_id,), 'warning')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (source_id,), 'warning')            
    return jsonify({'result': my_result, 'copied_configuration_items': items})


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetConfigurationItem(<int:value_id>,<string:item>)', methods=['GET'])
def set_configuration_item(node_id, value_id, item):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')
    debug_print("set_configuration_item for node_id:%s change valueId:%s to '%s'" % (node_id, value_id, item,))
    if node_id in _network.nodes:
        my_result = _network.manager.setValue(node_id, value_id, item)
        if my_result:
            mark_pending_change(get_value_by_id(node_id, value_id), item)
        return format_json_result(my_result)
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<int:value>,<int:size>)', methods=['GET'])
def set_config(node_id, index_id, value, size):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')
    debug_print("set_config for nodeId:%s index:%s, value:%s, size:%s" % (node_id, index_id, value, size,))
    if size == 0:
        size = 2
    if size > 4:
        size = 4
    try:
        if node_id in _network.nodes:
            result = _network.nodes[node_id].set_config_param(index_id, value, size)
            my_value = get_value_by_index(node_id, COMMAND_CLASS_CONFIGURATION, 1, index_id, False)
            mark_pending_change(my_value, value)
            return format_json_result(result)
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<string:value>,<int:size>)', methods=['GET'])
def set_config2(node_id, index_id, value, size):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')
    debug_print("set_config2 for node_id:%s change index:%s to '%s' size:(%s)" % (node_id, index_id, value, size,))
    try:
        if node_id in _network.nodes:
            for value_id in _network.nodes[node_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION, genre='All', type='All', readonly='All', writeonly='All'):
                if _network.nodes[node_id].values[value_id].index == index_id:
                    value = value.replace("@", "/")
                    my_value = _network.nodes[node_id].values[value_id]
                    if my_value.type == 'Button':
                        if value.lower() == 'true':
                            _network.manager.pressButton(my_value.value_id)
                        else:
                            _network.manager.releaseButton(my_value.value_id)
                    elif my_value.type == 'List':
                        _network.manager.setValue(value_id, value)
                        mark_pending_change(my_value, value)
                    elif my_value.type == 'Bool':
                        if value.lower() == 'true':
                            value = True
                        else: 
                            value = False
                        _network.manager.setValue(value_id, value)
                        mark_pending_change(my_value, value)
                    return format_json_result()   
            return format_json_result(False, 'configuration parameter not found')
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<float:value>,<int:size>)', methods=['GET'])
def set_config3(node_id, index_id, value, size):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')
    debug_print("set_config3 for nodeId:%s index:%s, value:%s, size:%s" % (node_id, index_id, value, size,))
    if size == 0:
        size = 2
    value = int(value)
    try:
        if node_id in _network.nodes:
            result = _network.nodes[node_id].set_config_param(index_id, value, size)
            mark_pending_change(get_value_by_index(node_id, COMMAND_CLASS_CONFIGURATION, 1, index_id), value)
            return format_json_result(result)
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<int:value>,<int:size>)', methods=['GET'])
def set_config4(node_id, instance_id, index_id2, index_id, value, size):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')
    debug_print("set_config4 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (node_id, instance_id, index_id, value, size,))
    if size == 0:
        size = 2
    value = int(value)
    try:
        if node_id in _network.nodes:
            my_value = get_value_by_index(node_id, COMMAND_CLASS_CONFIGURATION, 1, index_id)
            _network.nodes[node_id].set_config_param(index_id, value, size)
            if my_value is not None and my_value.type != 'List':
                mark_pending_change(my_value, value)
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<string:value>,<int:size>)', methods=['GET'])
def set_config5(node_id, instance_id, index_id2, index_id, value, size):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')
    debug_print("set_config5 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (node_id, instance_id, index_id, value, size,))
    if size == 0:
        size = 2
    value = int(value)
    try:
        if node_id in _network.nodes:
            _network.nodes[node_id].set_config_param(index_id, value, size)
            mark_pending_change(get_value_by_index(node_id, COMMAND_CLASS_CONFIGURATION, 1, index_id), value)
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<float:value>,<int:size>)', methods=['GET'])
def set_config6(node_id, instance_id, index_id2, index_id, value, size):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')
    debug_print("set_config6 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (node_id, instance_id, index_id, value, size,))
    if size == 0:
        size = 2
    value = int(value)
    try:
        if node_id in _network.nodes:
            _network.nodes[node_id].set_config_param(index_id, value, size)
            mark_pending_change(get_value_by_index(node_id, COMMAND_CLASS_CONFIGURATION, 1, index_id), value)
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses', methods=['GET'])
def get_command_classes(node_id):
    my_result = {}
    debug_print("get_command_classes for nodeId:%s" % (node_id,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values():
            my_result[_network.nodes[node_id].values[val].command_class] = {}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return jsonify(my_result)


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RequestNodeDynamic()', methods=['GET'])
def request_node_dynamic(node_id):
    if node_id in _network.nodes:
        # Fetch only the dynamic command class data for a node from the Z-Wave network
        _network.manager.requestNodeDynamic(_network.home_id, node_id)
        # mark as updated to avoid a second pass
        _network.nodes[node_id].last_update = time.time()
        debug_print("Fetch the dynamic command class data for the node %s" % (node_id,))
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Get()', methods=['GET'])
def get_value(node_id, instance_id, cc_id):
    if node_id in _network.nodes:
        try:
            _network.nodes[node_id].last_update
        except NameError:
            _network.nodes[node_id].last_update = time.time()
        now = datetime.datetime.now()
        if isinstance(_network.nodes[node_id].last_update, float):
            last_update = datetime.datetime.fromtimestamp(_network.nodes[node_id].last_update)
        else:
            last_update = datetime.datetime.now()
            _network.nodes[node_id].last_update = time.time()
        last_delta = last_update + datetime.timedelta(seconds=30)
        # check last update is out of delta time, if the node is not a sleeping device and isReady
        if now > last_delta and _network.nodes[node_id].is_listening_device and _network.nodes[node_id].is_ready:
            # Fetch only the dynamic command class data for a node from the Z-Wave network
            _network.manager.requestNodeDynamic(_network.home_id, _network.nodes[node_id].node_id)
            # mark as updated to avoid a second pass
            _network.nodes[node_id].last_update = time.time()
            debug_print("Fetch the dynamic command class data for the node %s" % (node_id,))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    return format_json_result()


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].val', methods=['GET'])
def get_value6(node_id, instance_id, index, cc_id):
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=int(cc_id, 16)):
            if _network.nodes[node_id].values[val].instance - 1 == instance_id and _network.nodes[node_id].values[val].index == index:
                if _network.nodes[node_id].values[val].units == 'F':
                    return str(convert_fahrenheit_celsius(_network.nodes[node_id].values[val]))
                else:
                    return str(_network.nodes[node_id].values[val].data)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return jsonify({})


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].ForceRefresh()', methods=['GET'])
def force_refresh_one_value(node_id, instance_id, index, cc_id):
    return refresh_one_value(node_id, instance_id, index, int(cc_id, 16))


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<int:cc_id>].data[<int:index>].Refresh()', methods=['GET'])
def refresh_one_value(node_id, instance_id, index, cc_id):
    # debug_print("refresh_one_value nodeId:%s instance:%s commandClasses:%s index:%s" % (node_id, instance_id, cc_id, index))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=cc_id):
            if _network.nodes[node_id].values[val].instance - 1 == instance_id and _network.nodes[node_id].values[val].index == index:
                _network.nodes[node_id].values[val].refresh()
                return format_json_result()
        return format_json_result(False, 'This device does not contain the specified value', 'warning')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x63].data[<int:index>].code', methods=['GET'])
def get_user_code(node_id, instance_id, index):
    debug_print("getValueRaw nodeId:%s instance:%s commandClasses:%s index:%s" % (node_id, instance_id, hex(COMMAND_CLASS_USER_CODE), index))
    my_result = {}
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        for val in my_node.get_values(class_id=COMMAND_CLASS_USER_CODE):
            my_value = my_node.values[val]
            if my_value.instance - 1 == instance_id and my_value.index == index:
                user_code = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                timestamp = int(1)
                raw_data = extract_data(my_value)
                # debug_print("found a value: %s with data: (%s)" % (myValue.label, rawData,))
                if raw_data != '00000000000000000000':
                    try:
                        timestamp = int(my_value.last_update)
                        chunks, chunk_size = len(raw_data), len(raw_data) / 10
                        user_code = [int(raw_data[i:i + chunk_size], 16) for i in range(0, chunks, chunk_size)]
                    except TypeError:
                        timestamp = int(1)                 
                my_result = {'invalidateTime': int(time.time() - datetime.timedelta(seconds=30).total_seconds()),
                             'type': get_standard_value_type(my_value.type),
                             'value': user_code,
                             'updateTime': timestamp
                             }
                break
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return jsonify(my_result)


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x63].data', methods=['GET'])
def get_user_codes(node_id, instance_id):
    debug_print("getValueAllRaw nodeId:%s instance:%s commandClasses:%s" % (node_id, instance_id, hex(COMMAND_CLASS_USER_CODE),))
    result_value = {}
    if node_id in _network.nodes:
        my_node = _network.nodes[node_id]
        for val in my_node.get_values(class_id=COMMAND_CLASS_USER_CODE):
            my_value = my_node.values[val]
            if my_value.instance - 1 == instance_id:
                if my_value.index == 0:
                    continue
                if my_value.index > 10:
                    continue
                raw_data = extract_data(my_value)
                # debug_print("found a value: %s with data: (%s)" % (myValue.label, raw_data,))
                if raw_data == '00000000000000000000':
                    result_value[my_value.index] = None
                else:
                    result_value[my_value.index] = {}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return jsonify(result_value)


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].UserCode.SetRaw(<int:slot_id>,[<string:value>],1)', methods=['GET'])
def set_user_code(node_id, slot_id, value):
    debug_print("set_user_code nodeId:%s slot:%s user code:%s" % (node_id, slot_id, value,))
    result_value = {}
    for val in _network.nodes[node_id].get_values(class_id=COMMAND_CLASS_USER_CODE):
        if _network.nodes[node_id].values[val].index == slot_id:
            result_value['data'] = {}
            original_value = value
            value = binascii.a2b_hex(value)
            _network.nodes[node_id].values[val].data = value
            result_value['data'][val] = {'device': node_id, 'slot': slot_id, 'val': original_value}
            return jsonify(result_value)
    return jsonify(result_value)


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0x63].SetRaw(<int:slot_id>,[<value1>,<value2>,<value3>,<value4>,<value5>,<value6>,<value7>,<value8>,<value9>,<value10>],1)', methods=['GET'])
def set_user_code2(node_id, slot_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10):
    debug_print("set_user_code2 nodeId:%s slot:%s user code:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (node_id, slot_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10,))
    result_value = {}
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=COMMAND_CLASS_USER_CODE):
            if _network.nodes[node_id].values[val].index == slot_id:
                result_value['data'] = {}
                value = convert_user_code_to_hex(value1) + convert_user_code_to_hex(value2) + convert_user_code_to_hex(value3) + convert_user_code_to_hex(value4) + convert_user_code_to_hex(value5) + convert_user_code_to_hex(value6) + convert_user_code_to_hex(value7) + convert_user_code_to_hex(value8) + convert_user_code_to_hex(value9) + convert_user_code_to_hex(value10)
                original_value = value
                value = binascii.a2b_hex(value)
                _network.nodes[node_id].values[val].data = value
                result_value['data'][val] = {'device': node_id, 'slot': slot_id, 'val': original_value}
                return jsonify(result_value)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return jsonify(result_value)


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<int:value>)', methods=['GET'])
def set_value7(node_id, instance_id, cc_id, index, value):
    debug_print("set_value7 nodeId:%s instance:%s commandClasses:%s index:%s data:%s" % (node_id, instance_id, cc_id, index, value,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
            if _network.nodes[node_id].values[val].instance - 1 == instance_id and _network.nodes[node_id].values[val].index == index:
                _network.nodes[node_id].values[val].data = value
                if _network.nodes[node_id].values[val].genre == 'System':
                    if _network.nodes[node_id].values[val].type == 'Bool':
                        if value == 0:
                            value = False
                        else:
                            value = True                        
                    mark_pending_change(_network.nodes[node_id].values[val], value)
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                    # dimmer don't report the final value until the value changes is completed
                    prepare_refresh(node_id, val, value)
                return format_json_result()
        return format_json_result(False, 'value not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<float:value>)', methods=['GET'])
def set_value8(node_id, instance_id, cc_id, index, value):
    debug_print("set_value8 nodeId:%s instance:%s commandClasses:%s index:%s data:%s" % (node_id, instance_id, cc_id, index, value,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
            if _network.nodes[node_id].values[val].instance - 1 == instance_id and _network.nodes[node_id].values[val].index == index:
                _network.nodes[node_id].values[val].data = value
                if _network.nodes[node_id].values[val].genre == 'System':
                    mark_pending_change(_network.nodes[node_id].values[val], value)
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                    # dimmer don't report the final value until the value changes is completed
                    prepare_refresh(node_id, val, value)
                return format_json_result()
        return format_json_result(False, 'value not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<string:value>)', methods=['GET'])
def set_value9(node_id, instance_id, cc_id, index, value):
    debug_print("set_value9 nodeId:%s instance:%s commandClasses:%s index:%s data:%s" % (node_id, instance_id, cc_id, index, value,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
            if _network.nodes[node_id].values[val].instance - 1 == instance_id and _network.nodes[node_id].values[val].index == index:
                last_value = _network.nodes[node_id].values[val].data
                _network.nodes[node_id].values[val].data = value
                if _network.nodes[node_id].values[val].genre == 'System':
                    mark_pending_change(_network.nodes[node_id].values[val], value)
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                    # dimmer don't report the final value until the value changes is completed
                    prepare_refresh(node_id, val, value)
                if cc_id == hex(COMMAND_CLASS_COLOR):                       
                    if len(last_value) == 9 and len(value) > 9:
                        value = value[:9]     
                    prepare_refresh(node_id, val, value.upper())
                return format_json_result() 
        return format_json_result(False, 'value not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Set(<string:value>)', methods=['GET'])
def set_value6(node_id, instance_id, cc_id, value):
    debug_print("set_value6 nodeId:%s instance:%s commandClasses:%s  data:%s" % (node_id, instance_id, cc_id, value,))
    if cc_id == str(COMMAND_CLASS_WAKE_UP):
        # is a wake up interval update
        arr = value.split(",")
        wake_up_time = int(arr[0])
        return set_wake_up(node_id, wake_up_time)
    if node_id in _network.nodes:
        if cc_id == '0x85':
            # is a add association
            arr = value.split(",")
            group = int(arr[0])
            target_node = int(arr[1])
            try:
                return format_json_result(add_assoc(node_id, group, target_node))
            except ValueError:
                debug_print('Node not Ready for associations')
                return format_json_result(False, 'Node not Ready for associations')
        for val in _network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
            if _network.nodes[node_id].values[val].instance - 1 == instance_id:
                _network.nodes[node_id].values[val].data = value
                return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    return format_json_result(False, 'value not found')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetColor()', methods=['GET'])
def get_color(node_id):
    debug_print("get_color nodeId:%s" % (node_id,))
    my_result = {}
    if node_id in _network.nodes:
        red_level = 0  
        green_level = 0 
        blue_level = 0 
        white_level = 0
        for val in _network.nodes[node_id].get_values(class_id=COMMAND_CLASS_SWITCH_MULTILEVEL, genre='User', type='Byte', readonly='All', writeonly=False):
            my_value = _network.nodes[node_id].values[val]
            if my_value.label != 'Level':
                continue
            if my_value.instance < 2:
                continue            
            
            if my_value.instance == 3:
                red_level = convert_level_to_color(my_value.data)
            elif my_value.instance == 4:
                green_level = convert_level_to_color(my_value.data)
            elif my_value.instance == 5:
                blue_level = convert_level_to_color(my_value.data)
            elif my_value.instance == 6:
                white_level = convert_level_to_color(my_value.data) 
        my_result['data'] = {'red': red_level, 'green': green_level, 'blue': blue_level, 'white': white_level}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return jsonify(my_result)


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetColor(<int:red_level>,<int:green_level>,<int:blue_level>,<int:white_level>)', methods=['GET'])
def set_color(node_id, red_level, green_level, blue_level, white_level):
    debug_print("set_color nodeId:%s red:%s green:%s blue:%s white:%s" % (node_id, red_level, green_level, blue_level, white_level,))
    my_result = False
    if node_id in _network.nodes:
        intensity_value = None
        red_value = None
        green_value = None
        blue_value = None
        # white_value = None
        for val in _network.nodes[node_id].get_values(class_id=COMMAND_CLASS_SWITCH_MULTILEVEL, genre='User', type='Byte', readonly='All', writeonly=False):
            my_value = _network.nodes[node_id].values[val]
            if my_value.label != 'Level':
                continue
            if my_value.instance == 2:
                continue
            if my_value.instance == 1:
                intensity_value = val
            elif my_value.instance == 3:
                red_value = val
                my_value.data = convert_color_to_level(red_level)
            elif my_value.instance == 4:
                green_value = val
                my_value.data = convert_color_to_level(green_level)
            elif my_value.instance == 5:
                blue_value = val
                my_value.data = convert_color_to_level(blue_level)
            elif my_value.instance == 6:
                # white_value = val
                my_value.data = convert_color_to_level(white_level)
        if red_value is not None and green_value is not None and blue_value is not None:
            prepare_refresh(node_id, intensity_value, None)
            my_result = True
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    return format_json_result(my_result)


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].PressButton()', methods=['GET'])
def press_button(node_id, instance_id, cc_id, index):
    # Start an activity in a device
    debug_print("press_button nodeId:%s, instance:%s, cc:%s, index:%s" % (node_id, instance_id, cc_id, index,))
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
            if _network.nodes[node_id].values[val].instance - 1 == instance_id and _network.nodes[node_id].values[val].index == index:
                _network.manager.pressButton(_network.nodes[node_id].values[val].value_id)
                # special case for dimmer and store
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL) and _network.nodes[node_id].values[val].label in ['Bright', 'Dim', 'Open', 'Close']:
                    # assume Dim / Close as target value
                    value = 1
                    if _network.nodes[node_id].values[val].label in ['Bright', 'Open']:
                        value = 99
                    # dimmer don't report the final value until the value changes is completed
                    value_level = get_value_by_label(node_id, COMMAND_CLASS_SWITCH_MULTILEVEL, _network.nodes[node_id].values[val].instance, 'Level')
                    if value_level:
                        prepare_refresh(node_id, value_level.value_id, value)
                return format_json_result()
        return format_json_result(False, 'button not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].ReleaseButton()', methods=['GET'])
def release_button(node_id, instance_id, cc_id, index):
    # Stop an activity in a device
    if node_id in _network.nodes:
        for val in _network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
            if _network.nodes[node_id].values[val].instance - 1 == instance_id and _network.nodes[node_id].values[val].index == index:
                _network.manager.releaseButton(_network.nodes[node_id].values[val].value_id)
                # stop refresh if running in background
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                    value_level = get_value_by_label(node_id, COMMAND_CLASS_SWITCH_MULTILEVEL, _network.nodes[node_id].values[val].instance, 'Level')
                    if value_level:
                        stop_refresh(node_id, value_level.value_id)
                
                return format_json_result()
        return format_json_result(False, 'button not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].ToggleSwitch()', methods=['GET'])
def toggle_switch(node_id, instance_id, cc_id, index):
    if node_id in _network.nodes:
        if cc_id in [hex(COMMAND_CLASS_SWITCH_BINARY), hex(COMMAND_CLASS_SWITCH_MULTILEVEL)]:
            for val in _network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
                if _network.nodes[node_id].values[val].instance - 1 == instance_id and _network.nodes[node_id].values[val].index == index:
                    if cc_id == hex(COMMAND_CLASS_SWITCH_BINARY):
                        switch_state = _network.nodes[node_id].get_switch_state(val)
                        _network.nodes[node_id].set_switch(val, not switch_state)
                    if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                        switch_state = _network.nodes[node_id].values[val].data > 0
                        target_level = 0
                        if switch_state:
                            target_level = 0
                        else:
                            target_level = 255
                        _network.nodes[node_id].values[val].data = target_level
                        # dimmer don't report the final value until the value changes is completed
                        prepare_refresh(node_id, val, target_level)
                    return format_json_result(True, 'Switch as toggle, state is now %s' % (not switch_state,))
            return format_json_result(False, 'instance or index not found')
        else:
            return format_json_result(False, 'commandClass %s cant toggle' % (cc_id,))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0xF0].SwitchAll(<int:state>)', methods=['GET'])
def switch_all(node_id, state):
    # Method for switching all devices on or off together.  The devices must support
    # the SwitchAll command class.  The command is first broadcast to all nodes, and
    # then followed up with individual commands to each node (because broadcasts are
    # not routed, the message might not otherwise reach all the nodes).
    if state == 0:
        debug_print("SwitchAll Off")
        _network.switch_all(False)
    else:
        debug_print("SwitchAll On")
        _network.switch_all(True)
    return format_json_result()


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RequestNodeNeighbourUpdate()', methods=['GET'])
def request_node_neighbour_update(node_id):
    if not can_execute_network_command():
        return build_network_busy_message()  
    debug_print("request_node_neighbour_update for node %s" % (node_id,))
    if node_id in _network.nodes:
        return format_json_result(_network.manager.requestNodeNeighborUpdate(_network.home_id, node_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RemoveFailedNode()', methods=['GET'])
def remove_failed_node(node_id):
    # Removing the failed node from the controller's list.
    # This command cannot be cancelled.
    if not can_execute_network_command(0):
        return build_network_busy_message()  
    add_log_entry("Remove a failed node %s" % (node_id,))
    if node_id in _network.nodes:
        return format_json_result(_network.manager.removeFailedNode(_network.home_id, node_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].HealNode()', methods=['GET'])
def heal_node(node_id, perform_return_routes_initialization=False):
    # Heal a single node in the network
    if not can_execute_network_command():
        return build_network_busy_message()  
    try:
        add_log_entry("Heal network node (%s) by requesting the node rediscover their neighbors" % (node_id,))
        if node_id in _network.nodes:
            _network.manager.healNetworkNode(_network.home_id, node_id, perform_return_routes_initialization)
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].AssignReturnRoute()', methods=['GET'])
def assign_return_route(node_id):
    # Assign network routes to a device
    if not can_execute_network_command():
        return build_network_busy_message()  
    add_log_entry("Ask Node (%s) to update its Return Route to the Controller" % (node_id,))
    if node_id in _network.nodes:
        return format_json_result(_network.manager.assignReturnRoute(_network.home_id, node_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>]', methods=['GET'])
def get_serialized_device(node_id):
    if node_id in _network.nodes:
        return jsonify(serialize_node_to_json(node_id))
    else:
        add_log_entry('This network does not contain any node with the id %s' % (node_id,), 'warning')
    return jsonify({})             


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].ReplaceFailedNode()', methods=['GET'])
def replace_failed_node(node_id):
    # Replace a failed device with another. If the node is not in the controller failed nodes list, or the node responds, this command will fail.
    if not can_execute_network_command():
        return build_network_busy_message()  
    add_log_entry("replace_failed_node node %s" % (node_id,))
    if node_id in _network.nodes:
        return format_json_result(_network.manager.replaceFailedNode(_network.home_id, node_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SendNodeInformation()', methods=['GET'])
def send_node_information(node_id):
    # end a node information frame (NIF).
    if not can_execute_network_command():
        return build_network_busy_message()  
    debug_print("send_node_information node %s" % (node_id,))
    if node_id in _network.nodes:
        return format_json_result(_network.manager.sendNodeInformation(_network.home_id, node_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].HasNodeFailed()', methods=['GET'])
def has_node_failed(node_id):
    # Check whether a node is in the controller failed nodes list.
    if not can_execute_network_command():
        return build_network_busy_message()  
    add_log_entry("has_node_failed node %s" % (node_id,))
    if node_id in _network.nodes:
        return format_json_result(_network.manager.hasNodeFailed(_network.home_id, node_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RefreshNodeInfo()', methods=['GET'])
def refresh_node_info(node_id):
    # Trigger the fetching of fixed data about a node.
    # Causes the node data to be obtained from the Z-Wave network in the same way as if it had just been added.
    if not can_execute_network_command():
        return build_network_busy_message()  
    debug_print("refresh_node_info node %s" % (node_id,))
    if node_id in _network.nodes:
        return format_json_result(_network.manager.refreshNodeInfo(_network.home_id, node_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RefreshAllValues()', methods=['GET'])
def refresh_all_values(node_id):
    #  manual refresh of all value of a node, we will receive a refreshed value form value refresh notification
    if node_id in _network.nodes:
        current_node = _network.nodes[node_id]
        try:
            counter = 0
            debug_print("refresh_all_values node %s" % (node_id,))
            for val in current_node.get_values():
                current_value = current_node.values[val]
                if current_value.type == 'Button':
                    continue
                if current_value.is_write_only:
                    continue
                current_value.refresh()
                counter += 1
            message = 'Refreshed values count: %s' % (counter,)            
            return format_json_result(True, message)
        except Exception, exception:
            return format_json_result(False, str(exception), 'error')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].TestNode()', methods=['GET'])
def test_node(node_id=0, count=3):
    # Test network node.
    # Sends a series of messages to a network node for testing network reliability.
    if not can_execute_network_command():
        return build_network_busy_message()  
    try:
        debug_print("test_network node %s" % (node_id,))
        if node_id in _network.nodes:
            _network.manager.testNetworkNode(_network.home_id, node_id, count)
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetNodeStatistics()', methods=['GET'])
def get_node_statistics(node_id):
    # Retrieve statistics per node
    try:
        if node_id in _network.nodes:
            query_stage_description = _network.manager.getNodeQueryStage(_network.home_id, node_id)
            query_stage_code = _network.manager.getNodeQueryStageCode(query_stage_description)
            return jsonify({'statistics': _network.manager.getNodeStatistics(_network.home_id, node_id),
                            'queryStageCode': query_stage_code,
                            'queryStageDescription': query_stage_description
                            })
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (node_id,), 'warning')
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RemoveDeviceZWConfig()', methods=['GET'])
def remove_device_openzwave_config(node_id):
    # Remove a device from the openzwave config file and restart network to rediscover again
    # ensure load latest file version
    global _data_folder
    try:
        _network.stop()
        add_log_entry('ZWave network is now stopped')
        time.sleep(5)
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')
    filename = _data_folder + "/zwcfg_" + _network.home_id_str + ".xml"
    try:
        tree = etree.parse(filename)
        node = tree.find("{http://code.google.com/p/open-zwave/}Node[@id='" + str(node_id) + "']")
        tree.getroot().remove(node)
        working_file = open(filename, "w")
        working_file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        working_file.writelines(etree.tostring(tree, pretty_print=True))
        working_file.close()
        start_network()
        return format_json_result()
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GhostKiller()', methods=['GET'])
def ghost_killer(node_id):
    global _ghost_node_id
    # Remove cc 0x84 wake up for a ghost device in openzwave config file
    if not can_execute_network_command(0):
        return build_network_busy_message() 
    add_log_entry('Remove cc 0x84 (wake_up) for a ghost device: %s' % (node_id,))
    
    filename = _data_folder + "/zwcfg_" + _network.home_id_str + ".xml"
    # ensure load latest file version
    try:
        _network.stop()
        add_log_entry('ZWave network is now stopped')
        time.sleep(5)
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')
    try: 
        found = False       
        message = None    
        tree = etree.parse(filename)
        namespace = tree.getroot().tag[1:].split("}")[0]
        node = tree.find("{%s}Node[@id='%s']" % (namespace, node_id,))
        if node is None:
            message = 'node not found'
        else:            
            command_classes = node.find(".//{%s}CommandClasses" % namespace)
            if command_classes is None:
                message = 'commandClasses not found'
            else:
                for command_Class in command_classes.findall(".//{%s}CommandClass" % namespace):
                    if int(command_Class.get("id")[:7]) == COMMAND_CLASS_WAKE_UP:
                        command_classes.remove(command_Class)
                        found = True
                        break
                if found:
                    config_file = open(filename, "w")
                    config_file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
                    config_file.writelines(etree.tostring(tree, pretty_print=True))
                    config_file.close()
                    # save _ghost_node_id for next sanitary check
                    _ghost_node_id = node_id
                else:
                    message = 'commandClass wake_up not found'
        return format_json_result(found, message)
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')
    finally:
        start_network()            

"""
controllers routes
"""


@app.route('/ZWaveAPI/Run/controller.AddNodeToNetwork(<int:state>,<do_security>)', methods=['GET'])
def start_node_inclusion(state, do_security):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')
    if state == 1:
        if not can_execute_network_command(0):
            return build_network_busy_message()
        if do_security == 1:
            do_security = True
            add_log_entry("Start the Inclusion Process to add a Node to the Network with Security CC if the node is supports it")
        else:
            do_security = False
            add_log_entry("Start the Inclusion Process to add a Node to the Network")        
        execution_result = _network.manager.addNode(_network.home_id, do_security)
        if execution_result:
            _network_information.actual_mode = ControllerMode.AddDevice
        return format_json_result(execution_result)
    elif state == 0:
        add_log_entry("Start the Inclusion (Cancel)")
        _network.manager.cancelControllerCommand(_network.home_id)
        return format_json_result()


@app.route('/ZWaveAPI/Run/controller.RemoveNodeFromNetwork(<int:state>)', methods=['GET'])
def start_node_exclusion(state):
    if _network_information.controller_is_busy:
        return format_json_result(False, 'Controller is busy')
    if state == 1:
        if not can_execute_network_command(0):
            return build_network_busy_message()  
        add_log_entry("Remove a Device from the Z-Wave Network (Started)")
        execution_result = _network.manager.removeNode(_network.home_id)
        if execution_result:
            _network_information.actual_mode = ControllerMode.RemoveDevice
        return format_json_result(execution_result)
    elif state == 0:
        add_log_entry("Remove a Device from the Z-Wave Network (Cancel)")
        _network.manager.cancelControllerCommand(_network.home_id)
        return format_json_result() 


@app.route('/ZWaveAPI/Run/controller.CancelCommand()', methods=['GET'])
def cancel_command():    
    # Cancels any in-progress command running on a controller.
    add_log_entry("Cancels any in-progress command running on a controller.")
    try:
        execution_result = _network.manager.cancelControllerCommand(_network.home_id)
        if execution_result:
            _network_information.controller_is_busy = False
        return format_json_result(execution_result)
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/controller.RequestNetworkUpdate(<int:bridge_controller_id>)', methods=['GET'])
def request_network_update(bridge_controller_id):
    # Update the controller with network information from the SUC/SIS
    add_log_entry("Update the controller (%s) with network information from the SUC/SIS" % (bridge_controller_id,))
    if not can_execute_network_command(0):
        return build_network_busy_message()  
    if bridge_controller_id in _network.nodes:
        execution_result = _network.manager.requestNetworkUpdate(_network.home_id, bridge_controller_id)
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (bridge_controller_id,), 'warning')
    return format_json_result(execution_result)


@app.route('/ZWaveAPI/Run/controller.ReplicationSend(<int:bridge_controller_id>)', methods=['GET'])
def replication_send(bridge_controller_id):
    # Send information from primary to secondary
    if not can_execute_network_command(0):
        return build_network_busy_message() 
    add_log_entry('Send information from primary to secondary %s' % (bridge_controller_id,))
    try:
        if bridge_controller_id in _network.nodes:
            return format_json_result(_network.manager.replicationSend(_network.home_id, bridge_controller_id))
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (bridge_controller_id,), 'warning')
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/controller.HealNetwork()', methods=['GET'])
def heal_network(perform_return_routes_initialization=False):
    if not can_execute_network_command(0):
        return build_network_busy_message()      
    add_log_entry("Heal network by requesting node's rediscover their neighbors") 
    for node_id in list(_network.nodes):
        if node_id in _not_supported_nodes:
            debug_print("skip not supported (nodeId: %s)" % (node_id,))
            continue
        if _network.nodes[node_id].is_failed:
            debug_print("skip presume dead (nodeId: %s)" % (node_id,))
            continue        
        if _network.nodes[node_id].query_stage != "Complete":
            debug_print("skip query stage not complete (nodeId: %s)" % (node_id,))
            continue
        if _network.nodes[node_id].generic == 1:
            debug_print("skip Remote controller (nodeId: %s) (they don't have neighbors)" % (node_id,))
            continue
        _network.manager.healNetworkNode(_network.home_id, node_id, perform_return_routes_initialization)
    return format_json_result()


@app.route('/ZWaveAPI/Run/controller.SerialAPISoftReset()', methods=['GET'])
def soft_reset():
    add_log_entry("Soft-reset the Z-Wave controller chip")
    try:
        return format_json_result(_network.controller.soft_reset())
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/controller.TestNetwork()', methods=['GET'])
def test_network(count=3):
    # Test network node.
    # Sends a series of messages to a network node for testing network reliability.
    if not can_execute_network_command():
        return build_network_busy_message()  
    try:
        add_log_entry("Sends a series of messages to a network node for testing network reliability")
        _network.manager.testNetwork(_network.home_id, count)
        return format_json_result()
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/controller.CreateNewPrimary()', methods=['GET'])
def create_new_primary():
    # Put the target controller into receive configuration mode.
    # The PC Z-Wave Controller must be within 2m of the controller that is being made the primary
    if not can_execute_network_command(0):
        return build_network_busy_message()  
    add_log_entry("Add a new controller to the Z-Wave network")
    try:
        return format_json_result(_network.manager.createNewPrimary(_network.home_id))
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/controller.TransferPrimaryRole()', methods=['GET'])
def transfer_primary_role():
    # Add a new controller to the network and make it the primary.
    # The existing primary will become a secondary controller
    if not can_execute_network_command(0):
        return build_network_busy_message()  
    add_log_entry("Transfer Primary Role")
    try:
        return format_json_result(_network.manager.transferPrimaryRole(_network.home_id))
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/controller.ReceiveConfiguration()', methods=['GET'])
def receive_configuration():
    # Receive Z-Wave network configuration information from another controller
    if not can_execute_network_command(0):
        return build_network_busy_message()  
    add_log_entry("Receive Configuration")
    try:
        return format_json_result(_network.manager.receiveConfiguration(_network.home_id))
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/controller.HardReset()', methods=['GET'])
def hard_reset():
    # Hard Reset a PC Z-Wave Controller.
    # Resets a controller and erases its network configuration settings.
    # The controller becomes a primary controller ready to add devices to a new network.
    add_log_entry("Resets a controller and erases its network configuration settings")
    if not can_execute_network_command(0):
        return build_network_busy_message() 
    try:
        _network.controller.hard_reset()
        add_log_entry('The controller becomes a primary controller ready to add devices to a new network')
        time.sleep(3)
        start_network()
        return format_json_result()        
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')
            
"""
network routes
"""


@app.route('/ZWaveAPI/Run/network.Start()', methods=['GET'])
def network_start():
    add_log_entry('******** The ZWave network is being started ********')
    try:
        start_network()     
        return format_json_result()   
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/network.Stop()', methods=['GET'])
def stop_network():
    graceful_stop_network()
    return format_json_result() 


@app.route('/ZWaveAPI/Run/network.GetStatus()', methods=['GET'])
def get_network_status(): 
    if _network is not None and _network.state >= 5:   # STATE_STARTED
        json_result = {'nodesCount': _network.nodes_count, 'sleepingNodesCount': get_sleeping_nodes_count(),
                       'scenesCount': _network.scenes_count, 'pollInterval': _network.manager.getPollInterval(),
                       'isReady': _network.is_ready, 'stateDescription': _network.state_str, 'state': _network.state,
                       'controllerCapabilities': concatenate_list(_network.controller.capabilities),
                       'controllerNodeCapabilities': concatenate_list(_network.controller.node.capabilities),
                       'outgoingSendQueue': _network.controller.send_queue_count,
                       'controllerStatistics': _network.controller.stats, 'devicePath': _network.controller.device,
                       'OpenZwaveLibraryVersion': _network.manager.getOzwLibraryVersionNumber(),
                       'PythonOpenZwaveLibraryVersion': _network.manager.getPythonLibraryVersionNumber(),
                       'neighbors': concatenate_list(_network.controller.node.neighbors),
                       'notification': _network_information.last_controller_notification,
                       'isBusy': _network_information.controller_is_busy, 'startTime': _network_information.start_time,
                       'isPrimaryController': _network.controller.is_primary_controller,
                       'isStaticUpdateController': _network.controller.is_static_update_controller,
                       'isBridgeController': _network.controller.is_bridge_controller,
                       'awakedDelay': _network_information.controller_awake_delay, 'mode': get_network_mode()
                       }
    else:
        json_result = {}
    return jsonify(json_result)


@app.route('/ZWaveAPI/Run/network.GetNeighbours()', methods=['GET'])
def get_network_neighbours():
    neighbours = {'updateTime': int(time.time())}
    nodes_data = {}
    for node_id in list(_network.nodes):
        nodes_data[node_id] = serialize_neighbour_to_json(node_id)
    neighbours['devices'] = nodes_data
    return jsonify(neighbours)


@app.route('/ZWaveAPI/Run/network.GetHealth()', methods=['GET'])
def get_network_health():
    network_health = {'updateTime': int(time.time())}
    nodes_data = {}
    for node_id in list(_network.nodes):
        nodes_data[node_id] = serialize_node_health(node_id)
    network_health['devices'] = nodes_data
    return jsonify(network_health)


@app.route('/ZWaveAPI/Run/network.GetNodesList()', methods=['GET'])
def get_nodes_list():
    nodes_list = {'updateTime': int(time.time())}
    nodes_data = {}
    for node_id in list(_network.nodes):
        my_node = _network.nodes[node_id]
        json_node = {}
        try:
            manufacturer_id = int(my_node.manufacturer_id, 16)
        except ValueError:
            manufacturer_id = None
        try:
            product_id = int(my_node.product_id, 16)
        except ValueError:
            product_id = None
        try:
            product_type = int(my_node.product_type, 16)
        except ValueError:
            product_type = None      
        
        node_name = my_node.name
        node_location = my_node.location
        if is_none_or_empty(node_name):
            node_name = 'Unknown'  
        if _network.controller.node_id == node_id:
            node_name = my_node.product_name
            node_location = 'Jeedom'
                  
        json_node['description'] = {'name': node_name, 'location': node_location, 'product_name': my_node.product_name, 'is_static_controller': my_node.basic == 2}
        json_node['product'] = {'manufacturer_id': manufacturer_id, 'product_type': product_type, 'product_id': product_id, 'is_valid': manufacturer_id is not None and product_id is not None and product_type is not None}
        nodes_data[node_id] = json_node
    nodes_list['devices'] = nodes_data
    return jsonify(nodes_list)


@app.route('/ZWaveAPI/Run/network.GetControllerStatus()', methods=['GET'])
def get_controller_status():
    # Get the controller status
    try:
        controller_status = {}
        if _network is not None and _network.state >= 5:   # STATE_STARTED
            if _network.controller:
                controller_status = serialize_controller_to_json()
        return jsonify({'result': controller_status})
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/network.GetOZLogs()', methods=['GET'])
def get_openzwave_logs():
    # Read the openzwave log file
    global _data_folder
    try:
        std_in, std_out = os.popen2("tail -n 1000 " + _data_folder + "/openzwave.log")
        std_in.close()
        lines = std_out.readlines()
        std_out.close()
        return jsonify({'result': lines})
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/network.GetZWConfig()', methods=['GET'])
def get_openzwave_config():
    # ensure load latest file version
    global _data_folder
    try:
        write_config()
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')
    filename = _data_folder + "/zwcfg_" + _network.home_id_str + ".xml"
    try:
        with open(filename, "r") as ins:
            content = ins.read()
        return jsonify({'result': content})
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/network.SaveZWConfig()', methods=['POST'])
def save_openzwave_config():
    # Save the openzwave config file
    add_log_entry('Edit openzwave configuration file')
    if len(request.data) == 0:
        return format_json_result(False, 'zwcfg data content not present', 'error')
    global _data_folder
    try:
        filename = _data_folder + "/zwcfg_" + _network.home_id_str + ".xml"
        _network.stop()
        while _network.state != 0:
            add_log_entry('%s (%s)' %(_network.state_str, _network.state,))
            time.sleep(1)
        add_log_entry(_network.state_str)
        add_log_entry('Write new config file: %s' %(filename,))
        with open(filename, "w") as ins:
            ins.write(request.data)
        add_log_entry('Restart network')
        start_network()
        return format_json_result() 
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/network.WriteZWConfig()', methods=['GET'])
def write_openzwave_config():
    # Write the openzwave config file
    try:
        write_config()
        return format_json_result()
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/network.RemoveUnknownsDevicesZWConfig()', methods=['GET'])
def remove_unknowns_devices_openzwave_config():
    # Remove unknowns devices from the openzwave config file
    # ensure load latest file version
    global _data_folder
    try:
        _network.stop()
        add_log_entry('ZWave network is now stopped')
        time.sleep(5)
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')
    
    filename = _data_folder + "/zwcfg_" + _network.home_id_str + ".xml"
    try:
        tree = etree.parse(filename)
        nodes = tree.findall(".//{http://code.google.com/p/open-zwave/}Product")
        for node in nodes:
            if node.get("name")[:7] == "Unknown":
                tree.getroot().remove(node.getparent().getparent())
        working_file = open(filename, "w")
        working_file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        working_file.writelines(etree.tostring(tree, pretty_print=True))
        working_file.close()
        start_network()
        return format_json_result()
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/network.SetPollInterval(<int:seconds>,<interval_between_polls>)', methods=['GET'])
def set_poll_interval(seconds, interval_between_polls):
    # Set the time period between polls of a node's state
    if not can_execute_network_command():
        return build_network_busy_message()  
    try:        
        add_log_entry('set_poll_interval seconds:%s, interval Between Polls: %s' % (seconds, bool(interval_between_polls)), )
        if _network.state < _network.STATE_AWAKED:
            return jsonify({'result': False, 'reason': 'network state must a minimum set to awake'})
        if seconds < 30:
            return jsonify({'result': False, 'reason': 'interval is too small'})
        _network.set_poll_interval(1000 * seconds, bool(interval_between_polls))
        return format_json_result()
    except Exception, exception:
        return format_json_result(False, str(exception), 'error')


@app.route('/ZWaveAPI/Run/network.RefreshAllBatteryLevel()', methods=['GET'])       
def refresh_all_battery_level():
    debug_print("refresh_all_battery_level")
    battery_levels = {}
    if _network is not None and _network.state >= 7:
        for node_id in list(_network.nodes):
            node = _network.nodes[node_id]
            if not node.is_listening_device:
                debug_print('Refresh battery level for nodeId: %s' % (node_id,))
                battery_level = get_value_by_index(node_id, COMMAND_CLASS_BATTERY, 1, 0)
                if battery_level is not None:
                    battery_level.refresh()
                    battery_levels[node_id] = {'value': battery_level.data, 'updateTime': battery_level.last_update}
    return jsonify(battery_levels)


@app.route('/ZWaveAPI/Run/network.GetOZBackups()', methods=['GET'])       
def get_openzwave_backups():
    # Return the list of all available backups
    global _data_folder
    debug_print("List all backups")
    my_result = {}
    backup_list = []
    backup_folder = _data_folder + "/xml_backups"
    # noinspection PyBroadException
    try:
        os.stat(backup_folder)
    except:
        os.mkdir(backup_folder)
    pattern = "_zwcfg_"
    filters = ['xml']
    actual_backups = os.listdir(backup_folder)
    actual_backups.sort(reverse=True)
    for candidateBackup in actual_backups:
        if candidateBackup[-3:] in filters and pattern in candidateBackup:
            backup_list.append(candidateBackup)
    my_result['Backups'] = backup_list
    return jsonify(my_result)


@app.route('/ZWaveAPI/Run/network.RestoreBackup(<backup_name>)', methods=['GET'])       
def restore_openzwave_backups(backup_name):
    # Manually restore a backup
    global _data_folder
    add_log_entry('Restoring backup ' + backup_name)
    backup_folder = _data_folder + "/xml_backups"
    # noinspection PyBroadException
    try:
        os.stat(backup_folder)
    except:
        os.mkdir(backup_folder)
    backup_file = os.path.join(backup_folder, backup_name)
    target_file = _data_folder + "/zwcfg_" + _network.home_id_str + ".xml"
    if not os.path.isfile(backup_file):
        add_log_entry('No config file found to backup', "error")
        return format_json_result(False, 'No config file found with name ' + backup_name)
    else:
        # noinspection PyBroadException
        try:
            tree = etree.parse(backup_file)
        except:
            add_log_entry('The backup file seems invalid', "error")
            return format_json_result(False, 'The backup file (' + backup_name + ') seems invalid')
        _network.stop()
        add_log_entry('ZWave network is now stopped')
        time.sleep(3)
        shutil.copy2(backup_file, target_file)
        os.chmod(target_file, 0777)
        start_network()
    return format_json_result(True, backup_name + ' successfully restored')


@app.route('/ZWaveAPI/Run/network.ManualBackup()', methods=['GET'])       
def manually_backup_config():
    # Manually create a backup
    add_log_entry('Manually creating a backup')
    return backup_xml_config('manual', _network.home_id_str)


@app.route('/ZWaveAPI/Run/network.DeleteBackup(<backup_name>)', methods=['GET'])       
def manually_delete_backup(backup_name):
    # Manually delete a backup
    global _data_folder
    add_log_entry('Manually deleting a backup')
    backup_folder = _data_folder + "/xml_backups"
    backup_file = os.path.join(backup_folder, backup_name)
    if not os.path.isfile(backup_file):
        add_log_entry('No config file found to delete', "error")
        return format_json_result(False, 'No config file found with name ' + backup_name)
    else:
        os.unlink(backup_file)
    return format_json_result(True, backup_name + ' successfully deleted')


@app.route('/ZWaveAPI/Run/IsAlive()', methods=['GET'])
def rest_is_alive():    
    return format_json_result()
    
if __name__ == '__main__':
    pid = str(os.getpid())
    file(_pid_file, 'w').write("%s\n" % pid)
    try:
        app.run(host='0.0.0.0', port=int(_port_server), debug=False)
    except Exception, ex:
        print "Fatal Error: %s" % str(ex)
