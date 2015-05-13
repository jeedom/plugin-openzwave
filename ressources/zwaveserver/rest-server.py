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
    
import time
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
    elif arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")

def debugPrint(message):
    if log == "Debug":
        addLogEntry(message, "debug")
        
def addLogEntry(message, level="info"):
    print('%s | %s | %s' % (time.strftime('%d-%m-%Y %H:%M:%S',time.localtime()), level, message,)) 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1',int(port_server)))
if result == 0:
    addLogEntry('The port %s is already in use. Please check your openzwave configuration plugin page' % (port_server,), 'error')
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


def signal_handler(signal, frame):
    network.write_config()
    addLogEntry('Graceful stopping the ZWave network.')
    network.stop()
    addLogEntry('The Openzwave REST-server was stopped in a normal way')
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
options.set_suppress_value_refresh(True) # if true, notifications for refreshed (but unchanged) values will not be sent.        
options.set_driver_max_attempts(5)                
#options.addOptionBool("PerformReturnRoutes", True)
#options.addOptionBool("AssumeAwake", True)        
options.addOptionInt("RetryTimeout", 6000)
options.addOptionString("NetworkKey","0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10",True)
options.lock()
       

def saveNodeEvent(node_id, timestamp, value):
    global con
    cur = con.cursor()
    #add a new cache entry for value 
    cur.execute("INSERT INTO Events (Node, Instance, Commandclass, Type, Id, Index_value, Value, Level, Updatetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (node_id, 0, 0, "", "", "", value, 0, timestamp))
    
def saveNodeValueEvent(node_id, timestamp, command_class, index, typeStandard, value, instance):
    global con
    cur = con.cursor()
    #delete the existing cache entry, if exist
    cur.execute("DELETE FROM Events where Node=? AND Commandclass=? AND Instance=? AND Index_value=?", (node_id, command_class, instance, index,))   
    #add a new cache entry for value 
    cur.execute("INSERT INTO Events (Node, Instance, Commandclass, Type, Id, Index_value, Value, Level, Updatetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (node_id, instance, command_class, typeStandard, "", index, value, 0, timestamp))  

def network_started(network):
    addLogEntry("Openzwave network are started with homeId %0.8x." % (network.home_id,))    
    networkInformations.assignControllerNotification(ZWaveController.SIGNAL_CTRL_STARTING, "Network is started")

def network_failed(network):
    addLogEntry("Openzwave network can't load", "error")
    networkInformations.assignControllerNotification(ZWaveController.SIGNAL_CTRL_ERROR, "Network have failed")

def RecoveringFailedNodes():
    return
    for idNode in network.nodes:
        if network.nodes[idNode].isNodeFailed:
            if network.controller.begin_command_has_node_failed(idNode):
                #avoid stress network
                time.sleep(2)

def network_awaked(network):
    addLogEntry("Openzwave network is awake : %d nodes were found (%d are sleeping). All listening nodes are queried, but some sleeping nodes may be missing." % (network.nodes_count, GetSleepingNodesCount(),))
    addLogEntry("Controller is : %s" % (network.controller,))
    networkInformations.assignControllerNotification(ZWaveController.SIGNAL_CTRL_NORMAL, "Network is awaked")
    RecoveringFailedNodes()

def network_ready(network):
    write_config()
    addLogEntry("Openzwave network is ready with %d nodes (%d are sleeping). All nodes are queried, the network is fully functionnal." % (network.nodes_count, GetSleepingNodesCount(),))   
    networkInformations.assignControllerNotification(ZWaveController.SIGNAL_CTRL_NORMAL, "Network is ready")
    RecoveringFailedNodes()

def button_on(network, node):
    addLogEntry('Controller button on pressed event') 
    
def button_off(network, node):
    addLogEntry('Controller button off pressed event') 

def nodes_queried(network):    
    write_config() 
    
def nodes_queried_some_dead(network):
    write_config()  
    addLogEntry("All nodes have been queried, but some node ar mark dead") 
    
def node_added(network, node):
    timestamp = int(time.time())    
    #notify jeedom
    #saveNodeEvent(network.controller.node_id, int(time.time()), Idle)    
    network.nodes[node.node_id].last_update=time.time()    
    addLogEntry('A new node has been added to OpenZWave list. %s.' % (node,))
    saveNodeEvent(node.node_id, timestamp, "added")  

def node_removed(network, node):
    timestamp = int(time.time())    
    #notify jeedom
    #saveNodeEvent(network.controller.node_id, int(time.time()), Idle)
    addLogEntry('A node has been removed from OpenZWave list. %s.' % (node,))
    saveNodeEvent(node.node_id, timestamp, "removed")

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

def canExecuteNetworkCommand(allowed_queue_count=25):
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
        addLogEntry('write configuration xml file')
        time.sleep(1)
    except Exception as error:
        addLogEntry('write_config %s' % (str(error),), "error")
    finally:
        networkInformations.configFileSaveInProgress = False

def essential_node_queries_complete(network, node):   
    debugPrint('The essential queries on a node have been completed. %s' % (node,))    
    timestamp = int(time.time())
    myNode = network.nodes[node.node_id]
    myNode.last_update=time.time()   
    #at this time is not good to save value, I skip this step                                    

def node_queries_complete(network, node):
    debugPrint('All the initialisation queries on a node have been completed. %s' % (node,))
    timestamp = int(time.time())
    myNode = network.nodes[node.node_id]
    myNode.last_update=time.time()  
    #save config 
    write_config() 
    ''' 
    for val in myNode.values :
        myValue = myNode.values[val]        
        if myValue.genre == 'Basic':
            # We skip tracking basic value genre, they are mapped to other user value
            continue        
        saveNodeValueEvent(node.node_id, timestamp, myValue.command_class, myValue.index, get_standard_value_type(myValue.type), extract_data(myValue), change_instance(myValue))
    '''
    
def save_valueAsynchronous(node, value, last_update):
    #debugPrint('A node value has been updated. nodeId:%s value:%s' % (node.node_id, value.label))
    myNode = network.nodes[node.node_id]
    #check if am the realy last update
    if myNode.last_update>last_update:
        return
        
    myNode.last_update=last_update
    #if value.genre != 'Basic':
    value.last_update=last_update 
    saveNodeValueEvent(node.node_id, int(time.time()), value.command_class, value.index, get_standard_value_type(value.type), extract_data(value, False), change_instance(value))    
    
def value_update(network, node, value):    
    try:
        thread = threading.Thread(target=save_valueAsynchronous, args=(node, value, time.time()))
        thread.setDaemon(False)
        thread.start()
    except Exception as error:
        addLogEntry('value_update %s' % (str(error),),"error")
        thread.stop()
        
def scene_event(network, node, scene_id):
    addLogEntry('Scene Activation : %s' % (scene_id,))        
    timestamp = int(time.time())
    typestd = 'int'        
    saveNodeValueEvent(node.node_id, int(time.time()), 91, 0, typestd, scene_id, 0)  
    saveNodeValueEvent(node.node_id, int(time.time()), 43, 0, typestd, scene_id, 0)  
    
def controller_message(state, message, network, controller):    
    #save actual state
    networkInformations.assignControllerNotification(state, message)    
    #notify jeedom
    saveNodeEvent(network.controller.node_id, int(time.time()), networkInformations.computeJeeDomMessage())     
    addLogEntry('Controller state: %s. %s' % (state, message,)) 
    debugPrint('Controller is busy: %s' % (networkInformations.controllerIsBusy,))   

def node_event(network, node, value):
    debugPrint('NodeId %s sends a Basic_Set command to the controller with value %s' % (node.node_id, value,)) 
    for val in network.nodes[node.node_id].values :
        myValue = network.nodes[node.node_id].values[val]
        if myValue.genre == "User" and myValue.is_write_only == False :
            value_update(network, node, myValue)
    """
    the value is actualy the event data, not a zwave value object.
    This is commonly caused when a node sends a Basic_Set command to the controller.
    """  

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

addLogEntry('******** The ZWave network is being started ********')
network.start()

#add node to the network, durring node discovering and after a inclusion 
dispatcher.connect(node_added, ZWaveNetwork.SIGNAL_NODE_ADDED)
# a node is fully removed from network.
dispatcher.connect(node_removed, ZWaveNetwork.SIGNAL_NODE_REMOVED)
# value is add, changed or is refreshed.
dispatcher.connect(value_update, ZWaveNetwork.SIGNAL_VALUE_ADDED)
dispatcher.connect(value_update, ZWaveNetwork.SIGNAL_VALUE_CHANGED)
dispatcher.connect(value_update, ZWaveNetwork.SIGNAL_VALUE_REFRESHED)
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
# keep a track of actual network stage and last message
dispatcher.connect(controller_message, ZWaveController.SIGNAL_CONTROLLER)

addLogEntry('OpenZwave Library Version %s' %(network.manager.getOzwLibraryVersionNumber(),)) 
addLogEntry('Python-OpenZwave Wrapper Version %s' %(network.manager.getPythonLibraryVersionNumber(),)) 

#We wait for the network.
addLogEntry('Waiting for network to become ready')
    
@app.errorhandler(400)
def not_found400(error):
    addLogEntry('%s %s' % (error, request.url), "error")
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found404(error):
    addLogEntry('%s %s' % (error, request.url), "error") 
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def buildNetworkBusyMessage():
    return jsonify({'result':False, 'reason:':'Controller is too busy', 'state':networkInformations.actualMode, 'send_queue_count':network.controller.send_queue_count, 'state':network.state_str})

def concatenateList(listValues, separator=';'):
    try:
        if listValues is None:
            return ""
        else:
            if isinstance(listValues, set):
                return separator.join(str(s) for s in listValues)
            return listValues

    except Exception as error:
        addLogEntry(str(error), "error")
    return ""
    
def get_device_info(device_id):    
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
        
        tmpNode['data']= {}
        tmpNode['data']['manufacturerId'] = {'value' : manufacturer_id}
        tmpNode['data']['vendorString'] = {'value' : myNode.manufacturer_name}
        tmpNode['data']['manufacturerProductId'] = {'value' : product_id}
        tmpNode['data']['product_name'] = {'value' : myNode.product_name}
        tmpNode['data']['name'] = {'value' : myNode.product_name}
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
            tmpNode['groups'][groupIndex] = {"label":group.label, "maximumAssociations": group.max_associations, "associations": concatenateList(group.associations)}  
        
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
                
            data_items = concatenateList(myValue.data_items)
            
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
                if myValue.command_class in [32,37,38,49] and myValue.label in ["Level","Switch"]:
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['level']={"value":value2,"type":typeStandard,"typeZW":myValue.type}
                if myValue.command_class in [128] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['supported']={"value":True,"type":"bool","updateTime":timestamp}
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['last']={"value":value2,"type":"int","updateTime":timestamp}
                if myValue.command_class in [132] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interval']={"value":value2,"type":"int","updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'][index2] = {"val": value2,"value": value2,"level": value2, "name": myValue.label, "help": myValue.help,"type":typeStandard,"typeZW":myValue.type,"units":myValue.units,"data_items":data_items,"read_only":myValue.is_read_only,"write_only":myValue.is_write_only,"updateTime":timestamp, "genre":myValue.genre, "value_id": myValue.value_id, "poll_intensity":myValue.poll_intensity}
            elif myValue.command_class not in tmpNode['instances'][instance2]['commandClasses']:
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class] = {"updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class] = {"name": myNode.get_command_class_as_string(myValue.command_class)}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'] = {"updateTime":timestamp}
                if myNode.isReady==False:
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interviewDone']={}
                if myValue.command_class in [32,37,38,49] and myValue.label in ["Level","Switch"]:
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['level']={"value":value2,"type":typeStandard,"typeZW":myValue.type}
                if myValue.command_class in [128] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['supported']={"value":True,"type":"bool","updateTime":timestamp}
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['last']={"value":value2,"type":"int","updateTime":timestamp}
                if myValue.command_class in [132] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interval']={"value":value2,"type":"int","updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'][index2] ={"val": value2,"value": value2,"level": value2, "name": myValue.label, "help": myValue.help,"type":typeStandard,"typeZW":myValue.type,"units":myValue.units,"data_items":data_items,"read_only":myValue.is_read_only,"write_only":myValue.is_write_only,"updateTime":timestamp, "genre":myValue.genre, "value_id": myValue.value_id, "poll_intensity":myValue.poll_intensity}
            elif index2 not in tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'] :
                if myValue.command_class in [32,37,38,49] and myValue.label in ["Level","Switch"]:
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['level']={"value":value2,"type":typeStandard,"typeZW":myValue.type}
                if myValue.command_class in [128] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['supported']={"value":True,"type":"bool","updateTime":timestamp}
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['last']={"value":value2,"type":"int","updateTime":timestamp}
                if myValue.command_class in [132] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interval']={"value":value2,"type":"int","updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'][index2] ={"val": value2,"value": value2,"level": value2, "name": myValue.label, "help": myValue.help,"type":typeStandard,"typeZW":myValue.type,"units":myValue.units,"data_items":data_items,"read_only":myValue.is_read_only,"write_only":myValue.is_write_only,"updateTime":timestamp, "genre":myValue.genre, "value_id": myValue.value_id, "poll_intensity":myValue.poll_intensity}
            else :
                print 'a'
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return tmpNode

