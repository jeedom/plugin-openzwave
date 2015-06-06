#!flask/bin/python
"""
Copyright (c) 2014 
author : Thomas Martinez tmartinez69009@gmail.com
author : Jean-Francois Auger jeanfrancois.auger@gmail.com
SOFTWARE NOTICE AND LICENSE This file is part of Plugin openzwave for jeedom project
Plugin openzwave for jeedom is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
Plugin openzwave for jeedom is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Plugin openzwave for jeedom. If not, see http://www.gnu.org/licenses.
"""
import sys, os

try:
    from flask import Flask, jsonify, abort, request, make_response, redirect, url_for
except Exception as e:
    print "The dependances of openzwave plugin are not installed. Please, check the plugin openzwave configuration page for instructions"
    print "Error %s:" % str(e)
    sys.exit(1)
    
import logging
import signal

import time
import datetime
import binascii
import sqlite3 as lite
import threading
import socket

os.environ['PYTHON_EGG_CACHE'] = '/opt/python-openzwave/python-eggs'

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('openzwave')

reload(sys)  
sys.setdefaultencoding('utf8')

con = None
try:
    con = lite.connect(":memory:", check_same_thread=False)
    con.isolation_level = None
    cur = con.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print "SQLite version: %s" % data  
    cur.execute("DROP TABLE IF EXISTS Events")  
    cur.execute("CREATE TABLE IF NOT EXISTS Events(Node INT, Instance INT, Commandclass INT, Type TEXT, Id TEXT, Index_value INT, Value TEXT, Level INT, UpdateTime INT)")               
except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)

try :
    import openzwave
    from openzwave.node import ZWaveNode
    from openzwave.value import ZWaveValue
    from openzwave.scene import ZWaveScene
    from openzwave.controller import ZWaveController
    from openzwave.network import ZWaveNetwork
    from openzwave.option import ZWaveOption
    from openzwave.group import ZWaveGroup
    print("Openzwave is installed.")
except :
    print("Openzwave is not installed. Get it from tmp directory.")
    sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.6/dist-packages'))
    sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.7/dist-packages'))
    sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.6/dist-packages'))
    sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.7/dist-packages'))
    import openzwave
    from openzwave.node import ZWaveNode
    from openzwave.value import ZWaveValue
    from openzwave.scene import ZWaveScene
    from openzwave.controller import ZWaveController
    from openzwave.network import ZWaveNetwork
    from openzwave.option import ZWaveOption
    from openzwave.group import ZWaveGroup
    
from louie import dispatcher, All

device="/dev/zwave-aeon-s2"
log="None"

COMMAND_CLASS_NO_OPERATION              = 0 # 0x00
COMMAND_CLASS_BASIC                     = 32 # 0x20   
COMMAND_CLASS_CONTROLLER_REPLICATION    = 33 # 0x21
COMMAND_CLASS_APPLICATION_STATUS        = 34 # 0x22
COMMAND_CLASS_ZIP_SERVICES              = 35 # 0x23
COMMAND_CLASS_ZIP_SERVER                = 36 # 0x24
COMMAND_CLASS_SWITCH_BINARY             = 37 # 0x25
COMMAND_CLASS_SWITCH_MULTILEVEL         = 38 # 0x26
COMMAND_CLASS_SWITCH_ALL                = 39 # 0x27
COMMAND_CLASS_SWITCH_TOGGLE_BINARY      = 40 # 0x28
COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL  = 41 # 0x29
COMMAND_CLASS_CHIMNEY_FAN               = 42 # 0x2A
COMMAND_CLASS_SCENE_ACTIVATION          = 43 # 0x2B
COMMAND_CLASS_SCENE_ACTUATOR_CONF       = 44 # 0x2C
COMMAND_CLASS_SCENE_CONTROLLER_CONF     = 45 # 0x2D
COMMAND_CLASS_ZIP_CLIENT                = 46 # 0x2E
COMMAND_CLASS_ZIP_ADV_SERVICES          = 47 # 0x2F
COMMAND_CLASS_SENSOR_BINARY             = 48 # 0x30
COMMAND_CLASS_SENSOR_MULTILEVEL         = 49 # 0x31
COMMAND_CLASS_METER                     = 50 # 0x32    
COMMAND_CLASS_ZIP_ADV_SERVER            = 51 # 0x33
COMMAND_CLASS_ZIP_ADV_CLIENT            = 52 # 0x34
COMMAND_CLASS_METER_PULSE               = 53 # 0x35
COMMAND_CLASS_THERMOSTAT_HEATING        = 56 # 0x38
COMMAND_CLASS_METER_TBL_CONFIG          = 60 # 0x3C
COMMAND_CLASS_METER_TBL_MONITOR         = 61 # 0x3D
COMMAND_CLASS_METER_TBL_PUSH            = 62 # 0x3E
COMMAND_CLASS_THERMOSTAT_MODE           = 64 # 0x40
COMMAND_CLASS_THERMOSTAT_OPERATING_STATE = 66 # 0x42
COMMAND_CLASS_THERMOSTAT_SETPOINT       = 67 # 0x43
COMMAND_CLASS_THERMOSTAT_FAN_MODE       = 68 # 0x44
COMMAND_CLASS_THERMOSTAT_FAN_STATE      = 69 # 0x45
COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE  = 70 # 0x46
COMMAND_CLASS_THERMOSTAT_SETBACK        = 71 # 0x47
COMMAND_CLASS_DOOR_LOCK_LOGGING         = 76 # 0x4C
COMMAND_CLASS_SCHEDULE_ENTRY_LOCK       = 78 # 0x4E
COMMAND_CLASS_BASIC_WINDOW_COVERING     = 80 # 0x50
COMMAND_CLASS_MTP_WINDOW_COVERING       = 81 # 0x51
COMMAND_CLASS_MULTI_INSTANCE            = 96 # 0x60
COMMAND_CLASS_DOOR_LOCK                 = 98 # 0x62
COMMAND_CLASS_USER_CODE                 = 99 # 0x63
COMMAND_CLASS_BARRIER_OPERATOR          = 102 # 0x66
COMMAND_CLASS_CONFIGURATION             = 112 # 0x70
COMMAND_CLASS_ALARM                     = 113 # 0x71
COMMAND_CLASS_MANUFACTURER_SPECIFIC     = 114 # 0x72    
COMMAND_CLASS_POWERLEVEL                = 115 # 0x73
COMMAND_CLASS_PROTECTION                = 117 # 0x75
COMMAND_CLASS_LOCK                      = 118 # 0x76
COMMAND_CLASS_NODE_NAMING               = 119 # 0x77
COMMAND_CLASS_FIRMWARE_UPDATE_MD        = 122 # 0x7A
COMMAND_CLASS_GROUPING_NAME             = 123 # 0x7B
COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE =124 # 0x7C
COMMAND_CLASS_REMOTE_ASSOCIATION        = 125 # 0x7D
COMMAND_CLASS_BATTERY                   = 128 #0x80
COMMAND_CLASS_CLOCK                     = 129 #0x81
COMMAND_CLASS_HAIL                      = 130 #0x82
COMMAND_CLASS_WAKE_UP                   = 132 #0x84
COMMAND_CLASS_ASSOCIATION               = 133 #0x85
COMMAND_CLASS_VERSION                   = 134 #0x86
COMMAND_CLASS_INDICATOR                 = 135 #0x87
COMMAND_CLASS_PROPRIETARY               = 136 #0x88
COMMAND_CLASS_LANGUAGE                  = 137 #0x89
COMMAND_CLASS_TIME                      = 138 #0x8A
COMMAND_CLASS_TIME_PARAMETERS           = 139 # 0x8B
COMMAND_CLASS_GEOGRAPHIC_LOCATION       = 150 #0x8C
COMMAND_CLASS_COMPOSITE                 = 141 # 0x8D
COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION_V2 = 142 #0x8E
COMMAND_CLASS_MULTI_CMD                 = 143 # 0x8F
COMMAND_CLASS_ENERGY_PRODUCTION         = 144 # 0x90
COMMAND_CLASS_MANUFACTURER_PROPRIETARY  = 145 # 0x91
COMMAND_CLASS_SCREEN_MD                 = 146 #0x92
COMMAND_CLASS_SCREEN_ATTRIBUTES         = 147 # 0x93
COMMAND_CLASS_SIMPLE_AV_CONTROL         = 148 # 0x94
COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD   = 149 # 0x95
COMMAND_CLASS_AV_RENDERER_STATUS        = 150 # 0x96
COMMAND_CLASS_AV_CONTENT_SEARCH_MD      = 151 # 0x97
COMMAND_CLASS_SECURITY                  = 152 # 0x98
COMMAND_CLASS_AV_TAGGING_MD             = 153 # 0x99
COMMAND_CLASS_IP_CONFIGURATION          = 154 # 0x9A
COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION = 155 # 0x9B
COMMAND_CLASS_SENSOR_ALARM              = 156 # 0x9C
COMMAND_CLASS_SILENCE_ALARM             = 157 # 0x9D
COMMAND_CLASS_SENSOR_CONFIGURATION      = 158 #0x9E
COMMAND_CLASS_MARK                      = 239 # 0xEF
COMMAND_CLASS_NON_INTEROPERABLE         = 240 # 0xF0
 
for arg in sys.argv:
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--port"):
        temp,port_server = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    elif arg.startswith("--pidfile"):
        temp,pidfile = arg.split("=")
    elif arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")

#log = "Debug"

def debug_print(message):
    if log == "Debug":
        add_log_entry(message, "debug")
        
def add_log_entry(message, level="info"):
    print('%s | %s | %s' % (time.strftime('%d-%m-%Y %H:%M:%S',time.localtime()), level, message.encode('utf8'),)) 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1',int(port_server)))
if result == 0:
    add_log_entry('The port %s is already in use. Please check your openzwave configuration plugin page' % (port_server,), 'error')
    sys.exit(1)

Idle= 0
AddDevice = 1
RemoveDevice = 5

class ControllerMode:
    class Idle: pass
    class AddDevice: pass
    class RemoveDevice: pass
  
class NetworkInformations(object):
    
    def __init__(self):
        self._actualMode = ControllerMode.Idle
        self._startTime=int(time.time())
        self._configFileSaveInProgress = False
        self._controllerIsBusy = False;
        self._controllerState = ZWaveController.SIGNAL_CTRL_STARTING
        self._lastControllerNotification = {"state": self._controllerState, "details": '', "timestamp" :int(time.time())}         
    
    @property
    def actualMode(self):        
        return self._actualMode
    
    @actualMode.setter
    def actualMode(self, value):        
        self._actualMode = value
        
    @property
    def startTime(self):        
        return self._startTime
    
    @startTime.setter
    def startTime(self, value):        
        self._startTime = value
        
    @property
    def configFileSaveInProgress(self):        
        return self._configFileSaveInProgress
    
    @configFileSaveInProgress.setter
    def configFileSaveInProgress(self, value):        
        self._configFileSaveInProgress = value
        
    @property
    def controllerIsBusy(self):        
        return self._controllerIsBusy
    
    @controllerIsBusy.setter
    def controllerIsBusy(self, value):        
        self._controllerIsBusy = value
        
    @property
    def controllerState(self):        
        return self._controllerState
    
    @property
    def lastControllerNotification(self):        
        return self._lastControllerNotification
    
    def assignControllerNotification(self, state, details):
        self._controllerState = state
        self._lastControllerNotification['state'] = state
        self._lastControllerNotification['details'] = details
        self._lastControllerNotification['timestamp'] = int(time.time())
        
        if state == ZWaveController.SIGNAL_CTRL_WAITING:
            self.controllerIsBusy = True
        elif state == ZWaveController.SIGNAL_CTRL_INPROGRESS:
            self.controllerIsBusy = True
        elif state == ZWaveController.SIGNAL_CTRL_STARTING:
            self.controllerIsBusy = False           
            self.actualMode = ControllerMode.Idle
            self._startTime=int(time.time())
        else:
            self.controllerIsBusy = False
            #reset flag
            self.actualMode = ControllerMode.Idle
            
    def computeJeeDomMessage(self):
        if self.actualMode == ControllerMode.AddDevice:
            return AddDevice         
        elif self.actualMode == ControllerMode.RemoveDevice:
            return RemoveDevice
        else:
            return Idle


class PendingConfiguration(object):
    
    def __init__(self, expectedData, timeOut):
        self._startTime=int(time.time())
        self._expectedData = expectedData
        self._timeOut = timeOut;    
        self._data = None 
        
    @property
    def data(self):        
        return self._data
    
    @data.setter
    def data(self, value):        
        self._data = value
        
    @property
    def state(self):  
        if (self._data == None):
            # is pending
            return 3
        if (self._data != self._expectedData)  :
            # the node reject changes and set a default
            return 2
        # the parameter have be set succesfully
        return 1

            
class NodeNotification(object):
    
    def __init__(self, code, wakeup_time=None):
        self._receive_time=int(time.time())           
        self._code = code 
        self._description = code 
        self._help = code 
        self._wakeup_time = wakeup_time 
        self._next_wakeup = None       
        self.refresh(code, wakeup_time)
        
    def refresh(self, code, wakeup_time):
        if code == 0:
            self._description = "Completed"
            self._help = "Completed messages"
        elif code == 1:
            self._description = "Timeout"
            self._help = "Messages that timeout will send a Notification with this code"
        elif code == 2:
            self._description = "NoOperation"
            self._help = "Report on NoOperation message sent completion"
        elif code == 3:
            self._description = "Awake."
            self._help = "Report when a sleeping node wakes"
        elif code == 4:
            self._description = "Sleep."
            self._help = "Report when a node goes to sleep"
            #if they go to sleep, calcul the next expected wakeup time
            if wakeup_time != None:
                self._next_wakeup = wakeup_time + self._receive_time
        elif code == 5:
            self._description = "Dead."
            self._help = "Report when a node is presumed dead"
        elif code == 6:
            self._description = "Alive."
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
    def next_wakeup(self):        
        return self._next_wakeup
    

class ControllerCommands(object):
    
    def __init__(self, state, command):
        self._timestamp = int(time.time())
        self._state = state
        self._state_description = None
        self._command = command
        self._command_description = None
        
        if state == 0:
            self._state_description = 'Normal'
        elif state == 1:
            self._state_description = 'Starting'
        elif state == 2:
            self._state_description = 'Cancel'
        elif state == 3:
            self._state_description = 'Error'
        elif state == 4:
            self._state_description = 'Waiting'
        elif state == 5:
            self._state_description = 'Sleeping'
        elif state == 6:
            self._state_description = 'InProgress'
        elif state == 7:
            self._state_description = 'Completed'
        elif state == 8:
            self._state_description = 'Failed'
        elif state == 9:
            self._state_description = 'Node OK'
        elif state == 10:
            self._state_description = 'Node Failed'
                                                
        if command == 0:
            self._command_description = 'None'
        elif command == 1:
            self._command_description = 'Add Device' #'Remove Device'
        elif command == 2:
            self._command_description = 'Create New Primary'
        elif command == 3:
            self._command_description = 'Receive Configuration'
        elif command == 4:
            self._command_description = 'Remove Device' #'None'
        elif command == 5:
            self._command_description = 'Remove Failed Node'
        elif command == 6:
            self._command_description = 'Has Node Failed'
        elif command == 7:
            self._command_description = 'Replace Failed Node'
        elif command == 8:
            self._command_description = 'Transfer Primary Role'
        elif command == 9:
            self._command_description = 'Request Network Update'
        elif command == 10:
            self._command_description = 'Request Node Neighbor Update'
        elif command == 11:
            self._command_description = 'Assign Return Route'
        elif command == 12:
            self._command_description = 'Delete All Return Routes'
        elif command == 13:
            self._command_description = 'Send Node Information'
        elif command == 14:
            self._command_description = 'Replication Send'
        elif command == 15:
            self._command_description = 'Create Button'
        elif command == 16:
            self._command_description = 'Delete Button'                                                                                                                                                 
    
    @property
    def timestamp(self):
        return self._timestamp
    
    @property
    def state(self):
        return self._state
    
    @property
    def command(self):
        return self._command
    
    @property
    def state_description(self):
        return self._state_description
    
    @property
    def command_description(self):
        return self._command_description   
    
    
def signal_handler(signal, frame):
    network.write_config()
    add_log_entry('Graceful stopping the ZWave network.')
    network.stop()
    add_log_entry('The Openzwave REST-server was stopped in a normal way')
    sys.exit(0)
        
signal.signal(signal.SIGTERM, signal_handler)