@app.before_first_request
def _run_on_start():    
    global con

@app.route('/',methods = ['GET'])
def index() :
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'index.html')), 'rb') as f:
        content = f.read()
    return content

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[133].Get()',methods = ['GET'])
def refresh_assoc(device_id) :
    debugPrint("refresh_assoc for nodeId: %s" % (device_id,))
    config = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            if network.nodes[device_id].values[val].command_class == 133 :
                network.nodes[device_id].values[val].refresh()
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[133].data',methods = ['GET'])
def get_assoc(device_id) :
    debugPrint("get_assoc for nodeId: %s" % (device_id,))
    timestamp = int(time.time())
    config = {}
    if(device_id in network.nodes) :
        if network.nodes[device_id].groups :
            config['supported']={'value':'true'}
            for group in network.nodes[device_id].groups :
                config[network.nodes[device_id].groups[group].index]={}
                config[network.nodes[device_id].groups[group].index]['nodes']={'value':list(network.nodes[device_id].groups[group].associations),'updateTime':int(timestamp), 'invalidateTime':0}
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[0x85].Remove(<int:value>,<int:value2>)',methods = ['GET'])
def remove_assoc(device_id,value,value2) :    
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    
    config = {}   
    groupIndex=value
    targetNodeId=value2    
    debugPrint("remove_assoc for nodeId: %s for group %s with nodeId: %s" % (device_id, groupIndex, targetNodeId,))
    if(device_id in network.nodes) : 
        network.manager.removeAssociation(network.home_id, device_id, groupIndex, targetNodeId)
        config['result']={'value':'ok'}
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
        config['result']={'value':'failed'}
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[0x85].Add(<int:value>,<int:value2>)',methods = ['GET'])
def add_assoc(device_id, value, value2) :  
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState})    
    config = {}
    groupIndex=value
    targetNodeId=value2
    debugPrint("add_assoc for nodeId: %s for group %s with nodeId: %s" % (device_id, groupIndex, targetNodeId,))
    if(device_id in network.nodes) :
        network.manager.addAssociation(network.home_id, device_id, groupIndex, targetNodeId)
        config['result']={'value':'ok'}
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
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
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return str(polling)

def changes_value_polling(frequence, value):
    if frequence == 0: #disable the value polling for any value
        value.disable_poll()
    elif value.genre == "User" and not value.is_write_only: #we activate the value polling only on user genre value and is not a writeOnly
        value.enable_poll(frequence)
    write_config()    
        
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetPolling(<int:frequence>)',methods = ['GET'])
def set_polling(device_id, frequence) :
    debugPrint("set_polling for nodeId: %s at: %s" % (device_id, frequence,))    
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            myValue = network.nodes[device_id].values[val]        
            changes_value_polling(frequence, myValue)    
        return jsonify({'result' : True})  
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : False}) 

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetPolling(<int:value_id>,<int:frequence>)',methods = ['GET'])
def set_polling2(device_id, value_id, frequence) :
    debugPrint("set_polling for nodeId: %s ValueId %s at: %s" % (device_id, value_id, frequence,))   
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            myValue = network.nodes[device_id].values[val] 
            if(myValue.value_id==value_id):
                changes_value_polling(frequence, myValue)
                return jsonify({'result' : True})    
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : False,'raison':'valueId not found'})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].SetPolling(<int:frequence>)',methods = ['GET'])
def set_polling_value(device_id, instance_id, cc_id, index, frequence) :
    debugPrint("set_polling for nodeId: %s at: %s" % (device_id, frequence,))
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
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[132].data.interval.value',methods = ['GET'])
def get_wakeup(device_id) :
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            myValue = network.nodes[device_id].values[val]
            if myValue.command_class == 132 and myValue.label =="Wake-up Interval":
                return str(network.nodes[device_id].values[val].data_as_string)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')        
    return str('')