#Define some manager options
options = ZWaveOption(device, config_path="/opt/python-openzwave/openzwave/config", user_path="/opt/python-openzwave/", cmd_line="")
options.set_log_file("openzwave.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level(log)
options.set_logging(True)
options.set_associate(True)                       
options.set_save_configuration(True)              
options.set_poll_interval(60000) #  60 seconds    
options.set_interval_between_polls(False)         
options.set_notify_transactions(True) # Notifications when transaction complete is reported.           
options.set_suppress_value_refresh(False) # if true, notifications for refreshed (but unchanged) values will not be sent.        
options.set_driver_max_attempts(5)                
#options.addOptionBool("PerformReturnRoutes", True)
#options.addOptionBool("AssumeAwake", True)        
options.addOptionInt("RetryTimeout", 6000)
options.addOptionString("NetworkKey","0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10",True)
options.lock()

force_refresh_nodes = []    

def save_node_event(node_id, timestamp, value):
    global con
    cur = con.cursor()
    #add a new cache entry for value 
    cur.execute("INSERT INTO Events (Node, Instance, Commandclass, Type, Id, Index_value, Value, Level, Updatetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (node_id, 0, 0, "", "", "", value, 0, timestamp))
    
def save_node_value_event(node_id, timestamp, command_class, index, typeStandard, value, instance):
    global con
    cur = con.cursor()
    #delete the existing cache entry, if exist
    cur.execute("DELETE FROM Events where Node=? AND Commandclass=? AND Instance=? AND Index_value=?", (node_id, command_class, instance, index,))   
    #add a new cache entry for value 
    cur.execute("INSERT INTO Events (Node, Instance, Commandclass, Type, Id, Index_value, Value, Level, Updatetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (node_id, instance, command_class, typeStandard, "", index, value, 0, timestamp))  

def network_started(network):
    add_log_entry("Openzwave network are started with homeId %0.8x." % (network.home_id,))    
    networkInformations.assignControllerNotification(ZWaveController.SIGNAL_CTRL_STARTING, "Network is started")

def network_failed(network):
    add_log_entry("Openzwave network can't load", "error")
    networkInformations.assignControllerNotification(ZWaveController.SIGNAL_CTRL_ERROR, "Network have failed")

def recovering_failed_nodes():
    return
    for idNode in network.nodes:
        if network.nodes[idNode].isNodeFailed:
            if network.manager.hasNodeFailed(network.home_id, idNode):
                #avoid stress network
                time.sleep(2)

def network_awaked(network):
    add_log_entry("Openzwave network is awake : %d nodes were found (%d are sleeping). All listening nodes are queried, but some sleeping nodes may be missing." % (network.nodes_count, get_sleeping_nodes_count(),))
    add_log_entry("Controller is : %s" % (network.controller,))
    networkInformations.assignControllerNotification(ZWaveController.SIGNAL_CTRL_NORMAL, "Network is awaked")
    recovering_failed_nodes()

def network_ready(network):
    add_log_entry("Openzwave network is ready with %d nodes (%d are sleeping). All nodes are queried, the network is fully functionnal." % (network.nodes_count, get_sleeping_nodes_count(),))   
    write_config()
    networkInformations.assignControllerNotification(ZWaveController.SIGNAL_CTRL_NORMAL, "Network is ready")
    recovering_failed_nodes()

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
    add_log_entry('A new node (%s), not already stored in zwcfg*.xml file, was found.' % (node_id,))
    force_refresh_nodes.append(node_id)    
    
def node_added(network, node):
    add_log_entry('A node has been added to OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
    node.last_update=time.time()   
    save_node_event(node.node_id, int(time.time()), "added") 
    #TODO: is a work around until got real command notifications
    if networkInformations.actualMode != ControllerMode.Idle:
        networkInformations.actualMode = ControllerMode.Idle
    
        
def node_removed(network, node):
    add_log_entry('A node has been removed from OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
    save_node_event(node.node_id, int(time.time()), "removed")
    #TODO: is a work around until got real command notifications
    if networkInformations.actualMode != ControllerMode.Idle:
        networkInformations.actualMode = ControllerMode.Idle

def get_standard_value_type(valueType):
    if valueType == "Int" :
        return 'int'
    elif valueType == "Decimal" :
        return 'float'
    elif valueType == "Bool" :
        return 'bool'
    elif valueType == "Byte" :
        return 'int'
    elif valueType == "Short" :
        return 'int'
    elif valueType == "Button" :
        return 'bool'
    elif valueType == "Raw" :
        return 'binary'
    else :
        return valueType

def change_instance(myValue):
    if myValue.instance > 1:
        return myValue.instance - 1
    return 0

def extract_data(value, displayRaw = False):
    if value.type == "Bool":
        if value.data:
            value2 = 'true'
        else:
            value2 = 'false'
    elif value.units == "F":
        value2 = str((float(value.data_as_string) - 32) * 5.0 / 9.0)
    elif value.type == "Raw":
        value2 = binascii.b2a_hex(value.data)
        if displayRaw :
            print('Raw Signal : %s' % value2)
    else:
        value2 = str(value.data_as_string)
    return value2

def can_execute_network_command(allowed_queue_count=25):
    if not network.controller.is_primary_controller:
        return True
    if network.controller.send_queue_count > allowed_queue_count:
        return False
    if networkInformations.controllerIsBusy:
        return False
    if networkInformations.actualMode != ControllerMode.Idle:
        return False
    if network.state < network.STATE_STARTED:
        return False
    return True

def write_config():  
    watchDog = 0  
    while(networkInformations.configFileSaveInProgress and watchDog <10):
        if log == "Debug":
            print ('.')
        time.sleep(1)
        watchDog +=1
    if networkInformations.configFileSaveInProgress:
        return        
    networkInformations.configFileSaveInProgress = True
    try:
        network.write_config()
        add_log_entry('write configuration xml file')
        time.sleep(1)
    except Exception as error:
        add_log_entry('write_config %s' % (str(error),), "error")
    finally:
        networkInformations.configFileSaveInProgress = False

def essential_node_queries_complete(network, node):   
    debug_print('The essential queries on a node have been completed. id:[%s] model:[%s].' % (node.node_id, node.product_name,))   
    timestamp = int(time.time())
    myNode = network.nodes[node.node_id]
    myNode.last_update=time.time()   
    #at this time is not good to save value, I skip this step                                    

def node_queries_complete(network, node):
    debug_print('All the initialisation queries on a node have been completed. id:[%s] model:[%s].' % (node.node_id, node.product_name,))        
    node.last_update=time.time()  
    #save config 
    write_config() 
    '''
    for new node not already stored in zwcfg*.xml file, we need to force a refresh of all configuration values. 
    openzwave only return default values durring interview, not the stored in device 
    '''    
    try:
        index = force_refresh_nodes.index(node.node_id)
        force_refresh_nodes.remove(node.node_id) 
        debug_print('Forces a refresh of the configuration values nodeId: %s' % (node.node_id,)) 
        try:
            for val in node.values:
                currentValue = node.values[val]
                if currentValue.genre == 'Config':
                    if currentValue.type == 'Button':
                        continue
                    if currentValue.is_write_only:
                        continue                
                    currentValue.refresh()                
        except Exception as error:
            add_log_entry('Refresh configuration: %s' % (str(error), ), "error")            
    except ValueError:
        #node_id not found come here, is the speed way to check item in list
        pass    
    
def save_valueAsynchronous(node, value, last_update):
    #debug_print('A node value has been updated. nodeId:%s value:%s' % (node.node_id, value.label))
    if(node.node_id in network.nodes) :
        myNode = network.nodes[node.node_id]    
        #check if am the realy last update
        if myNode.last_update>last_update:
            return
        #mark as seen flag
        myNode.last_update=last_update
        #if value.genre != 'Basic':
        value.last_update=last_update         
        save_node_value_event(node.node_id, int(time.time()), value.command_class, value.index, get_standard_value_type(value.type), extract_data(value, False), change_instance(value))    

def value_added(network, node, value):  
    #debug_print('value_added. %s %s' % (node.node_id, value.label,)) 
    #mark initial data for skip notification durring interview
    value.lastData = value.data 

def prepare_value_notification(node, value):
    if hasattr(value, 'pendingConfiguration' ):
        if(value.pendingConfiguration != None):
            #mark result
            value.pendingConfiguration.data = value.data
                
    if value.genre == 'System' or value.genre == 'Config':
        return
    
    if not node.isReady :
        #check if have the attribute
        if hasattr(value, 'lastData') and value.lastData == value.data :
            #we skip notification to avoid value refresh durring the interview process
            return
    #update for next run    
    value.lastData = value.data    
    debug_print('send value notification %s %s %s' % (node.node_id, value.label, value.data_as_string))  
    thread = None
    try:
        thread = threading.Thread(target=save_valueAsynchronous, args=(node, value, time.time()))
        thread.setDaemon(False)
        thread.start()
    except Exception as error:
        add_log_entry('value_update %s' % (str(error), ), "error")
        if (thread != None):
            thread.stop()

def value_update(network, node, value): 
    #debug_print('value_update. %s %s' % (node.node_id, value.label,))
    prepare_value_notification(node, value)
                
def value_refreshed(network, node, value): 
    #debug_print('value_refreshed. %s %s' % (node.node_id, value.label,))  
    value_update(network, node, value)
        
def scene_event(network, node, scene_id):
    add_log_entry('Scene Activation : %s' % (scene_id,))        
    timestamp = int(time.time())
    typestd = 'int'        
    save_node_value_event(node.node_id, int(time.time()), 91, 0, typestd, scene_id, 0)  
    save_node_value_event(node.node_id, int(time.time()), 43, 0, typestd, scene_id, 0)  
    
def controller_message(state, message, network, controller):    
    #save actual state
    networkInformations.assignControllerNotification(state, message)    
    #notify jeedom
    save_node_event(network.controller.node_id, int(time.time()), networkInformations.computeJeeDomMessage())     
    add_log_entry('Controller state: %s. %s' % (state, message,)) 
    debug_print('Controller is busy: %s' % (networkInformations.controllerIsBusy,))   

def save_controller_command(state, command):
    #TODO: got a real notification with valid data, the current are not correctly mapped. 
    #network.current_command = ControllerCommands(state, command)
    #add_log_entry('A message is sent form controller: %s(%s) is %s(%s)' % (network.current_command.command_description, network.current_command.command, network.current_command.state_description, network.current_command.state))
    add_log_entry('A message is sent form controller: %s is %s' % (command, state))

def controller_command(network, controller, state, command):
    save_controller_command(state, command)

def node_event(network, node, value):
    debug_print('NodeId %s sends a Basic_Set command to the controller with value %s' % (node.node_id, value,)) 
    for val in network.nodes[node.node_id].values :
        myValue = network.nodes[node.node_id].values[val]
        if myValue.genre == "User" and myValue.is_write_only == False :
            value_update(network, node, myValue)
    """
    the value is actualy the event data, not a zwave value object.
    This is commonly caused when a node sends a Basic_Set command to the controller.
    """  

def node_group_changed(network, node):
    debug_print('Group changed for nodeId %s' % (node.node_id,)) 
    #TODO: reset group changed for pending associations

def get_wakeup_interval(device_id) :
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            myValue = network.nodes[device_id].values[val]
            if myValue.command_class == 132 and myValue.label =="Wake-up Interval":
                return network.nodes[device_id].values[val].data
    return None

def node_notification(args):
    code = int(args['notificationCode'])
    device_id = int(args['nodeId'])    
    if(device_id in network.nodes) :
        myNode = network.nodes[device_id]
        wakeup_time = get_wakeup_interval(device_id)
        if not hasattr(myNode, 'last_notification') :                         
            myNode.last_notification = NodeNotification(code, wakeup_time) 
        else:
            #I refresh notification, the wakeup_time can be modified from last time, we need to calculate the next expected wakeup time 
            myNode.last_notification.refresh(code, wakeup_time)
        debug_print('NodeId %s send a notification: %s' % (device_id, myNode.last_notification.description,))
        
        
    
#app = Flask(__name__, static_url_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'static')))
app = Flask(__name__, static_url_path = '/static')

#Create a network object
global network
global networkInformations

networkInformations = NetworkInformations()  
network = ZWaveNetwork(options, autostart=False)

#We connect to the louie dispatcher
dispatcher.connect(network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
dispatcher.connect(network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(network_failed, ZWaveNetwork.SIGNAL_DRIVER_FAILED)
dispatcher.connect(network_awaked, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
dispatcher.connect(network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

add_log_entry('******** The ZWave network is being started ********')
network.start()

#a new node has been found (not already stored in zwcfg*.xml file).
dispatcher.connect(node_new, ZWaveNetwork.SIGNAL_NODE_NEW)
#add node to the network, durring node discovering and after a inclusion 
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
# when a node sends a Basic_Set command to the controller.
dispatcher.connect(node_event, ZWaveNetwork.SIGNAL_NODE_EVENT)
# scene event
dispatcher.connect(scene_event, ZWaveNetwork.SIGNAL_SCENE_EVENT)
# the essential node query are completed
dispatcher.connect(essential_node_queries_complete, ZWaveNetwork.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE)
# all node querys are completed, the node is fully operational, is ready!
dispatcher.connect(node_queries_complete, ZWaveNetwork.SIGNAL_NODE_QUERIES_COMPLETE)
# is network notification same as SIGNAL_NETWORK_AWAKED, we don't need
dispatcher.connect(nodes_queried, ZWaveNetwork.SIGNAL_AWAKE_NODES_QUERIED)
# is network notification same as SIGNAL_NETWORK_READY, we don't need
dispatcher.connect(nodes_queried, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED)

dispatcher.connect(nodes_queried_some_dead, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD)
# a button is pressed
dispatcher.connect(button_on, ZWaveNetwork.SIGNAL_BUTTON_ON)
dispatcher.connect(button_off, ZWaveNetwork.SIGNAL_BUTTON_OFF)

#dispatcher.connect(node_group_changed, ZWaveNetwork.SIGNAL_GROUP)

# keep a track of actual network stage and last message
dispatcher.connect(controller_message, ZWaveController.SIGNAL_CONTROLLER)
# Called when an error happened, or node changed (awake, sleep, death, no operation, timeout).
dispatcher.connect(node_notification, ZWaveNetwork.SIGNAL_NOTIFICATION)
# keep a track of actual network command in progress
dispatcher.connect(controller_command, ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND)

add_log_entry('OpenZwave Library Version %s' %(network.manager.getOzwLibraryVersionNumber(),)) 
add_log_entry('Python-OpenZwave Wrapper Version %s' %(network.manager.getPythonLibraryVersionNumber(),)) 

#We wait for the network.
add_log_entry('Waiting for network to become ready')

def get_value_by_index(device_id, command_class, instance, index_id):
    if(device_id in network.nodes) :
        myDevice = network.nodes[device_id]
        for value_id in myDevice.values :
            if myDevice.values[value_id].command_class == command_class and myDevice.values[value_id].instance==instance and myDevice.values[value_id].index==index_id:
                return myDevice.values[value_id]      
    debug_print("get_value_by_index Value not found for device_id:%s, cc:%s, instance:%s, index:%s" % (device_id, command_class, instance, index_id,))            
    return None

def get_value_by_id(device_id, value_id):
    if(device_id in network.nodes) :
        myDevice = network.nodes[device_id]
        if (value_id in myDevice.values) :
            return myDevice.values[value_id]                 
    debug_print("get_value_by_id Value not found for device_id:%s, value_id:%s" % (device_id, value_id,)) 
    return None

def mark_pending_change(myValue, data, wakeupTime = 0):
    if(myValue != None):
        myValue.pendingConfiguration = PendingConfiguration(data, wakeupTime)
        
def build_network_busy_message():
    return jsonify({'result':False, 'reason:':'Controller is too busy', 'state':networkInformations.actualMode, 'send_queue_count':network.controller.send_queue_count, 'state':network.state_str})

def concatenate_list(listValues, separator=';'):
    try:
        if listValues is None:
            return ""
        else:
            if isinstance(listValues, set):
                return separator.join(str(s) for s in listValues)
            return listValues

    except Exception as error:
        add_log_entry(str(error), "error")
    return ""
    
def serialize_node_to_json(device_id):    
    tmpNode = {}    
    if(device_id in network.nodes) :
        myNode = network.nodes[device_id]        
        try:
            timestamp = int(myNode.last_update)
        except TypeError:
            timestamp = int(1)
        try :
            manufacturer_id=int(myNode.manufacturer_id,16)
        except ValueError:
            manufacturer_id=""
        try :
            product_id=int(myNode.product_id,16)
        except ValueError:
            product_id=""
        try :
            product_type=int(myNode.product_type,16)
        except ValueError:
            product_type=""
        try :
            location=int(myNode.location,16)
        except ValueError:
            location=""
        try :
            name=int(myNode.name,16)
        except ValueError:
            name=""
        
        tmpNode['data']= {}
        tmpNode['data']['manufacturerId'] = {'value' : manufacturer_id}
        tmpNode['data']['vendorString'] = {'value' : myNode.manufacturer_name}
        tmpNode['data']['manufacturerProductId'] = {'value' : product_id}
        tmpNode['data']['product_name'] = {'value' : myNode.product_name}
        tmpNode['data']['location'] = {'value' : myNode.location}
        tmpNode['data']['name'] = {'value' : myNode.name}
        tmpNode['data']['version'] = {'value' : myNode.version}    
        tmpNode['data']['manufacturerProductType'] = {'value' : product_type}
        tmpNode['data']['neighbours'] = {'value' : list(myNode.neighbors)}
        tmpNode['data']['isVirtual'] = {'value' : ''}
        if network.controller.node_id == device_id and myNode.basic==1:
            tmpNode['data']['basicType'] = {'value' : 2}
        else:
            tmpNode['data']['basicType'] = {'value' : myNode.basic}
            
        tmpNode['data']['genericType'] = {'value' : myNode.generic}
        tmpNode['data']['specificType'] = {'value' : myNode.specific}
        
        tmpNode['data']['type'] = {'value' : myNode.type}
            
        tmpNode['data']['state'] = {'value' : str(myNode.getNodeQueryStage)}
        if myNode.isNodeAwake():
            tmpNode['data']['isAwake'] = {'value' : 'true',"updateTime":timestamp}
        else :                                                    
            tmpNode['data']['isAwake'] = {'value' : '',"updateTime":timestamp}
        if myNode.isReady:
            tmpNode['data']['isReady'] = {'value' : 'true',"updateTime":timestamp}        
        else :                                                    
            tmpNode['data']['isReady'] = {'value' : 'false',"updateTime":timestamp}
        if myNode.can_wake_up():
            tmpNode['data']['can_wake_up'] = {'value' : 'true'}        
        else :                                                    
            tmpNode['data']['can_wake_up'] = {'value' : 'false'}        
        if myNode.isNodeFailed :
            tmpNode['data']['isFailed'] = {'value' : 'true'}
        if myNode.is_listening_device :
            tmpNode['data']['isListening'] = {'value' : 'true'}
        else :                                                    
            tmpNode['data']['isListening'] = {'value' : 'false'}
        if myNode.is_routing_device:
            tmpNode['data']['isRouting'] = {'value' : 'true'}
        else :                                                    
            tmpNode['data']['isRouting'] = {'value' : 'false'}
        if myNode.is_security_device:
            tmpNode['data']['isSecurity'] = {'value' : 'true'}
        else :                                                    
            tmpNode['data']['isSecurity'] = {'value' : 'false'}     
        if myNode.is_beaming_device:
            tmpNode['data']['isBeaming'] = {'value' : 'true'}
        else :                                                    
            tmpNode['data']['isBeaming'] = {'value' : 'false'}   
        if myNode.is_frequent_listening_device:
            tmpNode['data']['isFrequentListening'] = {'value' : 'true'}
        else :                                                    
            tmpNode['data']['isFrequentListening'] = {'value' : 'false'}     
            
        tmpNode['data']['security'] = {'value' : myNode.security}        
        tmpNode['data']['lastReceived'] = {'updateTime' : timestamp}
        tmpNode['data']['maxBaudRate'] = {'value' : myNode.max_baud_rate}
        
        
        tmpNode['instances'] = {"updateTime":timestamp}    
        tmpNode['groups'] = {"updateTime":timestamp}
            
        for groupIndex in myNode.groups:
            group = myNode.groups[groupIndex]
            tmpNode['groups'][groupIndex] = {"label":group.label, "maximumAssociations": group.max_associations, "associations": concatenate_list(group.associations)}  
        
        
        if hasattr(myNode, 'last_notification') : 
            notification = myNode.last_notification
            tmpNode['last_notification'] = {"receiveTime":notification.receive_time,
                                            "code":notification.code,
                                            "description":notification.description,
                                            "help":notification.help,
                                            "next_wakeup": notification.next_wakeup}
        else:
            tmpNode['last_notification'] = {}
        
            
        #for val in myNode.values.keys() : 
        for val in myNode.values : 
            myValue = myNode.values[val]
            if myValue.genre != 'Basic':
                typeStandard = get_standard_value_type(myValue.type)
            else:
                typeStandard = 'int'
                
            value2 = extract_data(myValue)
            instance2 = change_instance(myValue)
            
            if myValue.index :
                index2=myValue.index
            else :
                index2=0
            
            pendingState = None    
            data_items = concatenate_list(myValue.data_items)
            if hasattr(myValue, 'pendingConfiguration' ):
                if(myValue.pendingConfiguration != None) :
                    pendingState = myValue.pendingConfiguration.state 
            try:
                timestamp = int(myValue.last_update)
            except TypeError:
                timestamp = int(1)
                
            if instance2 not in tmpNode['instances']:
                tmpNode['instances'][instance2] = {"updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'] = {"updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses']['data'] = {"updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class] = {"name": myNode.get_command_class_as_string(myValue.command_class)}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'] = {"updateTime":timestamp}  
                if myNode.isReady==False:
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interviewDone']={}
                if myValue.command_class in [128] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['supported']={"value":True,"type":"bool","updateTime":timestamp}
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['last']={"value":value2,"type":"int","updateTime":timestamp}
                if myValue.command_class in [132] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interval']={"value":value2,"type":"int","updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'][index2] = {"val": value2, "name": myValue.label, "help": myValue.help,"type":typeStandard,"typeZW":myValue.type,"units":myValue.units,"data_items":data_items,"read_only":myValue.is_read_only,"write_only":myValue.is_write_only,"updateTime":timestamp, "genre":myValue.genre, "value_id": myValue.value_id, "poll_intensity":myValue.poll_intensity, "pendingState":pendingState}
                
            elif myValue.command_class not in tmpNode['instances'][instance2]['commandClasses']:
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class] = {"updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class] = {"name": myNode.get_command_class_as_string(myValue.command_class)}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'] = {"updateTime":timestamp}
                if myNode.isReady==False:
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interviewDone']={}
                if myValue.command_class in [128] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['supported']={"value":True,"type":"bool","updateTime":timestamp}
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['last']={"value":value2,"type":"int","updateTime":timestamp}
                if myValue.command_class in [132] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interval']={"value":value2,"type":"int","updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'][index2] ={"val": value2, "name": myValue.label, "help": myValue.help,"type":typeStandard,"typeZW":myValue.type,"units":myValue.units,"data_items":data_items,"read_only":myValue.is_read_only,"write_only":myValue.is_write_only,"updateTime":timestamp, "genre":myValue.genre, "value_id": myValue.value_id, "poll_intensity":myValue.poll_intensity, "pendingState":pendingState}
                
            elif index2 not in tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'] :
                if myValue.command_class in [128] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['supported']={"value":True,"type":"bool","updateTime":timestamp}
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['last']={"value":value2,"type":"int","updateTime":timestamp}
                if myValue.command_class in [132] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interval']={"value":value2,"type":"int","updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'][index2] ={"val": value2, "name": myValue.label, "help": myValue.help,"type":typeStandard,"typeZW":myValue.type,"units":myValue.units,"data_items":data_items,"read_only":myValue.is_read_only,"write_only":myValue.is_write_only,"updateTime":timestamp, "genre":myValue.genre, "value_id": myValue.value_id, "poll_intensity":myValue.poll_intensity, "pendingState":pendingState}
                
            else :
                print 'a'
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return tmpNode

def serialize_controller_to_json():    
    result={}
    controllerdata = {
        'name' : 'controller.data',
        'type' : 'NoneType',
        'value' : 'null'
    }
    result['data']=controllerdata  
    lastExcludedDevice = {
        'name' : 'lastExcludedDevice',
        'type' : 'NoneType',
        'value' : 'null'
    }
    lastIncludedDevice = {
        'name' : 'lastIncludedDevice',
        'type' : 'NoneType',
        'value' : 'null'
    }            
    roles = {'isPrimaryController': network.controller.is_primary_controller,
             'isStaticUpdateController': network.controller.is_static_update_controller,
             'isBridgeController': network.controller.is_bridge_controller
    }
    result['data']['roles']=roles                      
    result['data']['nodeId']={'value':network.controller.node_id}            

    '''
    if the controller is flag as busy I set the coresponding networkInformations.controllerState, 
    if not yet busy, I ignore the actual ControllerMode and assume is idle
    '''
    if networkInformations.controllerIsBusy  :
        if networkInformations.actualMode == ControllerMode.AddDevice:
            result['data']['controllerState']={'value':AddDevice}
        elif networkInformations.actualMode == ControllerMode.RemoveDevice:
            result['data']['controllerState']={'value':RemoveDevice}
        else:
            # not suppose
            result['data']['controllerState']={'value':Idle}
            # I reset the flag
            networkInformations.actualMode = ControllerMode.Idle
    else:
        result['data']['controllerState']={'value':Idle}
        
    result['data']['lastExcludedDevice']=lastExcludedDevice
    result['data']['lastIncludedDevice']=lastIncludedDevice
    result['data']['softwareRevisionVersion']={"value":''+network.controller.ozw_library_version+' '+network.controller.python_library_version}            
    result['data']['notification'] = networkInformations.lastControllerNotification
    result['data']['isBusy'] = {"value" : networkInformations.controllerIsBusy} 
    result['data']['networkstate'] = {"value" : network.state} 
    
    if hasattr(network, 'current_command') :
        current_command = network.current_command
        result['data']['last_command'] = {'received':current_command.timestamp,
                                          'command':current_command.command,
                                          'state':current_command.state,
                                          'command_description':current_command.command_description,
                                          'state_description':current_command.state_description}
    else:
        result['data']['last_command'] = {}
    
    return result

def changes_value_polling(frequence, value):
    if frequence == 0: #disable the value polling for any value
        value.disable_poll()
    elif value.genre == "User" and not value.is_write_only: #we activate the value polling only on user genre value and is not a writeOnly
        value.enable_poll(frequence)
    write_config() 

def convert_user_code_to_hex(value):
    value1 = int(value)
    result = hex(value1)[2:]
    if len(result)==1:
        result = '0'+result
    return result

def set_value(device_id, valueId, data):    
    debug_print("set a value for nodeId:%s valueId:%s data:%s" % (device_id, valueId, data,))
    #check for a valid device_id    
    if device_id == 0xff:        
        return jsonify({'result' : False, 'reason' : 'not a valid nodeId'})
    if(device_id in network.nodes) :
        currentNode = network.nodes[device_id]
        if not currentNode.isReady:
            return jsonify({'result' : False, 'reason' : 'The node must be Ready'})        
        
        for value in currentNode.values:
            if value == valueId:
                zwaveValue = currentNode.values[value]
                lastValue = zwaveValue.data
                #cast data in desired type
                data = zwaveValue.check_data(data=data)        
                if data is None:
                    return jsonify({'result' : False, 'reason' : 'cant convert in desired dataType'})
                result = network.manager.setValue(zwaveValue.value_id, data)
                if result == 0:
                    resultMessage = 'fails'
                elif result == 1:
                    resultMessage = 'succeed'
                elif result == 2:
                    resultMessage = 'fails (valueId not exist)'
                else:
                    resultMessage = 'fails (unknown error)'
                if result == 1 :
                    return jsonify({'result' : True, 'lastValue' : lastValue, 'newValue' : data})
                return jsonify({'result' : False, 'reason' : resultMessage})
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : False, 'reason' : 'value not found'})  

def refresh_background(device_id, values):
    time.sleep(3)
    for val in values:
        if val != None:
            network.nodes[device_id].values[val].refresh()

def get_sleeping_nodes_count():
    sleeping_nodes_count = 0
    for idNode in network.nodes:
        if not network.nodes[idNode].isNodeAwake():
            sleeping_nodes_count += 1
    return sleeping_nodes_count  

def convert_level_to_color(level):
    if level > 99:
        return 255
    return level*255/99

def convert_color_to_level(color):
    if color > 255:
        color = 255
    if color < 0:
        color = 0
    return color*99/255
        
@app.before_first_request
def _run_on_start():    
    global con

@app.route('/',methods = ['GET'])
def index() :
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'index.html')), 'rb') as f:
        content = f.read()
    return content

@app.errorhandler(400)
def not_found400(error):
    add_log_entry('%s %s' % (error, request.url), "error")
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found404(error):
    add_log_entry('%s %s' % (error, request.url), "error") 
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.teardown_appcontext
def close_network(error):
    return error

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[133].Get()',methods = ['GET'])
def refresh_assoc(device_id) :
    debug_print("refresh_assoc for nodeId: %s" % (device_id,))
    config = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            if network.nodes[device_id].values[val].command_class == 133 :
                network.nodes[device_id].values[val].refresh()
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[133].data',methods = ['GET'])
def get_assoc(device_id) :
    debug_print("get_assoc for nodeId: %s" % (device_id,))
    timestamp = int(time.time())
    config = {}
    if(device_id in network.nodes) :
        if network.nodes[device_id].groups :
            config['supported']={'value':'true'}
            for group in network.nodes[device_id].groups :
                config[network.nodes[device_id].groups[group].index]={}
                config[network.nodes[device_id].groups[group].index]['nodes']={'value':list(network.nodes[device_id].groups[group].associations),'updateTime':int(timestamp), 'invalidateTime':0}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[0x85].Remove(<int:value>,<int:value2>)',methods = ['GET'])
def remove_assoc(device_id,value,value2) :    
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    
    config = {}   
    groupIndex=value
    targetNodeId=value2    
    debug_print("remove_assoc for nodeId: %s for group %s with nodeId: %s" % (device_id, groupIndex, targetNodeId,))
    if(device_id in network.nodes) : 
        network.manager.removeAssociation(network.home_id, device_id, groupIndex, targetNodeId)
        config['result']={'value':'ok'}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
        config['result']={'value':'failed'}
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[0x85].Add(<int:value>,<int:value2>)',methods = ['GET'])
def add_assoc(device_id, value, value2) :  
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState})    
    config = {}
    groupIndex=value
    targetNodeId=value2
    debug_print("add_assoc for nodeId: %s for group %s with nodeId: %s" % (device_id, groupIndex, targetNodeId,))
    if(device_id in network.nodes) :
        network.manager.addAssociation(network.home_id, device_id, groupIndex, targetNodeId)
        config['result']={'value':'ok'}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
        config['result']={'value':'failed'}
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].GetPolling()',methods = ['GET'])
def get_polling(device_id) :
    polling = 0
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            if network.nodes[device_id].values[val].poll_intensity > polling :
                polling = network.nodes[device_id].values[val].poll_intensity
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return str(polling)
        
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetPolling(<int:frequence>)',methods = ['GET'])
def set_polling(device_id, frequence) :
    debug_print("set_polling for nodeId: %s at: %s" % (device_id, frequence,))    
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            myValue = network.nodes[device_id].values[val]        
            changes_value_polling(frequence, myValue)    
        return jsonify({'result' : True})  
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : False}) 

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetPolling(<int:value_id>,<int:frequence>)',methods = ['GET'])
def set_polling2(device_id, value_id, frequence) :
    debug_print("set_polling for nodeId: %s ValueId %s at: %s" % (device_id, value_id, frequence,))   
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            myValue = network.nodes[device_id].values[val] 
            if(myValue.value_id==value_id):
                changes_value_polling(frequence, myValue)
                return jsonify({'result' : True})    
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : False,'raison':'valueId not found'})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].SetPolling(<int:frequence>)',methods = ['GET'])
def set_polling_value(device_id, instance_id, cc_id, index, frequence) :
    debug_print("set_polling for nodeId: %s at: %s" % (device_id, frequence,))
    Value = {}
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].index == index:
                myValue = network.nodes[device_id].values[val]
                if frequence == 0:
                    #disable the value polling for any value
                    myValue.disable_poll()
                elif myValue.genre == "User" and myValue.is_write_only == False :
                    #we activate the value polling only on user genre value and is not a writeOnly 
                    myValue.enable_poll(frequence)
        write_config()        
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[132].data.interval.value',methods = ['GET'])
def get_wakeup(device_id) :
    if(device_id in network.nodes) : 
        return str(get_wakeup_interval(device_id))
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')        
    return str('')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetWakeup(<int:time>)',methods = ['GET'])       