def set_value(device_id, valueId, data):    
    debugPrint("set a value for nodeId:%s valueId:%s data:%s" % (device_id, valueId, data,))
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
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : False, 'reason' : 'value not found'})        
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetWakeup(<int:time>)',methods = ['GET'])       
def set_wakeup(device_id, time) :    
    debugPrint("set wakeup interval for nodeId %s at: %s" % (device_id, time,))
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            myValue = network.nodes[device_id].values[val]
            #we need to find the right valueId
            if myValue.command_class == 132 and myValue.label == "Wake-up Interval":
                return set_value(device_id, myValue.value_id, int(time))   
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')         
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].SetChangeVerified(<int:index>,<int:verified>)',methods = ['GET'])       
def setChangeVerified(device_id, instance_id, cc_id, index, verified) :
    """
    Sets a flag indicating whether value changes noted upon a refresh should be verified
    """       
    debugPrint("setChangeVerified nodeId:%s instance:%s commandClasses:%s index:%s verified:%s" % (device_id, instance_id, cc_id, index, verified,))
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            myValue = network.nodes[device_id].values[val]
            if hex(myValue.command_class)==cc_id and myValue.instance - 1 == instance_id and myValue.index == index:
                network._manager.setChangeVerified(myValue.value_id, bool(verified))    
                return jsonify({'result' : True})
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : False})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Refresh()',methods = ['GET'])
def requestAllConfigParams(device_id) :    
    """
    Request the values of all known configurable parameters from a device
    """       
    debugPrint("Request the values of all known configurable parameters from nodeId %s" % (device_id,))
    result = False
    if(device_id in network.nodes) : 
        network._manager.requestAllConfigParams(network.home_id, device_id)   
        result = True
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning') 
    return jsonify({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Get(<int:index_id>)',methods = ['GET'])
def refresh_config(device_id, index_id) :
    debugPrint("refresh_config for nodeId:%s index_id:%s" % (device_id, index_id,))
    config = {}
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            if network.nodes[device_id].values[val].command_class == COMMAND_CLASS_CONFIGURATION and network.nodes[device_id].values[val].index == index_id :
                network.nodes[device_id].values[val].refresh()    
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].data',methods = ['GET'])
def get_config(device_id) :
    debugPrint("get_config for nodeId:%s" % (device_id,))
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
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetConfigurationItem(<int:value_id>,<string:item>)',methods = ['GET'])
def setConfigurationItem(device_id, value_id, item) :    
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debugPrint("setConfigurationItem for device_id:%s change valueId:%s to '%s'" % (device_id, value_id, item,))
    result = False
    if(device_id in network.nodes) : 
        result = network._manager.setValue(value_id, item)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Set(<int:index_id>,<int:value>,<int:size>)',methods = ['GET'])
def set_config(device_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debugPrint("set_config for nodeId:%s index:%s, value:%s, size:%s" % (device_id, index_id, value, size,))
    config = {}
    if size==0 :
        size=2
    try :
        if(device_id in network.nodes) :
            network.nodes[device_id].set_config_param(index_id, value, size)
        else:
            addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})         
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Set(<int:index_id>,<string:value>,<int:size>)',methods = ['GET'])
def set_config2(device_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debugPrint("set_config2 for device_id:%s change index:%s to '%s' size:(%s)" % (device_id,index_id,value,size,))
    config = {}
    try :
        if(device_id in network.nodes) :
            for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='List', readonly='All', writeonly='All') :
                if network.nodes[device_id].values[val].command_class == COMMAND_CLASS_CONFIGURATION and network.nodes[device_id].values[val].index==index_id:
                    network._manager.setValue(val, value)
        else:
            addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})    
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Set(<int:index_id>,<float:value>,<int:size>)',methods = ['GET'])
def set_config3(device_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debugPrint("set_config3 for nodeId:%s index:%s, value:%s, size:%s" % (device_id, index_id, value, size,))
    config = {}
    if size==0 :
        size=2
    value=int(value)
    try :
        if(device_id in network.nodes) :
            network.nodes[device_id].set_config_param(index_id, value, size)
        else:
            addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})    
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x70].Set(<int:index_id>,<int:value>,<int:size>)',methods = ['GET'])
def set_config4(device_id,instance_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debugPrint("set_config4 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (device_id, instance_id, index_id, value, size,))
    config = {}
    if size==0 :
        size=2
    value=int(value)
    try :
        if(device_id in network.nodes) :
            #network.nodes[device_id].values[val].value_id
            network.nodes[device_id].set_config_param(index_id, value, size)
        else:
            addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})    
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x70].Set(<int:index_id>,<string:value>,<int:size>)',methods = ['GET'])
def set_config5(device_id,instance_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debugPrint("set_config5 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (device_id, instance_id, index_id, value, size,))
    config = {}
    if size==0 :
        size=2
    value=int(value)
    try :
        if(device_id in network.nodes) :
            network.nodes[device_id].set_config_param(index_id, value, size)
        else:
            addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})    
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x70].Set(<int:index_id>,<float:value>,<int:size>)',methods = ['GET'])
def set_config6(device_id,instance_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    debugPrint("set_config6 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (device_id, instance_id, index_id, value, size,))
    config = {}
    if size==0 :
        size=2
    value=int(value)
    
    try :
        if(device_id in network.nodes) : 
            network.nodes[device_id].set_config_param(index_id, value, size)
        else:
            addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify({'result' : False, 'reason:': str(e)})    
    return jsonify(config)
            
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses',methods = ['GET'])
def commandClasses(device_id) :
    commandClasses = {}
    debugPrint("commandClasses for nodeId:%s" % (device_id,))
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            commandClasses[network.nodes[device_id].values[val].command_class] = {}
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(commandClasses)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Get()',methods = ['GET'])
def getValue(device_id, instance_id,cc_id) :
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
            debugPrint("Fetch the dynamic command class data for the node %s" % (device_id,))
        
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[<cc_id>].Get()',methods = ['GET'])
def getValue2(device_id, cc_id) :
    #network.manager.RequestNodeDynamic(network.home_id,network.nodes[device_id].values[val].value_id)
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id:
                #network.nodes[device_id].values[val].refresh()
                if network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data == True :
                    return str('true')
                elif network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data == False :
                    return str('false')
                else :
                    return str(network.nodes[device_id].values[val].data)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)    

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[<cc_id>].data.level',methods = ['GET'])
def getLevel(device_id, cc_id) :
    Value = {}
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id:
                if network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data == True :
                    Value['value']=str('true')
                    Value['type']=str('bool')
                    return jsonify(Value)
                elif network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data == False :
                    Value['value']=str('false')
                    Value['type']=str('bool')
                    return jsonify(Value)
                else :
                    Value['value']=str('true')
                    return jsonify(Value)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value) 

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data.level',methods = ['GET'])
def getLevel2(device_id, instance_id, cc_id) :
    Value = {}
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and hex(network.nodes[device_id].values[val].command_class)==cc_id:
                if network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data == True :
                    Value['value']=str('true')
                    Value['type']=str('bool')
                    return jsonify(Value)
                elif network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data == False :
                    Value['value']=str('false')
                    Value['type']=str('bool')
                    return jsonify(Value)
                else :
                    Value['value']=str('true')
                    Value['type']=str('bool')
                    return jsonify(Value)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value) 

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[<cc_id>].data.last',methods = ['GET'])
def getLast(device_id, cc_id) :
    Value = {}
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].values :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id:
                return str(network.nodes[device_id].values[val].data)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value) 

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data.last',methods = ['GET'])
def getLast2(device_id, instance_id, cc_id) :
    Value = {}
    if (device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and hex(network.nodes[device_id].values[val].command_class)==cc_id:
                return str(network.nodes[device_id].values[val].data)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)     

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[<cc_id>].data[<int:index>].val',methods = ['GET'])
def getValue5(device_id, index, cc_id):
    Value = {}
    if (device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].index == index:
                if network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data == True :
                    return str('true')
                elif network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data == False :
                    return str('false')
                else :
                    return str(network.nodes[device_id].values[val].data)  
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value) 

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].val',methods = ['GET'])
def getValue6(device_id, instance_id, index,cc_id) :
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
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
                
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data.currentScene',methods = ['GET'])
def getValueScene(device_id, instance_id, cc_id) :
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].values :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and hex(network.nodes[device_id].values[val].command_class)==cc_id :
                return str(network.nodes[device_id].values[val].data)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
                
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x63].data[<int:index>].code',methods = ['GET'])
def getUserCode(device_id, instance_id, index) :
    debugPrint("getValueRaw nodeId:%s instance:%s commandClasses:%s index:%s" % (device_id, instance_id, hex(COMMAND_CLASS_USER_CODE), index))
    Value = {}
    if(device_id in network.nodes) :        
        myDevice = network.nodes[device_id]
        for val in myDevice.values :  
            myValue = myDevice.values[val]                                  
            if myValue.instance -1 == instance_id and myValue.command_class==COMMAND_CLASS_USER_CODE and myValue.index == index:                            
                userCode = [0,0,0,0,0,0,0,0,0,0] 
                timestamp = int(1)
                rawData = extract_data(myValue) 
                #debugPrint("found a value: %s with data: (%s)" % (myValue.label, rawData,))                  
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
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x63].data',methods = ['GET'])
def getAllUserCode(device_id, instance_id) :    
    debugPrint("getValueAllRaw nodeId:%s instance:%s commandClasses:%s" % (device_id, instance_id, hex(COMMAND_CLASS_USER_CODE),))
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
                #debugPrint("found a value: %s with data: (%s)" % (myValue.label, rawData,))                
                if rawData == '00000000000000000000' :
                    Value[myValue.index] = None
                else:
                    Value[myValue.index] = {}
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning') 
    return jsonify(Value)  

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[<cc_id>].Set(<int:value>)',methods = ['GET'])
def setValue(device_id, cc_id, value) :
    debugPrint("setValue nodeId:%s commandClasses:%s data:%s" % (device_id, cc_id, value,))
    Value = {}
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].get_switches() :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                Value['data'][val] = {'val':network.nodes[device_id].set_switch(val, value)}
                return jsonify(Value)
        for val in network.nodes[device_id].get_dimmers() :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                Value['data'][val] = {'val':network.nodes[device_id].set_dimmer(val, value)}
                if cc_id == COMMAND_CLASS_SWITCH_MULTILEVEL:
                    #dimmer don't report the final value until the value changes is completed
                    time.sleep(1)
                    network.nodes[device_id].values[val].refresh()
                    time.sleep(1)
                    network.nodes[device_id].values[val].refresh()
                return jsonify(Value)
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                network.nodes[device_id].values[val].data=value
                Value['data'][val] = {'val': value}
                return jsonify(Value) 
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning') 
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[<cc_id>].Set(<string:value>)',methods = ['GET'])
def setValue5(device_id, cc_id, value) :
    debugPrint("setValue5 nodeId:%s commandClasses:%s data:%s" % (device_id, cc_id, value,))
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].get_switches() :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                Value['data'][val] = {'val':network.nodes[device_id].set_switch(val, value)}
                return jsonify(Value)
        for val in network.nodes[device_id].get_dimmers() :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                Value['data'][val] = {'val':network.nodes[device_id].set_dimmer(val, value)}
                return jsonify(Value)
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                network.nodes[device_id].values[val].data=value
                Value['data'][val] = {'val': value}
                return jsonify(Value)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].UserCode.SetRaw(<int:slot_id>,[<string:value>],1)',methods = ['GET'])
def setUserCode(device_id, slot_id, value) :
    debugPrint("setUserCode nodeId:%s slot:%s usercode:%s" % (device_id, slot_id, value,))
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

def convertUserCodeHex(value):
    value1 = int(value)
    result = hex(value1)[2:]
    if len(result)==1:
        result = '0'+result
    return result

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[0x63].SetRaw(<int:slot_id>,[<value1>,<value2>,<value3>,<value4>,<value5>,<value6>,<value7>,<value8>,<value9>,<value10>],1)',methods = ['GET'])
def setUserCode2(device_id, slot_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10) :    
    debugPrint("setUserCode2 nodeId:%s slot:%s usercode:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (device_id, slot_id, value1,value2,value3,value4,value5,value6,value7,value8,value9,value10,))
    Value2 = {}
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].get_values() :
            if network.nodes[device_id].values[val].command_class==COMMAND_CLASS_USER_CODE and network.nodes[device_id].values[val].index == slot_id:
                Value2['data'] = {}            
                value = convertUserCodeHex(value1)+convertUserCodeHex(value2)+convertUserCodeHex(value3)+convertUserCodeHex(value4)+convertUserCodeHex(value5)+convertUserCodeHex(value6)+convertUserCodeHex(value7)+convertUserCodeHex(value8)+convertUserCodeHex(value9)+convertUserCodeHex(value10)
                valueorig = value
                value=binascii.a2b_hex(value)            
                network.nodes[device_id].values[val].data=value
                Value2['data'][val] = {'device':device_id,'slot':slot_id,'val': valueorig}
                return jsonify(Value2) 
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value2)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[<cc_id>].Set(<float:value>)',methods = ['GET'])
def setValue4(device_id, cc_id, value) :
    debugPrint("setValue4 nodeId:%s commandClasses:%s data:%s" % (device_id, cc_id, value,))
    Value = {}
    if(device_id in network.nodes) : 
        for val in network.nodes[device_id].get_switches() :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                Value['data'][val] = {'val':network.nodes[device_id].set_switch(val, value)}
                return jsonify(Value)
        for val in network.nodes[device_id].get_dimmers() :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                Value['data'][val] = {'val':network.nodes[device_id].set_dimmer(val, value)}
                return jsonify(Value)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<int:value>)',methods = ['GET'])
def setValue7(device_id,instance_id, cc_id, index, value) :
    debugPrint("setValue7 nodeId:%s instance:%s commandClasses:%s index:%s data:%s" % (device_id, instance_id, cc_id, index, value,))
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                Value['data'] = {}
                network.nodes[device_id].values[val].data=value
                Value['data'][val] = {'val': value}
                if cc_id == COMMAND_CLASS_SWITCH_MULTILEVEL:
                    #dimmer don't report the final value until the value changes is completed
                    time.sleep(1)
                    network.nodes[device_id].values[val].refresh()
                    time.sleep(1)
                    network.nodes[device_id].values[val].refresh()
                return jsonify(Value) 
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<float:value>)',methods = ['GET'])
def setValue8(device_id,instance_id, cc_id, index, value) :
    debugPrint("setValue8 nodeId:%s instance:%s commandClasses:%s index:%s data:%s" % (device_id, instance_id, cc_id, index, value,))
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                Value['data'] = {}
                network.nodes[device_id].values[val].data=value
                Value['data'][val] = {'val': value}
                if cc_id == COMMAND_CLASS_SWITCH_MULTILEVEL:
                    #dimmer don't report the final value until the value changes is completed
                    time.sleep(1)
                    network.nodes[device_id].values[val].refresh()
                    time.sleep(1)
                    network.nodes[device_id].values[val].refresh()
                return jsonify(Value) 
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Set(<string:value>)',methods = ['GET'])
def setValue6(device_id, instance_id, cc_id, value) :
    debugPrint("setValue6 nodeId:%s instance:%s commandClasses:%s  data:%s" % (device_id, instance_id, cc_id,  value,))
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
                debugPrint('Node not Ready for associations')
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
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Set(<float:value>)',methods = ['GET'])
def setValue2(device_id, instance_id, cc_id, value) :
    debugPrint("setValue2 nodeId:%s instance:%s commandClasses:%s data:%s" % (device_id, instance_id, cc_id, value,))
    Value = {}
    if(device_id in network.nodes) : 
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
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Set(<int:value>)',methods = ['GET'])
def setValue3(device_id, instance_id, cc_id, value) :
    debugPrint("setValue3 nodeId:%s instance:%s commandClasses:%s data:%s" % (device_id, instance_id, cc_id, value,))
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].get_switches() :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                Value['data'][val] = {'val':network.nodes[device_id].set_switch(val, value)}
                return jsonify(Value)
        for val in network.nodes[device_id].get_dimmers() :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and hex(network.nodes[device_id].values[val].command_class)==cc_id:
                Value['data'] = {}
                Value['data'][val] = {'val':network.nodes[device_id].set_dimmer(val, value)}
                if cc_id == COMMAND_CLASS_SWITCH_MULTILEVEL:
                    #dimmer don't report the final value until the value changes is completed
                    time.sleep(1)
                    network.nodes[device_id].values[val].refresh()
                    time.sleep(1)
                    network.nodes[device_id].values[val].refresh()
                return jsonify(Value)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].PressButton()',methods = ['GET'])
def pressButton(device_id,instance_id, cc_id, index) :
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                Value['data'] = {}
                network._manager.pressButton(network.nodes[device_id].values[val].value_id)
                Value['data'][val] = {'val': 'true'}
                return jsonify(Value)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].ReleaseButton()',methods = ['GET'])
def releaseButton(device_id,instance_id, cc_id, index) :
    Value = {}
    if(device_id in network.nodes) :
        for val in network.nodes[device_id].get_values(class_id='All', genre='All', type='All', readonly='All', writeonly='All') :
            if hex(network.nodes[device_id].values[val].command_class)==cc_id and network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                Value['data'] = {}
                network._manager.releaseButton(network.nodes[device_id].values[val].value_id)
                Value['data'][val] = {'val': 'true'}
                return jsonify(Value) 
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/InspectQueue',methods = ['GET'])
def InspectQueue() :
    tmpQueue = {}
    for i in range(0,network.controller.send_queue_count):
        tmpQueue[i]=0
    return jsonify(tmpQueue)

@app.route('/ZWaveAPI/Run/controller.AddNodeToNetwork(<int:state>)',methods = ['GET'])
def AddNodeToNetwork(state) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    State = {}
    if state == 1 :    
        if canExecuteNetworkCommand(0) == False:
            return buildNetworkBusyMessage()    
        addLogEntry("AddNodeToNetwork Started" )
        result = network.controller.begin_command_add_device('true') 
        if result :
            networkInformations.actualMode = ControllerMode.AddDevice            
        return jsonify({'result' : result})      
    elif state == 0 :
        addLogEntry("AddNodeToNetwork Cancel" ) 
        network.controller.cancel_command()
    return jsonify(State)
 