def set_wakeup(device_id, time) :    
    debug_print("set wakeup interval for nodeId %s at: %s" % (device_id, time,))
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            myValue = network.nodes[device_id].values[val]
            #we need to find the right valueId
            if myValue.command_class == 132 and myValue.label == "Wake-up Interval":
                return set_value(device_id, myValue.value_id, int(time))   
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')         
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].SetChangeVerified(<int:index>,<int:verified>)',methods = ['GET'])       
def set_change_verified(device_id, instance_id, cc_id, index, verified) :
    """
    Sets a flag indicating whether value changes noted upon a refresh should be verified
    """       
    debug_print("set_change_verified nodeId:%s instance:%s commandClasses:%s index:%s verified:%s" % (device_id, instance_id, cc_id, index, verified,))
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            myValue = network.nodes[device_id].values[val]
            if hex(myValue.command_class)==cc_id and myValue.instance - 1 == instance_id and myValue.index == index:
                network._manager.setChangeVerified(myValue.value_id, bool(verified))    
                return jsonify({'result' : True})
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : False})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Refresh()',methods = ['GET'])
def request_all_config_params(device_id) :    
    """
    Request the values of all known configurable parameters from a device
    """       
    debug_print("Request the values of all known configurable parameters from nodeId %s" % (device_id,))
    result = False
    if(device_id in network.nodes) : 
        network._manager.requestAllConfigParams(network.home_id, device_id)   
        result = True
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning') 
    return jsonify({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Get(<int:index_id>)',methods = ['GET'])
def refresh_config(device_id, index_id) :
    debug_print("refresh_config for nodeId:%s index_id:%s" % (device_id, index_id,))
    config = {}
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            if network.nodes[device_id].values[val].command_class == COMMAND_CLASS_CONFIGURATION and network.nodes[device_id].values[val].index == index_id :
                network.nodes[device_id].values[val].refresh()    
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetDeviceName(<string:location>,<string:name>)',methods = ['GET'])
def set_device_name(device_id, location, name) :    
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState})     
    debug_print("setName for device_id:%s New Name ; '%s'" % (device_id, name,))
    result = False
    if(device_id in network.nodes) :   
        name = name.encode('utf8')
        name = name.replace('+',' ')      
        network.nodes[device_id].set_field('name',name)
        location = location.encode('utf8')
        location = location.replace('+',' ')
        network.nodes[device_id].set_field('location',location)
        result = True
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].data',methods = ['GET'])
def get_config(device_id) :
    debug_print("get_config for nodeId:%s" % (device_id,))
    timestamp = int(time.time())
    config = {}
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            list_values=[]
            if network.nodes[device_id].values[val].command_class == COMMAND_CLASS_CONFIGURATION :
                config[network.nodes[device_id].values[val].index]={}
                if network.nodes[device_id].values[val].type == "List" :
                    value10 = network._manager.getValueListSelectionNum(network.nodes[device_id].values[val].value_id)
                    values = network.nodes[device_id].values[val].data_items
                    for index, valeur in enumerate(values):
                        list_values.append(valeur)
                        if valeur == network.nodes[device_id].values[val].data_as_string :
                            value10 = index
                elif network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data== False:
                    value10 = 0
                elif network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data== True:
                    value10 = 1
                else :
                    value10 = network.nodes[device_id].values[val].data
                config[network.nodes[device_id].values[val].index]['val']={'value2':network.nodes[device_id].values[val].data,'value':value10,'value3':network.nodes[device_id].values[val].label,'value4':list_values,'updateTime':int(timestamp), 'invalidateTime':0}
                config[network.nodes[device_id].values[val].index]['size']={'value':len(str(value10))}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:source_id>].CopyConfigurations(<int:target_id>)',methods = ['GET'])