@app.route('/ZWaveAPI/Run/controller.RemoveNodeFromNetwork(<int:state>)',methods = ['GET'])
def RemoveNodeFromNetwork(state) :
    if networkInformations.controllerIsBusy:
        return jsonify({'result' : False, 'reason:': 'Controller is busy', 'state' : networkInformations.controllerState}) 
    State = {}
    if state == 1 :
        if canExecuteNetworkCommand(0) == False:
            return buildNetworkBusyMessage()  
        addLogEntry("RemoveNodeFromNetwork Started" ) 
        result = network.controller.begin_command_remove_device('true')
        if result :
            networkInformations.actualMode = ControllerMode.RemoveDevice            
        return jsonify({'result' : result})
    elif state == 0 :
        addLogEntry("RemoveNodeFromNetwork Cancel" ) 
        network.controller.cancel_command()
    return jsonify(State)

@app.route('/ZWaveAPI/Run/controller.RequestNetworkUpdate()',methods = ['GET'])
def RequestNetworkUpdate() :
    """
    Update the controller with network information from the SUC/SIS.
    """    
    return jsonify ({'result' : False})    
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    try:
        debugPrint("RequestNetworkUpdate Started" ) 
        result = network.controller.begin_command_request_network_update()
        return jsonify ({'result' : result})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RemoveFailedNode()',methods = ['GET'])
def RemoveFailedNode(device_id) :
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    addLogEntry("Remove a failed node %s" %(device_id,))
    result = False
    if(device_id in network.nodes) :
        result = network.controller.begin_command_remove_failed_node(device_id)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RequestNodeNeighbourUpdate()',methods = ['GET'])
def RequestNodeNeighbourUpdate(device_id) :
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    debugPrint("RequestNodeNeighbourUpdate for node %s" %(device_id,)) 
    result = False
    if(device_id in network.nodes) :
        result = network.controller.begin_command_request_node_neigbhor_update(device_id)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})
   
@app.route('/ZWaveAPI/Run/controller.HealthNetwork()',methods = ['GET'])
def HealthNetwork() :
    return HealNetwork()
    
@app.route('/ZWaveAPI/Run/controller.HealNetwork()',methods = ['GET'])
def HealNetwork(performReturnRoutesInitialization=False) :
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    State = {}
    addLogEntry("HealNetwork") 
    network._manager.healNetwork(network.home_id, performReturnRoutesInitialization)
    return jsonify ({'result' : True})
    
    return jsonify(State)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].HealNode()',methods = ['GET'])
def HealNode(device_id, performReturnRoutesInitialization=False) :
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    State = {}
    try:
        addLogEntry("HealNode node %s" %(device_id,)) 
        if(device_id in network.nodes) :
            network._manager.healNetworkNode(network.home_id, device_id, performReturnRoutesInitialization)
            return jsonify ({'result' : True})
        else:
            addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
            return jsonify ({'result' : False})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})
    return jsonify(State)    

@app.route('/ZWaveAPI/Run/SerialAPISoftReset()',methods = ['GET'])
def SerialAPISoftReset() :
    addLogEntry("Controller software Reset")
    try:
        result = network.controller.soft_reset()
        return jsonify ({'result' : result})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})
    
@app.route('/ZWaveAPI/network_start()',methods = ['GET'])
def start_network() :
    State = {}
    addLogEntry('******** The ZWave network is being started ********')
    network.start()
    return jsonify(State)
    
@app.route('/ZWaveAPI/network_stop()',methods = ['GET'])
def stop_network() :
    State = {}    
    network.stop()
    addLogEntry('ZWave network is now stopped')
    return jsonify(State)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RequestNodeInformation()',methods = ['GET'])
def RequestNodeInformation(device_id) :
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    debugPrint("RequestNodeInformation node %s" %(device_id,)) 
    if(device_id in network.nodes) : 
        return str(network.network.nodes[device_id].request_all_config_params())
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({}) 

@app.route('/ZWaveAPI/Data/<int:fromtime>',methods = ['GET'])
def get_device(fromtime):
    timestamp = int(time.time())
    if network :
        public_network={}
        public_network['updateTime']=timestamp
        if network.controller :
            public_controller={}
            controllerdata = {
                'name' : 'controller.data',
                'type' : 'NoneType',
                'value' : 'null'
            }
            public_controller['data']=controllerdata  
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
            public_controller['data']['roles']=roles                      
            public_controller['data']['nodeId']={'value':network.controller.node_id}            
                        
            #if the controller is flag as busy I set the coresponding networkInformations.controllerState, if not yet busy, I ignore the actual ControllerMode
            if networkInformations.controllerIsBusy == False :
                if networkInformations.actualMode == ControllerMode.AddDevice:
                    public_controller['data']['controllerState']={'value':AddDevice}
                elif networkInformations.actualMode == ControllerMode.RemoveDevice:
                    public_controller['data']['controllerState']={'value':RemoveDevice}
                else:
                    # not suppose
                    public_controller['data']['controllerState']={'value':Idle}
                    # I reset the flag
                    networkInformations.actualMode = ControllerMode.Idle
            else:
                public_controller['data']['controllerState']={'value':Idle}
                
            public_controller['data']['lastExcludedDevice']=lastExcludedDevice
            public_controller['data']['lastIncludedDevice']=lastIncludedDevice
            public_controller['data']['softwareRevisionVersion']={"value":''+network.controller.ozw_library_version+' '+network.controller.python_library_version}            
            public_controller['data']['notification'] = networkInformations.lastControllerNotification
            public_controller['data']['isBusy'] = {"value" : networkInformations.controllerIsBusy} 
            public_controller['data']['networkstate'] = {"value" : network.state} 
            
        if network.nodes:
            public_nodes = {}
            if fromtime==0 :
                for i in network.nodes:
                    public_nodes[i] = get_device_info(i) 
            elif fromtime :
                changes = {}
                global con
                con.row_factory = lite.Row
                cur = con.cursor() 
                cur.execute("SELECT * FROM Events")
                rows = cur.fetchall()
                timestamp = int(time.time())
                changes['updateTime']=timestamp
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
                        if row["Commandclass"] in [32,37,38,48,49] :
                            changes['devices.' + str(row["Node"]) + '.instances.' + str(row["Instance"]) + '.commandClasses.' + str(row["Commandclass"]) + '.data.level'] = {"value":row["Value"],"type": row["Type"],"updateTime": row["updateTime"]}
                            changes['devices.' + str(row["Node"]) + '.instances.' + str(row["Instance"]) + '.commandClasses.' + str(row["Commandclass"]) + '.data.' + str(row["Index_value"]) + '.level'] = {"value":row["Value"],"type": row["Type"],"updateTime": row["updateTime"]}
                        if row["Commandclass"] in [43,91] :
                            changes['devices.' + str(row["Node"]) + '.instances.' + str(row["Instance"]) + '.commandClasses.' + str(row["Commandclass"]) + '.data.currentScene'] = {"value":row["Value"],"type": "int","updateTime": row["updateTime"]}
                            changes['devices.' + str(row["Node"]) + '.instances.' + str(row["Instance"]) + '.commandClasses.' + str(row["Commandclass"]) + '.data.' + str(row["Index_value"]) + '.currentScene'] = {"value":row["Value"],"type": "int","updateTime": row["updateTime"]}
                        if row["Commandclass"] in [156] :
                            changes['devices.' + str(row["Node"]) + '.instances.' + str(row["Instance"]) + '.commandClasses.' + str(row["Commandclass"]) + '.data.' + str(row["Index_value"]) + '.sensorState'] = {"value":row["Value"],"type": "int","updateTime": row["updateTime"]}
                        if row["Commandclass"] in [128] :
                            changes['devices.' + str(row["Node"]) + '.instances.' + str(row["Instance"]) + '.commandClasses.' + str(row["Commandclass"]) + '.data.supported'] = {"value":"true","type": "bool","updateTime": row["updateTime"]}
                            changes['devices.' + str(row["Node"]) + '.instances.' + str(row["Instance"]) + '.commandClasses.' + str(row["Commandclass"]) + '.data.last'] = {"value":row["Value"],"type": "int","updateTime": row["updateTime"]}
                        changes['devices.' + str(row["Node"]) + '.instances.' + str(row["Instance"]) + '.commandClasses.' + str(row["Commandclass"]) + '.data.' + str(row["Index_value"])]["val"]= {"value":row["Value"],"type":row["Type"],"updateTime": row["updateTime"]}
                cur.execute("DELETE FROM Events")
                return jsonify(changes)
                 
            else :
                error = {
                'status' : 'error',
                'msg' : 'unable to retrieve ideas'
                }
                return jsonify(error)
                
            public_network['controller']=public_controller
            public_network['devices']=public_nodes
            return jsonify(public_network)
     
        else:
            error = {
                'status' : 'error',
                'msg' : 'unable to retrieve ideas'
            }
            return jsonify(error)
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>]', methods = ['GET'])
def run_devices(device_id):
    if(device_id in network.nodes) :
        return jsonify( get_device_info(device_id))
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({}) 