def copy_configuration(source_id, target_id):
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debug_print("copy_configuration from source_id:%s to target_id:%s'" % (source_id, target_id,))
    result = False
    items = 0
    if(source_id in network.nodes) : 
        if(target_id in network.nodes) : 
            source = network.nodes[source_id]
            target = network.nodes[target_id]            
            if source.manufacturer_id == target.manufacturer_id and source.product_type == target.product_type and source.product_id == target.product_id :
                for val in source.values:
                    configurationValue = source.values[val]
                    if configurationValue.genre == 'Config':
                        if configurationValue.type == 'Button':
                            continue
                        if configurationValue.is_write_only:
                            continue                
                        try:
                            target_value = get_value_by_index(target_id, COMMAND_CLASS_CONFIGURATION, 1, configurationValue.index)
                            if target_value != None:
                                if configurationValue.type == 'List':
                                    network._manager.setValue(target_value.value_id, configurationValue.data)
                                    accepted = True
                                else:
                                    accepted = target.set_config_param(configurationValue.index, configurationValue.data)
                                if accepted :
                                    items +=1
                                    mark_pending_change(target_value, configurationValue.data)                                    
                        except Exception as error:
                            add_log_entry('Copy configuration %s (index:%s) :%s' % (configurationValue.label, configurationValue.index, str(error), ), "error")
                result = items != 0       
            else:
                add_log_entry('The two nodes must be with same: manufacturer_id, product_type and product_id', 'warning') 
        else:
            add_log_entry('This network does not contain any node with the id %s' % (target_id,), 'warning')             
    else:
        add_log_entry('This network does not contain any node with the id %s' % (source_id,), 'warning')
    return jsonify({'result' : result, 'copied_configuration_items': items})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetConfigurationItem(<int:index_id>,<string:item>)',methods = ['GET'])
def set_configuration_item(device_id, value_id, item) :    
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debug_print("set_configuration_item for device_id:%s change valueId:%s to '%s'" % (device_id, value_id, item,))
    result = False
    if(device_id in network.nodes) : 
        result = network._manager.setValue(device_id, value_id, item)
        if (result):
           mark_pending_change(get_value_by_id(device_id, value_id), item) 
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Set(<int:index_id>,<int:value>,<int:size>)',methods = ['GET'])
def set_config(device_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debug_print("set_config for nodeId:%s index:%s, value:%s, size:%s" % (device_id, index_id, value, size,))
    config = {}
    if size==0 :
        size=2
    try :
        if(device_id in network.nodes) :
            network.nodes[device_id].set_config_param(index_id, value, size)
            mark_pending_change(get_value_by_index(device_id, COMMAND_CLASS_CONFIGURATION, 1, index_id), value) 
        else:
            add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})         
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Set(<int:index_id>,<string:value>,<int:size>)',methods = ['GET'])
def set_config2(device_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debug_print("set_config2 for device_id:%s change index:%s to '%s' size:(%s)" % (device_id,index_id,value,size,))
    config = {}
    try :
        if(device_id in network.nodes) :
            for value_id in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
                if network.nodes[device_id].values[value_id].command_class == COMMAND_CLASS_CONFIGURATION and network.nodes[device_id].values[value_id].index==index_id:
                    value=value.replace("@","/")
                    myValue = network.nodes[device_id].values[value_id]
                    if myValue.type == 'Button':
                        if value.lower() == 'true':
                            network._manager.pressButton(myValue.value_id)
                            debug_print("Button pressed") 
                            #mark_pending_change(myValue, 1) 
                        else:
                            network._manager.releaseButton(myValue.value_id)  
                            debug_print("Button released")    
                            #mark_pending_change(myValue, 0)                                                   
                    elif  myValue.type == 'List':
                        network._manager.setValue(value_id, value)                    
                        mark_pending_change(myValue, value) 
                    elif myValue.type == 'Bool':
                        if value.lower() == 'true':
                            value = True
                        else: 
                            value = False
                        network._manager.setValue(value_id, value)                    
                        mark_pending_change(myValue, value)
                        
                        
        else:
            add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})    
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Set(<int:index_id>,<float:value>,<int:size>)',methods = ['GET'])
def set_config3(device_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debug_print("set_config3 for nodeId:%s index:%s, value:%s, size:%s" % (device_id, index_id, value, size,))
    config = {}
    if size==0 :
        size=2
    value=int(value)
    try :
        if(device_id in network.nodes) :
            network.nodes[device_id].set_config_param(index_id, value, size)
            mark_pending_change(get_value_by_index(device_id, COMMAND_CLASS_CONFIGURATION, 1, index_id), value) 
        else:
            add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})    
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<int:value>,<int:size>)',methods = ['GET'])
def set_config4(device_id,instance_id,index_id2,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debug_print("set_config4 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (device_id, instance_id, index_id, value, size,))
    config = {}
    if size==0 :
        size=2
    value=int(value)
    try :
        if(device_id in network.nodes) :
            network.nodes[device_id].set_config_param(index_id, value, size)
            mark_pending_change(get_value_by_index(device_id, COMMAND_CLASS_CONFIGURATION, 1, index_id), value) 
        else:
            add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})    
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<string:value>,<int:size>)',methods = ['GET'])
def set_config5(device_id,instance_id,index_id2,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debug_print("set_config5 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (device_id, instance_id, index_id, value, size,))
    config = {}
    if size==0 :
        size=2
    value=int(value)
    try :
        if(device_id in network.nodes) :
            network.nodes[device_id].set_config_param(index_id, value, size)
            mark_pending_change(get_value_by_index(device_id, COMMAND_CLASS_CONFIGURATION, 1, index_id), value)  
        else:
            add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})    
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<float:value>,<int:size>)',methods = ['GET'])
def set_config6(device_id,instance_id,index_id2,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debug_print("set_config6 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (device_id, instance_id, index_id, value, size,))
    config = {}
    if size==0 :
        size=2
    value=int(value)
    
    try :
        if(device_id in network.nodes) : 
            network.nodes[device_id].set_config_param(index_id, value, size)
            mark_pending_change(get_value_by_index(device_id, COMMAND_CLASS_CONFIGURATION, 1, index_id), value)   
        else:
            add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})    
    return jsonify(config)
            
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses',methods = ['GET'])
def get_command_classes(device_id) :
    result = {}
    debug_print("get_command_classes for nodeId:%s" % (device_id,))
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            result[network.nodes[device_id].values[val].command_class] = {}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(result)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Get()',methods = ['GET'])
def get_value(device_id, instance_id,cc_id) :
    Value = {}
    if(device_id in network.nodes) :        
        try:
            network.nodes[device_id].last_update
        except NameError:
            network.nodes[device_id].last_update=time.time()
     
        now = datetime.datetime.now()
        if isinstance(network.nodes[device_id].last_update, float) :
            last_update = datetime.datetime.fromtimestamp(network.nodes[device_id].last_update)
        else:
            last_update = datetime.datetime.now()
            network.nodes[device_id].last_update=time.time()
        last_delta = last_update + datetime.timedelta(seconds=30)
        #check last update is out of delta time, if the node is not a sleeping device and isReady
        if now > last_delta and network.nodes[device_id].can_wake_up() == False and network.nodes[device_id].isReady:
            #Fetch only the dynamic command class data for a node from the Z-Wave network
            network._manager.requestNodeDynamic(network.home_id,network.nodes[device_id].node_id)
            #mark as updated to avoid a second pass
            network.nodes[device_id].last_update=time.time()
            debug_print("Fetch the dynamic command class data for the node %s" % (device_id,))
        
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value) 

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].val',methods = ['GET'])
def get_value6(device_id, instance_id, index,cc_id) :
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].index == index:
                if network.nodes[device_id].values[val].units=="F" :
                    return str((float(network.nodes[device_id].values[val].data) - 32) * 5.0/9.0)
                elif network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data == True :
                    return str('true')
                elif network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data == False :
                    return str('false')
                else :
                    return str(network.nodes[device_id].values[val].data)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
                
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x63].data[<int:index>].code',methods = ['GET'])
def get_user_code(device_id, instance_id, index) :
    debug_print("getValueRaw nodeId:%s instance:%s commandClasses:%s index:%s" % (device_id, instance_id, hex(COMMAND_CLASS_USER_CODE), index))
    Value = {}
    if(device_id in network.nodes) :        
        myDevice = network.nodes[device_id]
        for val in myDevice.values :  
            myValue = myDevice.values[val]                                  
            if myValue.instance -1 == instance_id and myValue.command_class==COMMAND_CLASS_USER_CODE and myValue.index == index:                            
                userCode = [0,0,0,0,0,0,0,0,0,0] 
                timestamp = int(1)
                rawData = extract_data(myValue) 
                #debug_print("found a value: %s with data: (%s)" % (myValue.label, rawData,))                  
                if rawData != '00000000000000000000' :        
                    try:
                        timestamp = int(myValue.last_update)
                        chunks, chunk_size = len(rawData), len(rawData)/10
                        userCode = [ int(rawData[i:i+chunk_size], 16)  for i in range(0, chunks, chunk_size) ] 
                       
                    except TypeError:
                        timestamp = int(1)                 
                Value = {'invalidateTime': int(time.time() - datetime.timedelta(seconds=30).total_seconds()),
                         'type': get_standard_value_type(myValue.type),
                         'value':userCode,
                         'updateTime':timestamp
                         }                            
                break
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x63].data',methods = ['GET'])
def get_user_codes(device_id, instance_id) :    
    debug_print("getValueAllRaw nodeId:%s instance:%s commandClasses:%s" % (device_id, instance_id, hex(COMMAND_CLASS_USER_CODE),))
    Value = {}
    if(device_id in network.nodes) :        
        myDevice = network.nodes[device_id]
        for val in myDevice.values :  
            myValue = myDevice.values[val]
            if myValue.instance -1 == instance_id and myValue.command_class==COMMAND_CLASS_USER_CODE : 
                if myValue.index == 0 :
                    continue
                if myValue.index > 10 :
                    continue
                rawData = extract_data(myValue)     
                #debug_print("found a value: %s with data: (%s)" % (myValue.label, rawData,))                
                if rawData == '00000000000000000000' :
                    Value[myValue.index] = None
                else:
                    Value[myValue.index] = {}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning') 
    return jsonify(Value)  

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].UserCode.SetRaw(<int:slot_id>,[<string:value>],1)',methods = ['GET'])
def set_user_code(device_id, slot_id, value) :
    debug_print("set_user_code nodeId:%s slot:%s usercode:%s" % (device_id, slot_id, value,))
    Value2 = {}
    for val in network.nodes[device_id].get_values() :
        if network.nodes[device_id].values[val].command_class==COMMAND_CLASS_USER_CODE and network.nodes[device_id].values[val].index == slot_id:
            Value2['data'] = {}
            valueorig = value
            value=binascii.a2b_hex(value)            
            network.nodes[device_id].values[val].data=value
            Value2['data'][val] = {'device':device_id,'slot':slot_id,'val': valueorig}
            return jsonify(Value2) 
    return jsonify(Value2)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[0x63].SetRaw(<int:slot_id>,[<value1>,<value2>,<value3>,<value4>,<value5>,<value6>,<value7>,<value8>,<value9>,<value10>],1)',methods = ['GET'])
def set_user_code2(device_id, slot_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10) :    
    debug_print("set_user_code2 nodeId:%s slot:%s usercode:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (device_id, slot_id, value1,value2,value3,value4,value5,value6,value7,value8,value9,value10,))
    Value2 = {}
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].get_values() :
            if network.nodes[device_id].values[val].command_class==COMMAND_CLASS_USER_CODE and network.nodes[device_id].values[val].index == slot_id:
                Value2['data'] = {}            
                value = convert_user_code_to_hex(value1)+convert_user_code_to_hex(value2)+convert_user_code_to_hex(value3)+convert_user_code_to_hex(value4)+convert_user_code_to_hex(value5)+convert_user_code_to_hex(value6)+convert_user_code_to_hex(value7)+convert_user_code_to_hex(value8)+convert_user_code_to_hex(value9)+convert_user_code_to_hex(value10)
                valueorig = value
                value=binascii.a2b_hex(value)            
                network.nodes[device_id].values[val].data=value
                Value2['data'][val] = {'device':device_id,'slot':slot_id,'val': valueorig}
                return jsonify(Value2) 
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value2)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<int:value>)',methods = ['GET'])
def set_value7(device_id,instance_id, cc_id, index, value) :
    debug_print("set_value7 nodeId:%s instance:%s commandClasses:%s index:%s data:%s" % (device_id, instance_id, cc_id, index, value,))
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                Value['data'] = {}
                network.nodes[device_id].values[val].data=value
                Value['data'][val] = {'val': value}
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                    #dimmer don't report the final value until the value changes is completed
                    waitrefresh=threading.Thread(target=refresh_background, args=(device_id, [val]))
                    waitrefresh.start()
                return jsonify(Value) 
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<float:value>)',methods = ['GET'])
def set_value8(device_id,instance_id, cc_id, index, value) :
    debug_print("set_value8 nodeId:%s instance:%s commandClasses:%s index:%s data:%s" % (device_id, instance_id, cc_id, index, value,))
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                Value['data'] = {}
                network.nodes[device_id].values[val].data=value
                Value['data'][val] = {'val': value}
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                    #dimmer don't report the final value until the value changes is completed
                    waitrefresh=threading.Thread(target=refresh_background, args=(device_id, [val]))
                    waitrefresh.start()
                return jsonify(Value) 
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<string:value>)',methods = ['GET'])
def set_value9(device_id,instance_id, cc_id, index, value) :
    debug_print("set_value8 nodeId:%s instance:%s commandClasses:%s index:%s data:%s" % (device_id, instance_id, cc_id, index, value,))
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                Value['data'] = {}
                network.nodes[device_id].values[val].data=value
                Value['data'][val] = {'val': value}
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                    #dimmer don't report the final value until the value changes is completed
                    waitrefresh=threading.Thread(target=refresh_background, args=(device_id, [val]))
                    waitrefresh.start()
                return jsonify(Value) 
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Set(<string:value>)',methods = ['GET'])
def set_value6(device_id, instance_id, cc_id, value) :
    debug_print("set_value6 nodeId:%s instance:%s commandClasses:%s  data:%s" % (device_id, instance_id, cc_id,  value,))
    Value = {}
    if cc_id == '132' :
        #is a wakeup interval update  
        arr=value.split(",")
        time=int(arr[0])      
        return set_wakeup(device_id, time) 
    if(device_id in network.nodes) :       
        if cc_id == '0x85' :
            # is a add association
            arr=value.split(",")
            group=int(arr[0])
            nodeTarget=int(arr[1])
            try:
                return add_assoc(device_id, group, nodeTarget)
            except ValueError:
                debug_print('Node not Ready for associations')
                Value['result']={'value':'Node not Ready for associations'}
                return jsonify(Value)        
        for val in network.nodes[device_id].get_switches() :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                Value['data'][val] = {'val':network.nodes[device_id].set_switch(val, value)}
                return jsonify(Value)
        for val in network.nodes[device_id].get_dimmers() :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                Value['data'][val] = {'val':network.nodes[device_id].set_dimmer(val, value)}
                return jsonify(Value)
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].instance - 1 == instance_id:
                Value['data'] = {}
                network.nodes[device_id].values[val].data=value
                Value['data'][val] = {'val': value}
                return jsonify(Value) 
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].GetColor()',methods = ['GET'])
def get_color(device_id) :
    debug_print("get_color nodeId:%s" % (device_id,))
    result = {}
    if(device_id in network.nodes) :
        red_level = 0  
        green_level = 0 
        blue_level = 0 
        white_level = 0
        
        for val in network.nodes[device_id].get_values(class_id='All', genre='User', type='Byte', readonly=False, writeonly=False) :
            my_value = network.nodes[device_id].values[val]
            if my_value.command_class != COMMAND_CLASS_SWITCH_MULTILEVEL:
                continue
            if my_value.label != 'Level':
                continue
            if my_value.instance < 2 :
                continue            
            
            if my_value.instance == 3 :                
                red_level = convert_level_to_color(my_value.data)
            elif my_value.instance == 4 :
                green_level = convert_level_to_color(my_value.data)
            elif my_value.instance == 5 :
                blue_level = convert_level_to_color(my_value.data)
            elif my_value.instance == 6 :
                white_level = convert_level_to_color(my_value.data) 
        result['data'] = {'red': red_level, 'green': green_level, 'blue': blue_level, 'white': white_level}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(result)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetColor(<int:red_level>,<int:green_level>,<int:blue_level>,<int:white_level>)',methods = ['GET'])