@app.teardown_appcontext
def close_network(error):
    return error
    
def GetSleepingNodesCount():
    sleeping_nodes_count = 0
    for idNode in network.nodes:
        if not network.nodes[idNode].isNodeAwake():
            sleeping_nodes_count += 1
    return sleeping_nodes_count  

@app.route('/ZWaveAPI/Run/network_status()', methods = ['GET'])
def GetNetworkStatus(): 
    networkStatus = {'nodesCount': network.nodes_count,
                     'sleepingNodesCount': GetSleepingNodesCount(),
                     'scenesCount': network.scenes_count,
                     'pollInterval': network.manager.getPollInterval(),
                     'isReady': network.is_ready,
                     'stateDescription': network.state_str,
                     'state': network.state,
                     'controllerCapabilities': concatenateList(network.controller.capabilities),
                     'controllerNodeCapabilities': concatenateList(network.controller.node.capabilities),
                     'outgoingSendQueue': network.controller.send_queue_count,
                     'controllerStatistics': network.controller.stats,
                     'devicePath': network.controller.device,
                     'OpenZwaveLibraryVersion': network.manager.getOzwLibraryVersionNumber(),
                     'PythonOpenZwaveLibraryVersion': network.manager.getPythonLibraryVersionNumber(),
                     'neighbors': concatenateList(network.controller.node.neighbors),
                     'notification' : networkInformations.lastControllerNotification,
                     'isBusy' : networkInformations.controllerIsBusy,
                     'startTime' :networkInformations.startTime,
                     'isPrimaryController': network.controller.is_primary_controller,
                     'isStaticUpdateController': network.controller.is_static_update_controller,
                     'isBridgeController': network.controller.is_bridge_controller
                     }
    return jsonify(networkStatus)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].ReplaceFailedNode()',methods = ['GET'])
def ReplaceFailedNode(device_id) :
    """
    Replace a failed device with another. If the node is not in the controller failed nodes list, or the node responds, this command will fail.
    """
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    addLogEntry("ReplaceFailedNode node %s" %(device_id,)) 
    result = False
    if(device_id in network.nodes) : 
        result = network.controller.begin_command_replace_failed_node(device_id)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SendNodeInformation()',methods = ['GET'])
def SendNodeInformation(device_id) :
    """
    Send a node information frame (NIF).
    """
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    debugPrint("SendNodeInformation node %s" %(device_id,)) 
    result = False
    if(device_id in network.nodes) : 
        result = network.controller.begin_command_send_node_information(device_id)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].HasNodeFailed()',methods = ['GET'])
def HasNodeFailed(device_id) :
    """
    Check whether a node is in the controller failed nodes list.
    """
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    addLogEntry("HasNodeFailed node %s" %(device_id,)) 
    result = False
    if(device_id in network.nodes) : 
        result = network.controller.begin_command_has_node_failed(device_id)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RefreshNodeInfo()',methods = ['GET'])
def RefreshNodeInfo(device_id) :
    """
    Trigger the fetching of fixed data about a node. Causes the node data to be obtained from the Z-Wave network in the same way as if it had just been added.
    """
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    debugPrint("RefreshNodeInfo node %s" %(device_id,)) 
    result = False
    if(device_id in network.nodes) : 
        result = network.manager.refreshNodeInfo(network.home_id, device_id)
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : result})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RefreshAllValues()',methods = ['GET'])
def RefreshAllValues(device_id):
    """
    A manual refresh of all value of a node, we will receive a refreshed value form value refresh notification
    """
    if device_id == 0xff:
        return jsonify({'result' : False})
    if(device_id in network.nodes) : 
        currentNode = network.nodes[device_id]
        try:
            counter = 0
            debugPrint("RefreshAllValues node %s" %(device_id,))
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
            addLogEntry(str(e), 'error')
            return jsonify ({'error' : str(e)})
    else:
        addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify ({'result' : False})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].TestNetwork()',methods = ['GET'])
def TestNetwork(device_id=0xff, count=3):
    """
    Test network node.
    Sends a series of messages to a network node for testing network reliability.
    """
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    try:
        debugPrint("TestNetwork node %s" %(device_id,))
        if device_id == 0xff:
            network.manager.testNetwork(network.home_id, count)
        else:
            if(device_id in network.nodes) :
                network.manager.testNetworkNode(network.home_id, device_id, count)
                return jsonify({'result' : True})
            else:
                addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
                return jsonify({'result' : False})        
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/CommunicationStatistics',methods = ['GET'])
def CommunicationStatistics():
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
def SendNoOperation(device_id):
    return TestNetwork(device_id)
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].GetNodeStatistics()',methods = ['GET'])
def GetNodeStatistics(device_id):
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
            addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
            return jsonify({'result' : False})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/CancelCommand()',methods = ['GET'])
def CancelCommand():
    """
    Cancels any in-progress command running on a controller.
    """
    addLogEntry("Cancels any in-progress command running on a controller.")
    try:
        result = network.controller.cancel_command()
        if result :
            networkInformations.controllerIsBusy = False
        return jsonify({'result' : result})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/addController()',methods = ['GET'])
def addController() :
    """
    Add a new secondary controller to the Z-Wave network.
    """
    if canExecuteNetworkCommand(0) == False:
        return buildNetworkBusyMessage()  
    addLogEntry("Add a new secondary controller to the Z-Wave network")
    try:
        result = network.controller.begin_command_add_controller()
        return jsonify ({'result' : result})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/CreateNewPrimary()',methods = ['GET'])