def set_color(device_id,  red_level, green_level, blue_level, white_level) :
    debug_print("set_color nodeId:%s red:%s green:%s blue:%s white:%s" % (device_id, red_level,  green_level, blue_level, white_level,))
    result = False
    if(device_id in network.nodes) :
        intensity_Value = None
        red_Value = None
        green_Value = None
        blue_Value = None
        white_Value = None
        
        for val in network.nodes[device_id].get_values(class_id='All', genre='User', type='Byte', readonly=False, writeonly=False) :
            my_value = network.nodes[device_id].values[val]
            if my_value.command_class != COMMAND_CLASS_SWITCH_MULTILEVEL:
                continue
            if my_value.label != 'Level':
                continue
            if my_value.instance == 2 :
                continue            
            
            if my_value.instance == 1 :
                intensity_Value = val
            elif my_value.instance == 3 :
                red_Value = val
                my_value.data = convert_color_to_level(red_level)
            elif my_value.instance == 4 :
                green_Value = val
                my_value.data = convert_color_to_level(green_level)
            elif my_value.instance == 5 :
                blue_Value = val
                my_value.data = convert_color_to_level(blue_level)
            elif my_value.instance == 6 :
                white_Value = val
                my_value.data = convert_color_to_level(white_level)
        if red_Value != None and green_Value != None and blue_Value != None  :
            worker=threading.Thread(target=refresh_background, args=(device_id, [intensity_Value]))
            worker.start()
            result = True
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].PressButton()',methods = ['GET'])
def press_button(device_id,instance_id, cc_id, index) :
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                Value['data'] = {}
                network._manager.pressButton(network.nodes[device_id].values[val].value_id)
                Value['data'][val] = {'val': 'true'}
                return jsonify(Value)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].ReleaseButton()',methods = ['GET'])
def release_button(device_id,instance_id, cc_id, index) :
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                Value['data'] = {}
                network._manager.releaseButton(network.nodes[device_id].values[val].value_id)
                Value['data'][val] = {'val': 'true'}
                return jsonify(Value) 
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/controller.AddNodeToNetwork(<int:state>,<int:doSecurity>)',methods = ['GET'])
def start_node_inclusion(state, doSecurity) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    State = {}
    if state == 1 :    
        if can_execute_network_command(0) == False:
            return build_network_busy_message()    
        
        if doSecurity == 1:
            doSecurity = True
            add_log_entry("Start the Inclusion Process to add a Node to the Network with Security CC if the node is supports it")
        else:
            doSecurity = False
            add_log_entry("Start the Inclusion Process to add a Node to the Network")
            
        
        result = network.manager.addNode(network.home_id, doSecurity)
        if result :
            networkInformations.actualMode = ControllerMode.AddDevice            
        return jsonify({'result' : result})      
    elif state == 0 :
        add_log_entry("Start the Inclusion is Cancel" ) 
        network.manager.cancelControllerCommand(network.home_id)
        #TODO: is a work around until got real command notifications
        if networkInformations.actualMode != ControllerMode.Idle:
            networkInformations.actualMode = ControllerMode.Idle
    return jsonify(State)
 
@app.route('/ZWaveAPI/Run/controller.RemoveNodeFromNetwork(<int:state>)',methods = ['GET'])
def start_node_exclusion(state) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    State = {}
    if state == 1 :
        if can_execute_network_command(0) == False:
            return build_network_busy_message()  
        add_log_entry("Remove a Device from the Z-Wave Network (Started)" ) 
        result = network.manager.removeNode(network.home_id)
        if result :
            networkInformations.actualMode = ControllerMode.RemoveDevice            
        return jsonify({'result' : result})
    elif state == 0 :
        add_log_entry("Remove a Device from the Z-Wave Network (Cancel)" ) 
        network.manager.cancelControllerCommand(network.home_id)  
        #TODO: is a work around until got real command notifications
        if networkInformations.actualMode != ControllerMode.Idle:
            networkInformations.actualMode = ControllerMode.Idle      
    return jsonify(State)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RequestNetworkUpdate()',methods = ['GET'])
def request_network_update(device_id) :
    """
    Update the controller with network information from the SUC/SIS.
    """    
    add_log_entry("Update the controller with network information from the SUC/SIS node %s" %(device_id,))
    return jsonify ({'result' : False})    
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    if(device_id in network.nodes) :
        result = network.manager.requestNetworkUpdate(network.home_id, device_id)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result}) 

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RemoveFailedNode()',methods = ['GET'])
def remove_failed_node(device_id) :
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    add_log_entry("Remove a failed node %s" %(device_id,))
    result = False
    if(device_id in network.nodes) :
        result = network.manager.removeFailedNode(network.home_id, device_id)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RequestNodeNeighbourUpdate()',methods = ['GET'])
def request_node_neighbour_update(device_id) :
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    debug_print("request_node_neighbour_update for node %s" %(device_id,)) 
    result = False
    if(device_id in network.nodes) :
        result = network.manager.requestNodeNeighborUpdate(network.home_id, device_id)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})
   
@app.route('/ZWaveAPI/Run/controller.HealthNetwork()',methods = ['GET'])
def health_network() :
    return heal_network()
    
@app.route('/ZWaveAPI/Run/controller.HealNetwork()',methods = ['GET'])
def heal_network(performReturnRoutesInitialization=False) :
    if can_execute_network_command() == False:
        return build_network_busy_message()      
    add_log_entry("heal_network") 
    network._manager.healNetwork(network.home_id, performReturnRoutesInitialization)
    return jsonify ({'result' : True})
    
    return jsonify(State)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].HealNode()',methods = ['GET'])
def heal_node(device_id, performReturnRoutesInitialization=False) :
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    State = {}
    try:
        add_log_entry("HealNode node %s" %(device_id,)) 
        if(device_id in network.nodes) :
            network._manager.healNetworkNode(network.home_id, device_id, performReturnRoutesInitialization)
            return jsonify ({'result' : True})
        else:
            add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
            return jsonify ({'result' : False})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})
    return jsonify(State)    

@app.route('/ZWaveAPI/Run/SerialAPISoftReset()',methods = ['GET'])
def soft_reset() :
    add_log_entry("Controller software Reset")
    try:
        result = network.controller.soft_reset()
        return jsonify ({'result' : result})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})
    
@app.route('/ZWaveAPI/network_start()',methods = ['GET'])
def start_network() :
    State = {}
    add_log_entry('******** The ZWave network is being started ********')
    network.start()
    return jsonify(State)
    
@app.route('/ZWaveAPI/network_stop()',methods = ['GET'])
def stop_network() :
    State = {}    
    network.stop()
    add_log_entry('ZWave network is now stopped')
    return jsonify(State)

@app.route('/ZWaveAPI/assign_return_route(<int:device_id>)',methods = ['GET'])
def assign_return_route(device_id) :
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    add_log_entry("Assign return route")
    try:
        result = network.manager.assignReturnRoute(network.home_id, device_id)
        return jsonify ({'result' : result})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RequestNodeInformation()',methods = ['GET'])
def request_node_information(device_id) :
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    debug_print("request_node_information node %s" %(device_id,)) 
    if(device_id in network.nodes) : 
        return str(network.network.nodes[device_id].request_all_config_params())
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({}) 
    
@app.route('/ZWaveAPI/Data/<int:fromtime>',methods = ['GET'])
def get_device(fromtime):
    timestamp = int(time.time())
    if network :
        networkData={}
        networkData['updateTime']=timestamp
        if network.controller :
            controllerData = serialize_controller_to_json()            
        if network.nodes:
            nodesData = {}
            if fromtime==0 :
                for i in network.nodes:
                    nodesData[i] = serialize_node_to_json(i) 
            elif fromtime :
                changes = {}
                global con
                con.row_factory = lite.Row
                cur = con.cursor() 
                cur.execute("SELECT * FROM Events")
                rows = cur.fetchall()
                cur.execute("DELETE FROM Events")
                for row in rows:
                    if row["Commandclass"] == 0 and row["Value"]=="removed":
                        changes['controller.data.lastExcludedDevice'] = {"value":row["Node"]}
                    elif row["Commandclass"] == 0 and row["Value"]=="added":
                        changes['controller.data.lastIncludedDevice'] = {"value":row["Node"]}
                    elif row["Commandclass"] == 0 and row["Value"] in ["0","1","5"]:
                        changes['controller']={}
                        changes['controller']['controllerState'] = {"value":int(row["Value"])}
                    else :
                        changes['devices.' + str(row["Node"]) + '.instances.' + str(row["Instance"]) + '.commandClasses.' + str(row["Commandclass"]) + '.data.' + str(row["Index_value"])] = {}
                        changes['devices.' + str(row["Node"]) + '.instances.' + str(row["Instance"]) + '.commandClasses.' + str(row["Commandclass"]) + '.data.' + str(row["Index_value"])]["val"]= {"value":row["Value"],"type":row["Type"]}
                return jsonify(changes)     
                        
            else :
                error = {
                'status' : 'error',
                'msg' : 'unable to retrieve ideas'
                }
                return jsonify(error)
                            
            networkData['controller']=controllerData
            networkData['devices']=nodesData
            return jsonify(networkData)
     
        else:
            error = {
                'status' : 'error',
                'msg' : 'unable to retrieve ideas'
            }
            return jsonify(error)
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>]', methods = ['GET'])
def get_serialized_device(device_id):
    if(device_id in network.nodes) :
        return jsonify( serialize_node_to_json(device_id))
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({}) 

@app.route('/ZWaveAPI/Run/network_status()', methods = ['GET'])
def get_network_status(): 
    networkStatus = {'nodesCount': network.nodes_count,
                     'sleepingNodesCount': get_sleeping_nodes_count(),
                     'scenesCount': network.scenes_count,
                     'pollInterval': network.manager.getPollInterval(),
                     'isReady': network.is_ready,
                     'stateDescription': network.state_str,
                     'state': network.state,
                     'controllerCapabilities': concatenate_list(network.controller.capabilities),
                     'controllerNodeCapabilities': concatenate_list(network.controller.node.capabilities),
                     'outgoingSendQueue': network.controller.send_queue_count,
                     'controllerStatistics': network.controller.stats,
                     'devicePath': network.controller.device,
                     'OpenZwaveLibraryVersion': network.manager.getOzwLibraryVersionNumber(),
                     'PythonOpenZwaveLibraryVersion': network.manager.getPythonLibraryVersionNumber(),
                     'neighbors': concatenate_list(network.controller.node.neighbors),
                     'notification' : networkInformations.lastControllerNotification,
                     'isBusy' : networkInformations.controllerIsBusy,
                     'startTime' :networkInformations.startTime,
                     'isPrimaryController': network.controller.is_primary_controller,
                     'isStaticUpdateController': network.controller.is_static_update_controller,
                     'isBridgeController': network.controller.is_bridge_controller
                     }
    if networkInformations.actualMode == ControllerMode.AddDevice:
        networkStatus['controllerState']= AddDevice
    elif networkInformations.actualMode == ControllerMode.RemoveDevice:
        networkStatus['controllerState']= RemoveDevice
    else:
        networkStatus['controllerState']= Idle
    return jsonify(networkStatus)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].ReplaceFailedNode()',methods = ['GET'])