def CreateNewPrimary() :
    """
    Add a new controller to the Z-Wave network. Used when old primary fails. Requires SUC.
    """
    if canExecuteNetworkCommand(0) == False:
        return buildNetworkBusyMessage()  
    addLogEntry("Add a new controller to the Z-Wave network")
    try:
        result = network.controller.begin_command_create_new_primary()
        return jsonify ({'result' : result})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/ReplicationSend()',methods = ['GET'])
def ReplicationSend() :
    """
    Send information from primary to secondary.
    """
    if canExecuteNetworkCommand(0) == False:
        return buildNetworkBusyMessage() 
    addLogEntry("Send information from primary to secondary")
    try:
        result = network.controller.begin_command_replication_send('true')
        return jsonify ({'result' : result})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/TransferPrimaryRole()',methods = ['GET'])
def TransferPrimaryRole() :
    """
    Make a different controller the primary. The existing primary will become a secondary controller.
    """
    if canExecuteNetworkCommand(0) == False:
        return buildNetworkBusyMessage()  
    addLogEntry("Make a different controller the primary")
    try:
        result = network.controller.begin_command_transfer_primary_role('true')
        return jsonify ({'result' : result})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/HardReset()',methods = ['GET'])
def HardReset() :    
    """
    Hard Reset a PC Z-Wave Controller. Resets a controller and erases its network configuration settings. The controller becomes a primary controller ready to add devices to a new network.
    """
    addLogEntry("Resets a controller and erases its network configuration settings")
    try:
        result = network.controller.hard_reset()
        return jsonify ({'result' : result})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].request_all_config_params()',methods = ['GET'])
def RequestAllConfigParams(device_id) :
    """
    Request the values of all known configurable parameters from a device.
    """
    if canExecuteNetworkCommand() == False:
        return buildNetworkBusyMessage()  
    try:
        debugPrint("RequestAllConfigParams node %s" %(device_id,))
        result = False
        if(device_id in network.nodes) : 
            result = str(network.network.nodes[device_id].request_all_config_params())
        else:
            addLogEntry('This network does not contain any node with the id %s' % (device_id,), 'warning')
        return jsonify ({'result' : result})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})

@app.route('/ZWaveAPI/Run/GetControllerStatus()',methods = ['GET'])
def GetControllerStatus() :
    """
    Get the controller status
    """
    try:
        timestamp = int(time.time())
        if network :
            public_network={}
            public_network['updateTime']=timestamp
            if network.controller :
                public_controller={}
                controllerdata = {
                    'name' : 'controller.data',
                    'type' : 'NoneType',
                    'value' : 'null'
                }
                public_controller['data']=controllerdata  
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
                public_controller['data']['roles']=roles                      
                public_controller['data']['nodeId']={'value':network.controller.node_id}            
                            
                #if the controller is flag as busy I set the coresponding networkInformations.controllerState, if not yet busy, I ignore the actual ControllerMode
                if networkInformations.controllerIsBusy == False :
                    if networkInformations.actualMode == ControllerMode.AddDevice:
                        public_controller['data']['controllerState']={'value':AddDevice}
                    elif networkInformations.actualMode == ControllerMode.RemoveDevice:
                        public_controller['data']['controllerState']={'value':RemoveDevice}
                    else:
                        # not suppose
                        public_controller['data']['controllerState']={'value':Idle}
                        # I reset the flag
                        networkInformations.actualMode = ControllerMode.Idle
                else:
                    public_controller['data']['controllerState']={'value':Idle}
                    
                public_controller['data']['lastExcludedDevice']=lastExcludedDevice
                public_controller['data']['lastIncludedDevice']=lastIncludedDevice
                public_controller['data']['softwareRevisionVersion']={"value":''+network.controller.ozw_library_version+' '+network.controller.python_library_version}            
                public_controller['data']['notification'] = networkInformations.lastControllerNotification
                public_controller['data']['isBusy'] = {"value" : networkInformations.controllerIsBusy} 
                public_controller['data']['networkstate'] = {"value" : network.state} 
        return jsonify ({'result' : public_controller})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'result' : str(e)})

@app.route('/ZWaveAPI/Run/GetOZLogs()',methods = ['GET'])
def GetOZLogs() :
    """
    Read the openzwave log file
    """
    try:
        stdin,stdout = os.popen2("tail -n 1000 /opt/python-openzwave/openzwave.log")
        stdin.close()
        lines = stdout.readlines(); stdout.close()
        return jsonify ({'result' : lines})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'result' : str(e)})

@app.route('/ZWaveAPI/Run/GetZWConfig()',methods = ['GET'])
def GetZWConfig() :
    """
    Read the openzwave config file
    """
    #ensure load latest file version
    try:
        write_config()
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})
    
    fileName = "/opt/python-openzwave/zwcfg_" + network.home_id_str +".xml"
    try:
        with open(fileName, "r") as ins:
            f = ins.read()
        return jsonify ({'result' : f})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e), 'fileName':fileName})
    
@app.route('/JS/Run/zway.devices.SaveData()',methods = ['GET'])
def SaveData() :
    return write_config()
    
@app.route('/ZWaveAPI/Run/SaveZWConfig()',methods = ['POST'])
def SaveZWConfig() :
    """
    Save the openzwave config file
    """
    try:
        network.stop()
        addLogEntry('ZWave network is now stopped')
        time.sleep(5)
        fileName = "/opt/python-openzwave/zwcfg_" + network.home_id_str +".xml"
        with open(fileName, "w") as ins:
            ins.write(request.data)
        addLogEntry('******** The ZWave network is being started ********')
        network.start()
        return jsonify ({'result' : True})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e), 'fileName':fileName})
    
@app.route('/ZWaveAPI/Run/WriteZWConfig()',methods = ['GET'])
def WriteZWConfig() :
    """
    Write the openzwave config file
    """
    try:
        write_config()
        return jsonify ({'result' : True})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})
    
@app.route('/ZWaveAPI/Run/SetPollInterval(<int:seconds>,<int:intervalBetweenPolls>)',methods = ['GET'])
def SetPollInterval(seconds, intervalBetweenPolls):
    """
    Set the time period between polls of a node's state.
    """ 
    if canExecuteNetworkCommand == False:
        return buildNetworkBusyMessage()  
    try:        
        addLogEntry('SetPollInterval seconds:%s, interval Between Polls: %s' % (seconds, bool(intervalBetweenPolls)),)
        if network.state < network.STATE_AWAKED:            
            return jsonify ({'result' : False, 'reason' : 'network state must a minimum set to awaked'})    
        if seconds < 30:
            return jsonify ({'result' : False, 'reason' : 'interval is too small'})  
        network.set_poll_interval(1000*seconds, bool(intervalBetweenPolls))                
        return jsonify ({'result' : True})
    except Exception as e:
        addLogEntry(str(e), 'error')
        return jsonify ({'error' : str(e)})    
    
@app.route('/ZAutomation/api/v1/notifications',methods = ['GET'])
def GetLoginfos():
    return jsonify ({'data' : True})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(port_server),debug=False)