def replace_failed_node(device_id) :
    """
    Replace a failed device with another. If the node is not in the controller failed nodes list, or the node responds, this command will fail.
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    add_log_entry("replace_failed_node node %s" %(device_id,)) 
    result = False
    if(device_id in network.nodes) : 
        result = network.manager.replaceFailedNode(network.home_id, device_id)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SendNodeInformation()',methods = ['GET'])
def send_node_information(device_id) :
    """
    Send a node information frame (NIF).
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    debug_print("send_node_information node %s" %(device_id,)) 
    result = False
    if(device_id in network.nodes) : 
        result = network.manager.sendNodeInformation(network.home_id, device_id)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].HasNodeFailed()',methods = ['GET'])
def has_node_failed(device_id) :
    """
    Check whether a node is in the controller failed nodes list.
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    add_log_entry("has_node_failed node %s" %(device_id,)) 
    result = False
    if(device_id in network.nodes) : 
        result = network.manager.hasNodeFailed(network.home_id, device_id)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RefreshNodeInfo()',methods = ['GET'])
def refresh_node_info(device_id) :
    """
    Trigger the fetching of fixed data about a node. Causes the node data to be obtained from the Z-Wave network in the same way as if it had just been added.
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    debug_print("refresh_node_info node %s" %(device_id,)) 
    result = False
    if(device_id in network.nodes) : 
        result = network.manager.refreshNodeInfo(network.home_id, device_id)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RefreshAllValues()',methods = ['GET'])
def refresh_all_values(device_id):
    """
    A manual refresh of all value of a node, we will receive a refreshed value form value refresh notification
    """
    if device_id == 0xff:
        return jsonify({'result' : False})
    if(device_id in network.nodes) : 
        currentNode = network.nodes[device_id]
        try:
            counter = 0
            debug_print("refresh_all_values node %s" %(device_id,))
            for val in currentNode.values:
                currentValue = currentNode.values[val]
                if currentValue.type == 'Button':
                    continue
                if currentValue.is_write_only:
                    continue
                currentValue.refresh()
                counter+=1            
            return jsonify({'result' : True,'refresh count': counter})
        except Exception as e:
            add_log_entry(str(e), 'error')
            return jsonify ({'error' : str(e)})
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : False})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].TestNetwork()',methods = ['GET'])
def test_network(device_id=0xff, count=3):
    """
    Test network node.
    Sends a series of messages to a network node for testing network reliability.
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    try:
        debug_print("test_network node %s" %(device_id,))
        if device_id == 0xff or device_id == 0:
            network.manager.testNetwork(network.home_id, count)
        else:
            if(device_id in network.nodes) :
                network.manager.testNetworkNode(network.home_id, device_id, count)
                return jsonify({'result' : True})
            else:
                add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
                return jsonify({'result' : False})        
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/CommunicationStatistics',methods = ['GET'])
def get_communication_statistics():
    '''
    "averageRequestRTT": 17, 
    "averageResponseRTT": 0, 
    "lastRequestRTT": 17, 
    "lastResponseRTT": 0, 
    "quality": 0,     
    "receivedCnt": 0, 
    "receivedDups": 0, 
    "receivedTS": "2015-03-12 23:18:05:299 ", 
    "receivedUnsolicited": 0, 
    "retries": 0,     
    "sentCnt": 1,     
    "sentFailed": 0, 
    "sentTS": "2015-03-12 23:18:09:010 "  
    jeedom
    'deliveryTime' == averageRequestRTT
    'delivered' == sentCnt
    '''
    statistics = {}
    for idNode in network.nodes:
        results = network.manager.getNodeStatistics(network.home_id, idNode)
        sentFailed = results['sentFailed']
        sentCnt = results['sentCnt']
        sentOk = sentCnt - sentFailed
        averageRequestRTT = results['averageRequestRTT']
        nodeStatistics = []        
        for x in range(0, sentOk):
            nodeStatistics.append({'date': int(time.time()),
                                  'delivered': True,                              
                                  'deliveryTime': averageRequestRTT,
                                  'packetLength': 1,
                                  })
        for x in range(0, sentFailed):
            nodeStatistics.append({'date': int(time.time()),
                                  'delivered': False,                              
                                  'deliveryTime' : averageRequestRTT,
                                  'packetLength': 1,
                                  })
        statistics[idNode] = nodeStatistics
    return jsonify(statistics)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SendNoOperation()',methods = ['GET'])
def send_no_operation(device_id):
    return test_network(device_id)
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].GetNodeStatistics()',methods = ['GET'])
def get_node_statistics(device_id):
    """
    Retrieve statistics per node.
    """
    if device_id == 0xff:
        return jsonify({'result' : False})
    try:
        if(device_id in network.nodes) :
            queryStageDescription = network.manager.getNodeQueryStage(network.home_id, device_id)
            queryStageCode = network.manager.getNodeQueryStageCode(queryStageDescription)
            return jsonify( {'statistics' : network.manager.getNodeStatistics(network.home_id, device_id),
                    'queryStageCode' : queryStageCode,
                    'queryStageDescription' : queryStageDescription})
        else:
            add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
            return jsonify({'result' : False})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/CancelCommand()',methods = ['GET'])
def cancel_command():
    """
    Cancels any in-progress command running on a controller.
    """
    add_log_entry("Cancels any in-progress command running on a controller.")
    try:
        result = network.manager.cancelControllerCommand(network.home_id)
        if result :
            networkInformations.controllerIsBusy = False
        #TODO: is a work around until got real command notifications
        if networkInformations.actualMode != ControllerMode.Idle:
            networkInformations.actualMode = ControllerMode.Idle
        return jsonify({'result' : result})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/addController()',methods = ['GET'])
def add_controller() :
    """
    Add a new secondary controller to the Z-Wave network.
    """
    return jsonify ({'result' : False})
    

@app.route('/ZWaveAPI/Run/CreateNewPrimary()',methods = ['GET'])
def create_new_primary() :
    """
    Add a new controller to the Z-Wave network. Used when old primary fails. Requires SUC.
    """
    if can_execute_network_command(0) == False:
        return build_network_busy_message()  
    add_log_entry("Add a new controller to the Z-Wave network")
    try:
        result = network.manager.createNewPrimary(network.home_id)
        return jsonify ({'result' : result})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].ReplicationSend()',methods = ['GET'])
def replication_send() :
    """
    Send a NIF frame from the Controller to the Node.
    """
    if can_execute_network_command(0) == False:
        return build_network_busy_message() 
    add_log_entry('Send a NIF frame from the Controller to the Nodeid %s' % (device_id,))
    try:
        result = network.manager.replicationSend(network.home_id, device_id)
        return jsonify ({'result' : result})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/TransferPrimaryRole()',methods = ['GET'])
def transfer_primary_role() :
    """
    Add a new controller to the network and make it the primary.
    The existing primary will become a secondary controller.
    """
    if can_execute_network_command(0) == False:
        return build_network_busy_message()  
    add_log_entry("Add a new controller to the network and make it the primary")
    try:
        result = network.manager.transferPrimaryRole(network.home_id)
        return jsonify ({'result' : result})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/HardReset()',methods = ['GET'])
def hard_reset() :    
    """
    Hard Reset a PC Z-Wave Controller. Resets a controller and erases its network configuration settings. The controller becomes a primary controller ready to add devices to a new network.
    """
    add_log_entry("Resets a controller and erases its network configuration settings")
    try:
        result = network.controller.hard_reset()
        return jsonify ({'result' : result})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].request_all_config_params()',methods = ['GET'])
def request_all_config_parameters(device_id) :
    """
    Request the values of all known configurable parameters from a device.
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    try:
        debug_print("RequestAllConfigParams node %s" %(device_id,))
        result = False
        if(device_id in network.nodes) : 
            result = str(network.network.nodes[device_id].request_all_config_params())
        else:
            add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
        return jsonify ({'result' : result})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/GetControllerStatus()',methods = ['GET'])
def get_controller_status() :
    """
    Get the controller status
    """
    try:
        controllerData = {}
        if network :            
            if network.controller :
                controllerData = serialize_controller_to_json()    
                
        return jsonify ({'result' : controllerData})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'result' : str(e)})

@app.route('/ZWaveAPI/Run/GetOZLogs()',methods = ['GET'])
def get_openzwave_logs() :
    """
    Read the openzwave log file
    """
    try:
        stdin,stdout = os.popen2("tail -n 1000 /opt/python-openzwave/openzwave.log")
        stdin.close()
        lines = stdout.readlines(); stdout.close()
        return jsonify ({'result' : lines})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'result' : str(e)})

@app.route('/ZWaveAPI/Run/GetZWConfig()',methods = ['GET'])
def get_openzwave_config() :
    """
    Read the openzwave config file
    """
    #ensure load latest file version
    try:
        write_config()
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})
    
    fileName = "/opt/python-openzwave/zwcfg_" + network.home_id_str +".xml"
    try:
        with open(fileName, "r") as ins:
            f = ins.read()
        return jsonify ({'result' : f})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e), 'fileName':fileName})
    
@app.route('/JS/Run/zway.devices.SaveData()',methods = ['GET'])
def save_data() :
    return write_config()
    
@app.route('/ZWaveAPI/Run/SaveZWConfig()',methods = ['POST'])
def save_openzwave_config() :
    """
    Save the openzwave config file
    """
    try:
        network.stop()
        add_log_entry('ZWave network is now stopped')
        time.sleep(5)
        fileName = "/opt/python-openzwave/zwcfg_" + network.home_id_str +".xml"
        with open(fileName, "w") as ins:
            ins.write(request.data)
        add_log_entry('******** The ZWave network is being started ********')
        network.start()
        return jsonify ({'result' : True})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e), 'fileName':fileName})
    
@app.route('/ZWaveAPI/Run/WriteZWConfig()',methods = ['GET'])
def write_openzwave_config() :
    """
    Write the openzwave config file
    """
    try:
        write_config()
        return jsonify ({'result' : True})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})
    
@app.route('/ZWaveAPI/Run/SetPollInterval(<int:seconds>,<int:intervalBetweenPolls>)',methods = ['GET'])
def set_poll_interval(seconds, intervalBetweenPolls):
    """
    Set the time period between polls of a node's state.
    """ 
    if can_execute_network_command == False:
        return build_network_busy_message()  
    try:        
        add_log_entry('set_poll_interval seconds:%s, interval Between Polls: %s' % (seconds, bool(intervalBetweenPolls)),)
        if network.state < network.STATE_AWAKED:            
            return jsonify ({'result' : False, 'reason' : 'network state must a minimum set to awaked'})    
        if seconds < 30:
            return jsonify ({'result' : False, 'reason' : 'interval is too small'})  
        network.set_poll_interval(1000*seconds, bool(intervalBetweenPolls))                
        return jsonify ({'result' : True})
    except Exception as e:
        add_log_entry(str(e), 'error')
        return jsonify ({'error' : str(e)})    
    
@app.route('/ZAutomation/api/v1/notifications',methods = ['GET'])
def get_log_infos():
    return jsonify ({'data' : True})
    
if __name__ == '__main__':
    pid = str(os.getpid())
    file(pidfile, 'w').write("%s\n" % pid)
    app.run(host='0.0.0.0',port=int(port_server),debug=False)
